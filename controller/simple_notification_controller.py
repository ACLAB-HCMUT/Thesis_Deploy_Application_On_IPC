
# simple_notification_controller.py
from fastapi import HTTPException, status
import random
from datetime import datetime, timedelta
import logging
from middleware.websocket_manager import broadcast_notification
# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hàm tạo thông báo đơn giản
async def create_notification(user_id, message):
    """
    Hàm giả lập tạo thông báo
    """
    notification_id = random.randint(1000, 9999)
    return {
        "id": notification_id,
        "user_id": user_id,
        "message": message,
        "created_at": datetime.now().isoformat(),
        "seen": False
    }

# Hàm dự đoán thu hoạch đơn giản
async def predict_harvest(body):
    """
    Hàm dự đoán thu hoạch đơn giản khi được gọi thủ công
    """
    try:
        user_id = body.get('user_id')
        
        if not user_id:
            raise ValueError("Missing user_id")
        
        # Tạo dữ liệu dự đoán mẫu
        days_to_harvest = random.randint(30, 60)
        harvest_date = (datetime.now() + timedelta(days=days_to_harvest)).strftime("%Y-%m-%d")
        confidence_value = round(random.uniform(0.75, 0.98), 2)
        crop_health = random.choice(["excellent", "good", "average"])
        # estimated_yield_value = f"{random.randint(80, 120)}%"
        crop_type = random.choice(["Lua", "Ngou", "Khoai tay", "Ca chua", "Da hau", "Ca rot", "Ot"])
        # Dữ liệu dự đoán
        prediction_data = {
            "harvest_date": harvest_date,
            "confidence": confidence_value,
            "days_remaining": days_to_harvest,
            "crop_health": crop_health,
            "crop_type": crop_type
        }
        
        # Tạo message thông báo
        message = (
            f"Dự đoán: Cây trồng của bạn sẽ sẵn sàng thu hoạch vào "
            f"ngày {harvest_date} (còn {days_to_harvest} ngày). "
            f"Tình trạng cây: {prediction_data['crop_health']}. "
            f"Loại cây: {prediction_data['crop_type']}"
        )
        
        # Tạo notification
        notification = await create_notification(user_id, message)
        
        # Chuẩn bị dữ liệu để gửi qua WebSocket
        ws_notification = {
            "type": "notification",
            "message": message,
            "prediction": prediction_data,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id
        }
        
        # Broadcast notification
        await broadcast_notification(ws_notification)
        
        return {
            "success": True,
            "message": "Prediction notification sent",
            "prediction": prediction_data,
            "notification": notification
        }
        
    except Exception as e:
        logger.error(f"Error in predict_harvest: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create prediction notification"
        }

# # Hàm để bắt đầu/dừng scheduler
# async def manage_prediction_scheduler(action: str):
#     """
#     Quản lý scheduler tự động dự đoán
#     """
#     try:
#         from scheduler import harvest_scheduler
        
#         if action == "start":
#             harvest_scheduler.start()
#             return {"success": True, "message": "Đã bắt đầu lập lịch tự động dự đoán"}
#         elif action == "stop":
#             harvest_scheduler.stop()
#             return {"success": True, "message": "Đã dừng lập lịch tự động dự đoán"}
#         else:
#             return {"success": False, "message": "Hành động không hợp lệ. Sử dụng 'start' hoặc 'stop'"}
    
#     except Exception as e:
#         logger.error(f"Lỗi khi quản lý scheduler: {str(e)}")
#         return {"success": False, "error": str(e)}