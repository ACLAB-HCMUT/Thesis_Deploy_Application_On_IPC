# scheduler.py
import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict
from middleware.websocket_manager import broadcast_notification

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Danh sách user mẫu cho demo
DEMO_USERS = [1, 2, 3, 4, 5]  # Giả lập 5 user

class HarvestPredictionScheduler:
    """
    Lập lịch tự động gửi thông báo dự đoán thu hoạch
    """
    def __init__(self, interval_seconds: int = 30):
        self.interval_seconds = interval_seconds
        self.is_running = False
        self.task = None
        
    async def generate_prediction_for_user(self, user_id: int) -> Dict:
        """
        Tạo dữ liệu dự đoán cho user
        """
        days_to_harvest = random.randint(30, 60)
        harvest_date = (datetime.now() + timedelta(days=days_to_harvest)).strftime("%Y-%m-%d")
        
        # Dữ liệu dự đoán
        prediction_data = {
            "harvest_date": harvest_date,
            "confidence": round(random.uniform(0.75, 0.98), 2),
            "days_remaining": days_to_harvest,
            "crop_health": random.choice(["excellent", "good", "average"]),
            "crop_type": random.choice(["Lua", "Ngou", "Khoai tay", "Ca chua", "Da hau", "Ca rot", "Ot"]),  # Thêm trường crop_type": f"{random.randint(80, 120)}%"
        }
        
        # Tạo message thông báo
        message = (
            f"Dự đoán: Cây trồng của bạn sẽ sẵn sàng thu hoạch vào "
            f"ngày {harvest_date} (còn {days_to_harvest} ngày). "
            f"Tình trạng cây: {prediction_data['crop_health']}. "
            f"Loại cây: {prediction_data['crop_type']}."
        )
        
        # Chuẩn bị dữ liệu để gửi qua WebSocket
        notification = {
            "type": "ai_prediction",  # Đánh dấu rõ đây là dự đoán AI
            "message": message,
            "prediction": prediction_data,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id
        }
        
        return notification
    
    async def send_scheduled_predictions(self):
        """
        Gửi dự đoán định kỳ cho tất cả user
        """
        while self.is_running:
            try:
                logger.info(f"Gửi dự đoán tự động vào {datetime.now().isoformat()}")
                
                # Tạo và gửi thông báo cho mỗi user
                for user_id in DEMO_USERS:
                    prediction = await self.generate_prediction_for_user(user_id)
                    await broadcast_notification(prediction)
                    logger.info(f"Đã gửi dự đoán cho user {user_id}")
                
                # Đợi đến kỳ tiếp theo
                await asyncio.sleep(self.interval_seconds)
                
            except Exception as e:
                logger.error(f"Lỗi khi gửi dự đoán tự động: {str(e)}")
                await asyncio.sleep(5)  # Đợi một chút trước khi thử lại
    
    def start(self):
        """
        Bắt đầu scheduler
        """
        if not self.is_running:
            self.is_running = True
            self.task = asyncio.create_task(self.send_scheduled_predictions())
            logger.info(f"Đã bắt đầu lập lịch dự đoán tự động mỗi {self.interval_seconds} giây")
    
    def stop(self):
        """
        Dừng scheduler
        """
        if self.is_running:
            self.is_running = False
            if self.task:
                self.task.cancel()
            logger.info("Đã dừng lập lịch dự đoán tự động")

# Tạo instance toàn cục
harvest_scheduler = HarvestPredictionScheduler(interval_seconds=60)  # Mỗi 60 giây