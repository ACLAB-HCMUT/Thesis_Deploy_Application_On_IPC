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
import aio_pika
import json
from databases.databases import *

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; specify domains for stricter security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

TOKEN_FILE = "core_iot_token.txt"

def save_token_to_file(token):
    """Lưu token vào file"""
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)
    print(f"Token đã được lưu vào file {TOKEN_FILE}")

def load_token_from_file():
    """Đọc token từ file"""
    if not os.path.exists(TOKEN_FILE):
        return None
    
    try:
        with open(TOKEN_FILE, 'r') as f:
            token = f.read().strip()
            return token if token else None
    except Exception as e:
        print(f"Lỗi khi đọc file token: {str(e)}")
        return None

# Consumer RabbitMQ
async def process_message(queue_name: str, message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        print(f"Received data from {queue_name}: {data}")
        
        if queue_name in ["sensor_data_queue", "relay_data_queue", "scheduler_data_queue"]:
            # Lưu vào MongoDB
            try:
                if queue_name == "sensor_data_queue":
                    collection_test_sensor_data.insert_one(data)

                if queue_name == "scheduler_data_queue":
                    collection_setup_scheduler.insert_one(data)
                
                if queue_name == "relay_data_queue":
                    # Cập nhật hoặc chèn mới
                    relay_name = data.get("relayName")
                    query = {"relayName": relay_name}
                    update = {
                        "$set": {
                            "status": data.get("status"),
                            "timestamp": data.get("timestamp"),
                            "updated_by": data.get("updated_by"),
                            "email_user": data.get("email_user")
                        }
                    }
                    collection_relay.update_one(query, update, upsert=True)

            except Exception as e:
                print(f"Failed to save to MongoDB: {str(e)}")
        
        elif queue_name == "core_iot_queue":
            # Gọi API Core IOT
            try:
                core_iot_url = "https://app.coreiot.io/api/plugins/telemetry/DEVICE/21c4e8a0-f63f-11ef-a887-6d1a184f2bb5/SHARED_SCOPE"
                
                # Đọc token từ file nếu có
                token = load_token_from_file()
                
                # Nếu không có token trong file, sử dụng token mặc định
                if not token:
                    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ2aW5oLm5ndXllbjEyM0BoY211dC5lZHUudm4iLCJ1c2VySWQiOiJjOWY5OGNmMC1lMTQ2LTExZWYtYWQwOS01MTVmNzkwZWQ5ZGYiLCJzY29wZXMiOlsiVEVOQU5UX0FETUlOIl0sInNlc3Npb25JZCI6ImU4MzU5YzgxLWQ2NmEtNDljYi05NjgyLWE3MTg0MDFlOTQ4YyIsImV4cCI6MTc0MjAyMDQzMSwiaXNzIjoiY29yZWlvdC5pbyIsImlhdCI6MTc0MjAxMTQzMSwiZmlyc3ROYW1lIjoiVklOSCIsImxhc3ROYW1lIjoiTkdVWeG7hE4gS0jhuq5DIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6ImM5ZTk4NzYwLWUxNDYtMTFlZi1hZDA5LTUxNWY3OTBlZDlkZiIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.mS-l5RJ-zRfHzJ237nGnnBNidf2KsQqnb0mgJWJtw8voOdkpMlOH3wuQvUtaKIV9qn8BZhr60E_DRrCzaDvp7w"
                
                headers = {
                    "Content-Type": "application/json",
                    "X-Authorization": f"Bearer {token}"
                }
                core_iot_body = {
                    "method": data.get("method"),
                    "value": data.get("value")
                }
                
                max_retries = 2
                for attempt in range(max_retries):
                    try:
                        response = requests.post(core_iot_url, headers=headers, json=core_iot_body)
                        if response.status_code == 401 and "Token has expired" in response.text:
                            login_url = "https://app.coreiot.io/api/auth/login"
                            login_body = {"username": "vinh.nguyen123@hcmut.edu.vn", "password": "Vinhnguyen1$"}
                            login_response = requests.post(login_url, json=login_body)
                            if login_response.status_code == 200:
                                token = login_response.json().get('token')
                                # Lưu token mới vào file
                                save_token_to_file(token)
                                headers["X-Authorization"] = f"Bearer {token}"
                                continue
                        if response.status_code == 200:
                            print(f"Successfully sent command to Core IOT: {response.text}")
                            break
                        else:
                            print(f"Error sending command to Core IOT: {response.status_code}, {response.text}")
                    except Exception as e:
                        print(f"Exception when calling Core IOT API: {str(e)}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(1)
            except Exception as e:
                print(f"Failed to process Core IOT command: {str(e)}")
        
        await asyncio.sleep(2)  # Giả lập xử lý lâu

async def start_rabbitmq_consumer():
    global consumer_running
    QUEUES = ["sensor_data_queue", "relay_data_queue", "core_iot_queue"]
    
    async def consume_queue(queue_name):
        while consumer_running:
            try:
                connection = await aio_pika.connect_robust(f"amqp://guest:guest@{RABBITMQ_HOST}/")
                async with connection:
                    channel = await connection.channel()
                    queue = await channel.declare_queue(queue_name, durable=True)
                    await channel.set_qos(prefetch_count=1)
                    
                    print(f"RabbitMQ consumer started for {queue_name}. Waiting for data...")
                    await queue.consume(lambda msg: process_message(queue_name, msg))
                    
                    try:
                        await asyncio.wait_for(asyncio.Event().wait(), timeout=1.0)
                    except asyncio.TimeoutError:
                        pass
            except (asyncio.CancelledError, Exception) as e:
                print(f"Consumer error for {queue_name}: {str(e)}. Retrying in 5 seconds...")
                await asyncio.sleep(5)
    
    tasks = [asyncio.create_task(consume_queue(queue)) for queue in QUEUES]
    await asyncio.gather(*tasks, return_exceptions=True)

@app.on_event("startup")
async def startup_event():
    global consumer_task
    consumer_task = asyncio.create_task(start_rabbitmq_consumer())
    print("Started RabbitMQ consumer task.")




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