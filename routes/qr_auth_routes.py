from fastapi import APIRouter, HTTPException, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json
import time
import logging
import uuid
import secrets
import socket
from middleware.websocket_manager import register_qr_session, qr_auth_sessions

router = APIRouter()
logger = logging.getLogger(__name__)

# Hàm lấy địa chỉ IPv4 nội bộ
def get_local_ip():
    """Lấy địa chỉ IPv4 nội bộ của máy"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        logger.error(f"Error getting local IP: {str(e)}")
        return 'localhost'

class QRSessionCreate(BaseModel):
    """Model yêu cầu tạo phiên QR từ ứng dụng Electron"""
    app_id: Optional[str] = "electron-app"
    device_info: Optional[Dict[str, Any]] = None
    ttl: Optional[int] = 300  # Thời gian sống của phiên (giây), mặc định 5 phút

class AuthRequest(BaseModel):
    """Model yêu cầu xác thực từ thiết bị di động"""
    session_id: str
    device_info: Dict[str, Any]

class AuthResponse(BaseModel):
    """Model phản hồi xác thực từ desktop"""
    session_id: str
    approved: bool
    user_data: Optional[Dict[str, Any]] = None

# API endpoint cho ứng dụng Electron để tạo phiên xác thực QR
@router.post("/create-session", response_class=JSONResponse)
async def create_qr_session_electron(request: Request, session_req: QRSessionCreate):
    """
    Tạo một phiên QR mới và trả về thông tin phiên cho ứng dụng Electron
    """
    try:
        # Tạo session ID và secret
        session_id = str(uuid.uuid4())
        secret = secrets.token_hex(16)
        
        # Tính thời gian hết hạn
        ttl = session_req.ttl if session_req.ttl else 300
        expires_at = int(time.time() + ttl)
        
        # Lấy địa chỉ IP nội bộ
        local_ip = get_local_ip()
        
        # Xác định scheme
        scheme = request.headers.get('x-forwarded-proto', 'http')
        
        # Tạo base URL với IPv4
        port = 8000  # Thay đổi port nếu cần
        base_url = f"{scheme}://{local_ip}:{port}"
        
        logger.info(f"Creating QR session for Electron: {session_id}")
        
        # Tạo dữ liệu phiên
        session_data = {
            "session_id": session_id,
            "secret": secret,
            "created_at": int(time.time()),
            "expires_at": expires_at,
            "app_id": session_req.app_id,
            "device_info": session_req.device_info,
            "status": "pending"
        }
        
        # Đăng ký phiên trong WebSocket manager
        await register_qr_session(session_id, session_data)
        
        # Tạo dữ liệu QR để trả về cho ứng dụng Electron
        qr_data = {
            "type": "qr_auth",
            "session_id": session_id,
            "secret": secret,
            "server_url": f"{base_url}/api/qr-auth/ws/qr-auth/{session_id}",
            "relay_url": f"{base_url}/ws/relay",
            "expires_at": expires_at,
            "ip": local_ip
        }
        
        # Trả về thông tin phiên
        return {
            "session_id": session_id,
            "expires_at": expires_at,
            "qr_data": qr_data,
            "ip": local_ip
        }
    
    except Exception as e:
        logger.error(f"Error creating QR session for Electron: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating QR session: {str(e)}")

# API endpoint để xác minh phiên QR từ thiết bị di động
@router.post("/verify", response_class=JSONResponse)
async def verify_qr_auth(request: Request, auth_request: AuthRequest):
    """
    Xác minh yêu cầu xác thực QR từ thiết bị di động
    """
    session_id = auth_request.session_id
    device_info = auth_request.device_info
    client_ip = request.client.host
    
    logger.info(f"Verification request from mobile: {session_id}")
    
    if session_id not in qr_auth_sessions:
        logger.error(f"Session not found: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = qr_auth_sessions[session_id]
    
    # Kiểm tra hết hạn
    if time.time() > session['data'].get('expires_at', 0):
        logger.warning(f"Session expired: {session_id}")
        raise HTTPException(status_code=410, detail="Session expired")
    
    # Lưu thông tin thiết bị di động
    if 'mobile_info' not in session or not session['mobile_info']:
        session['mobile_info'] = device_info
    
    # Cập nhật thông tin IP của thiết bị di động
    if 'ip' not in device_info or not device_info.get('ip'):
        device_info['ip'] = client_ip
    
    # Gửi yêu cầu xác thực đến desktop
    if session['desktop'] or session['desktop_connection']:
        target = session['desktop'] if session['desktop'] else session['desktop_connection']
        try:
            await target.send_json({
                "type": "auth-request",
                "session_id": session_id,
                "device_info": device_info
            })
            logger.info(f"Auth request sent to desktop for session {session_id}")
            
            # Trả về trạng thái đang chờ xác thực
            return {
                "success": True,
                "status": "pending",
                "message": "Authentication request sent to desktop"
            }
        except Exception as e:
            logger.error(f"Error sending auth request to desktop: {str(e)}")
            raise HTTPException(status_code=500, detail="Error sending auth request to desktop")
    else:
        # Desktop chưa kết nối hoặc đã ngắt kết nối
        return {
            "success": False,
            "status": "waiting_desktop",
            "message": "Desktop not connected. Please make sure the desktop application is running."
        }

# API endpoint để kiểm tra trạng thái phiên từ thiết bị di động
@router.get("/status/{session_id}", response_class=JSONResponse)
async def get_qr_status(session_id: str):
    """
    Kiểm tra trạng thái của phiên QR
    """
    if session_id not in qr_auth_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = qr_auth_sessions[session_id]
    
    # Kiểm tra hết hạn
    if time.time() > session['data'].get('expires_at', 0):
        raise HTTPException(status_code=410, detail="Session expired")
    
    return {
        "session_id": session_id,
        "status": session.get('status', 'pending'),
        "desktop_connected": session['desktop'] is not None or session['desktop_connection'] is not None,
        "mobile_connected": session['mobile'] is not None,
        "expires_at": session['data'].get('expires_at')
    }

# API endpoint để ping server và lấy địa chỉ IP
@router.get("/ping", response_class=JSONResponse)
async def ping():
    """
    Endpoint đơn giản để kiểm tra kết nối server và lấy địa chỉ IP
    """
    local_ip = get_local_ip()
    return {
        "message": "QR Authentication server is running", 
        "ip": local_ip,
        "timestamp": int(time.time())
    }