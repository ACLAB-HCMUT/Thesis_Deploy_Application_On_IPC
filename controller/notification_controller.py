# # app/controller/notification_controller.py
# from services.notification_service import create_notification
# from fastapi import HTTPException, status
# from middleware.websocket_manager import send_notification, broadcast_notification  # Import từ websocket_manager.py

# from fastapi import HTTPException, status

# import random
# from datetime import datetime, timedelta
# import json

# async def controller_create_notification(body: dict, token: str):
#     user_id = body.get('user_id')
#     message = body.get('message')

#     if not user_id or not message:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Missing user_id or message"
#         )

#     notification = await create_notification(user_id, message)

#     # Gửi thông báo qua WebSocket nếu người dùng đang online
#     await send_notification(user_id, message)
    
#     return notification

# async def controller_get_notifications(user_id: int, token: str):
#     notifications = await notification_service.get_notifications_by_user(user_id)
#     return notifications

# async def controller_mark_as_seen(user_id: int, notification_id: int, token: str):
#     result = await notification_service.mark_as_seen(user_id, notification_id)
#     if not result:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Notification not found"
#         )
#     return {"message": "Notification marked as seen"}



# # Thêm function dự đoán ngày thu hoạch
# async def predict_harvest(body: dict):
#     user_id = body.get('user_id')
#     input_data = body.get('input_data', {})
    
#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Missing user_id"
#         )
    
#     # Mock AI prediction model (thay thế bằng model thực tế sau này)
#     # Giả sử trồng cây ăn quả cần 30-60 ngày để thu hoạch
#     days_to_harvest = random.randint(30, 60)
#     harvest_date = (datetime.now() + timedelta(days=days_to_harvest)).strftime("%Y-%m-%d")
    
#     # Tạo dữ liệu dự đoán
#     prediction_data = {
#         "harvest_date": harvest_date,
#         "confidence": random.uniform(0.75, 0.98),
#         "days_remaining": days_to_harvest,
#         "crop_health": random.choice(["excellent", "good", "average"]),
#         "estimated_yield": f"{random.randint(80, 120)}%"
#     }
    
#     # Tạo message thông báo
#     health_emoji = "🌱" if prediction_data["crop_health"] == "excellent" else "🌿"
#     message = (
#         f"{health_emoji} Dự đoán: Cây trồng của bạn sẽ sẵn sàng thu hoạch vào "
#         f"ngày {harvest_date} (còn {days_to_harvest} ngày). "
#         f"Tình trạng cây: {prediction_data['crop_health']}. "
#         f"Năng suất ước tính: {prediction_data['estimated_yield']}."
#     )
    
#     # Tạo notification để lưu vào database
#     notification = await create_notification(user_id, message)
    
#     # Chuẩn bị dữ liệu để gửi qua WebSocket
#     ws_notification = {
#         "type": "notification",
#         "message": message,
#         "prediction": prediction_data,
#         "timestamp": datetime.now().isoformat(),
#         "user_id": user_id
#     }
    
#     # Broadcast notification qua WebSocket
#     await broadcast_notification(ws_notification)
    
#     return {
#         "success": True,
#         "message": "Prediction notification sent",
#         "prediction": prediction_data,
#         "notification": notification
#     }

#update new version
