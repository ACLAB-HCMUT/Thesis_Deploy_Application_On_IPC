# backend/middleware/websocket_manager.py

from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any, Optional
import json
import logging
import time

logger = logging.getLogger(__name__)

# Dictionary lưu trữ kết nối WebSocket
active_connections = {}

# Danh sách kết nối WebSocket cho relay
relay_connections: List[WebSocket] = []

# Dictionary lưu trữ kết nối QR auth
qr_auth_sessions = {}

async def websocket_relay_endpoint(websocket: WebSocket):
    """Điểm cuối WebSocket relay chính - kết nối từ ứng dụng Electron"""
    logger.info("Attempting WebSocket connection to /ws/relay")
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    
    # Lưu lại kết nối để sử dụng sau này
    relay_connections.append(websocket)
    
    try:
        # Nhận và xử lý tin nhắn
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                logger.info(f"Received message from relay: {message}")
                
                # Xử lý các loại tin nhắn khác nhau
                if message.get("type") == "register-desktop":
                    # Đăng ký desktop client với phiên QR
                    session_id = message.get("session_id")
                    device_info = message.get("device_info", {})
                    
                    if session_id and session_id in qr_auth_sessions:
                        qr_auth_sessions[session_id]["desktop_connection"] = websocket
                        qr_auth_sessions[session_id]["desktop_info"] = device_info
                        logger.info(f"Desktop registered for session {session_id}")
                
                elif message.get("type") == "auth-response":
                    # Phản hồi xác thực từ desktop
                    session_id = message.get("session_id")
                    approved = message.get("approved", False)
                    user_data = message.get("user_data", {})
                    
                    if session_id and session_id in qr_auth_sessions:
                        # Cập nhật trạng thái phiên
                        qr_auth_sessions[session_id]["status"] = "approved" if approved else "rejected"
                        
                        # Gửi phản hồi cho thiết bị di động
                        mobile_conn = qr_auth_sessions[session_id].get("mobile")
                        if mobile_conn:
                            response_message = {
                                "type": "auth-approved" if approved else "auth-rejected",
                                "message": "Authentication approved" if approved else "Authentication rejected",
                                "user_data": user_data if approved else None
                            }
                            await mobile_conn.send_json(response_message)
                            logger.info(f"Auth response sent to mobile for session {session_id}: {approved}")
            
            except json.JSONDecodeError:
                logger.error("Received invalid JSON data")
            except Exception as e:
                logger.error(f"Error processing relay message: {e}")
    
    except WebSocketDisconnect:
        # Xóa kết nối khi ngắt
        relay_connections.remove(websocket)
        
        # Tìm và cập nhật các phiên của desktop bị ngắt kết nối
        for session_id, session in qr_auth_sessions.items():
            if session.get("desktop_connection") == websocket:
                session["desktop_connection"] = None
                # Thông báo cho mobile nếu còn kết nối
                if session.get("mobile"):
                    try:
                        await session["mobile"].send_json({
                            "type": "desktop-disconnected",
                            "message": "Desktop application disconnected"
                        })
                    except Exception as e:
                        logger.error(f"Error notifying mobile: {e}")
        
        logger.info("Relay WebSocket disconnected")
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in relay_connections:
            relay_connections.remove(websocket)

async def broadcast_relay_update(relay_data: dict):
    """Gửi dữ liệu cập nhật đến tất cả các kết nối relay"""
    logger.info(f"Broadcasting relay data: {relay_data}")
    for connection in relay_connections:
        try:
            await connection.send_json(relay_data)
        except Exception as e:
            logger.error(f"Error broadcasting to relay client: {e}")

async def add_connection(user_id: int, websocket: WebSocket):
    """Thêm kết nối WebSocket cho user_id"""
    active_connections[user_id] = websocket

async def remove_connection(user_id: int):
    """Xóa kết nối WebSocket cho user_id"""
    if user_id in active_connections:
        del active_connections[user_id]

async def send_notification(user_id: int, message: str):
    """Gửi thông báo đến user_id cụ thể"""
    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_text(message)

async def broadcast_notification(notification_data: dict):
    """Gửi thông báo đến tất cả các kết nối relay"""
    logger.info(f"Broadcasting notification data: {notification_data}")
    for connection in relay_connections:
        try:
            await connection.send_json(notification_data)
        except Exception as e:
            logger.error(f"Error broadcasting to notification client: {e}")    

async def register_qr_session(session_id: str, data: dict):
    """Đăng ký một phiên QR mới"""
    qr_auth_sessions[session_id] = {
        'desktop': None,          # WebSocket kết nối từ desktop (FastAPI)
        'desktop_connection': None,  # WebSocket relay connection từ Electron
        'desktop_info': {},       # Thông tin về thiết bị desktop
        'mobile': None,           # WebSocket kết nối từ mobile
        'mobile_info': {},        # Thông tin về thiết bị mobile
        'data': data,             # Thông tin phiên (secret, expire, etc.)
        'status': 'pending'       # Trạng thái phiên (pending, approved, rejected)
    }
    logger.info(f"Registered new QR session: {session_id}")
    return True

