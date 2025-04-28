from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from routes import user_routes, sensor_routes, relay_routes, setup_routes, notifications_routes, simple_notifications_routes, ai_simulator_routes, qr_auth_routes
import uvicorn
from middleware.websocket_manager import websocket_relay_endpoint, add_connection, remove_connection  # Import từ module mới
from databases.databases import *
from schemas import Notification
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# from routes.relay_routes import relay_connections
# from scheduler import harvest_scheduler
import logging
import os
import asyncio

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; specify domains for stricter security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)




active_connections = {}

# WebSocket endpoint cho relay
@app.websocket("/ws/relay")
async def relay_websocket(websocket: WebSocket):
    await websocket_relay_endpoint(websocket)
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    await add_connection(user_id, websocket)  # Thêm kết nối vào danh sách
    try:
        while True:
            data = await websocket.receive_text()  # Lắng nghe dữ liệu nếu cần
            print(f"Received: {data} from User {user_id}")

            # Lưu vào MongoDB
            notification = Notification(user_id=user_id, message=data)
            collection_notification.insert_one(notification.to_dict())  # MongoDB

    except WebSocketDisconnect:
        await remove_connection(user_id)  # Xóa kết nối khi bị ngắt

# Include routers
app.include_router(user_routes.router, tags=['Users'], prefix='/api/users')
app.include_router(sensor_routes.router, tags=['Sensors'], prefix='/api/sensors')
app.include_router(relay_routes.router, tags=['Relay'], prefix='/api/relay')
app.include_router(setup_routes.router, tags=['Setup'], prefix='/api/setup')
app.include_router(simple_notifications_routes.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(ai_simulator_routes.router, tags=['AI Simulator'], prefix='/api/ai-simulator')
app.include_router(qr_auth_routes.router, tags=['QR Auth'], prefix='/api/qr-auth')

# Sự kiện startup và shutdown
# Event handlers
# @app.on_event("startup")
# async def startup_event():
#     logger.info("Ứng dụng đang khởi động...")
#     # Tự động bắt đầu scheduler khi ứng dụng khởi động
#     harvest_scheduler.start()

# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info("Ứng dụng đang tắt...")
#     # Dừng scheduler khi ứng dụng tắt
#     harvest_scheduler.stop()

# # Root endpoint
# @app.get("/", tags=["root"])
# async def root():
#     return {"message": "AI Harvest Prediction API"}

# Lưu file HTML của bạn vào thư mục templates
templates = Jinja2Templates(directory="templates")


# Đảm bảo thư mục templates tồn tại
os.makedirs("templates", exist_ok=True)
# Xử lý lỗi
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Lỗi không xử lý: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Lỗi server"}
    )
@app.get("/ping")
def ping():
    return {"message": "Server is running"}
# Cleanup task để dọn dẹp các phiên QR hết hạn
async def cleanup_expired_qr_sessions():
    from middleware.websocket_manager import cleanup_expired_sessions
    
    while True:
        await cleanup_expired_sessions()
        # Kiểm tra và xóa phiên hết hạn mỗi 30 giây
        await asyncio.sleep(30)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)