async def connect_qr_device(session_id: str, device_type: str, websocket: WebSocket, device_info: dict = None):
    """Kết nối một thiết bị với phiên QR"""
    if session_id not in qr_auth_sessions:
        return False
    
    session = qr_auth_sessions[session_id]
    session[device_type] = websocket
    
    if device_info:
        session[f'{device_type}_info'] = device_info
    
    logger.info(f"Connected {device_type} to session {session_id}")
    
    # Nếu là mobile kết nối, thông báo cho desktop
    if device_type == 'mobile':
        # Thông báo qua kết nối desktop trực tiếp (FastAPI)
        if session['desktop']:
            try:
                await session['desktop'].send_json({
                    "type": "auth-request",
                    "session_id": session_id,
                    "device_info": device_info
                })
            except Exception as e:
                logger.error(f"Error notifying desktop through FastAPI: {e}")
        
        # Thông báo qua kết nối relay (Electron)
        if session['desktop_connection']:
            try:
                await session['desktop_connection'].send_json({
                    "type": "auth-request",
                    "session_id": session_id,
                    "device_info": device_info
                })
            except Exception as e:
                logger.error(f"Error notifying desktop through relay: {e}")
    
    return True

async def disconnect_qr_device(session_id: str, device_type: str):
    """Ngắt kết nối thiết bị khỏi phiên QR"""
    if session_id in qr_auth_sessions and qr_auth_sessions[session_id][device_type]:
        qr_auth_sessions[session_id][device_type] = None
        logger.info(f"Disconnected {device_type} from session {session_id}")
        
        # Kiểm tra nếu cả hai thiết bị đều ngắt kết nối thì xóa phiên
        session = qr_auth_sessions[session_id]
        if not session['desktop'] and not session['mobile'] and not session['desktop_connection']:
            del qr_auth_sessions[session_id]
            logger.info(f"Removed session {session_id} due to all devices disconnected")
        
        # Thông báo cho thiết bị còn lại
        if device_type == 'mobile':
            # Thông báo cho desktop trực tiếp (FastAPI)
            if session['desktop']:
                try:
                    await session['desktop'].send_json({
                        "type": "mobile-disconnected",
                        "session_id": session_id
                    })
                except Exception as e:
                    logger.error(f"Error notifying desktop: {e}")
            
            # Thông báo qua kết nối relay (Electron)
            if session['desktop_connection']:
                try:
                    await session['desktop_connection'].send_json({
                        "type": "mobile-disconnected",
                        "session_id": session_id
                    })
                except Exception as e:
                    logger.error(f"Error notifying desktop through relay: {e}")
        
        elif device_type == 'desktop':
            # Thông báo cho mobile
            if session['mobile']:
                try:
                    await session['mobile'].send_json({
                        "type": "desktop-disconnected",
                        "session_id": session_id
                    })
                except Exception as e:
                    logger.error(f"Error notifying mobile: {e}")

async def relay_qr_message(session_id: str, from_device: str, message: dict):
    """Chuyển tiếp tin nhắn giữa desktop và mobile"""
    if session_id not in qr_auth_sessions:
        return False
    
    session = qr_auth_sessions[session_id]
    target_device = 'mobile' if from_device == 'desktop' else 'desktop'
    
    # Xử lý các loại tin nhắn đặc biệt
    if from_device == 'desktop' and message.get('type') == 'auth-response':
        # Cập nhật trạng thái phiên
        approved = message.get('approved', False)
        session['status'] = 'approved' if approved else 'rejected'
        
        # Thông báo cho mobile
        if session['mobile']:
            try:
                await session['mobile'].send_json({
                    'type': 'auth-approved' if approved else 'auth-rejected',
                    'message': 'Authentication approved' if approved else 'Authentication rejected',
                    'user_data': message.get('user_data')
                })
                return True
            except Exception as e:
                logger.error(f"Error sending auth response to mobile: {e}")
                return False
    
    # Chuyển tiếp tin nhắn thông thường
    if session[target_device]:
        try:
            await session[target_device].send_json(message)
            logger.info(f"Relayed message from {from_device} to {target_device} in session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error relaying message in session {session_id}: {e}")
            return False
    
    # Nếu đích là desktop, thử gửi qua kết nối relay
    if target_device == 'desktop' and session['desktop_connection']:
        try:
            await session['desktop_connection'].send_json(message)
            logger.info(f"Relayed message from {from_device} to desktop_connection in session {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error relaying message to desktop_connection in session {session_id}: {e}")
            return False
    
    return False

# Hàm kiểm tra và xóa phiên hết hạn
async def cleanup_expired_sessions():
    """Xóa các phiên QR đã hết hạn"""
    current_time = time.time()
    expired_sessions = []
    
    for session_id, session in qr_auth_sessions.items():
        if current_time > session['data'].get('expires_at', 0):
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        # Thông báo cho các thiết bị kết nối
        session = qr_auth_sessions[session_id]
        
        # Thông báo desktop
        if session['desktop']:
            try:
                await session['desktop'].send_json({
                    "type": "session-expired",
                    "session_id": session_id
                })
            except Exception:
                pass
        
        # Thông báo desktop qua relay
        if session['desktop_connection']:
            try:
                await session['desktop_connection'].send_json({
                    "type": "session-expired",
                    "session_id": session_id
                })
            except Exception:
                pass
        
        # Thông báo mobile
        if session['mobile']:
            try:
                await session['mobile'].send_json({
                    "type": "session-expired",
                    "session_id": session_id
                })
            except Exception:
                pass
        
        # Xóa phiên
        del qr_auth_sessions[session_id]
        logger.info(f"Removed expired session: {session_id}")