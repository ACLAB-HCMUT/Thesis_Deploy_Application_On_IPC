# controller/ai_simulator_controller.py
import random
from datetime import datetime, timedelta
import asyncio
import logging
from middleware.websocket_manager import broadcast_relay_update

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Danh sách loại cây trồng để mô phỏng
CROPS = ["Lúa", "Ngô", "Khoai tây", "Cà chua", "Dưa hấu", "Cà rốt", "Ớt"]

# Mô phỏng dữ liệu cảm biến
async def generate_sensor_data(device_id=None):
    """
    Tạo dữ liệu cảm biến giả lập cho thiết bị
    """
    if not device_id:
        device_id = f"device_{random.randint(100, 999)}"
        
    return {
        "device_id": device_id,
        "timestamp": datetime.now().isoformat(),
        "sensors": {
            "temperature": round(random.uniform(20, 35), 1),
            "humidity": round(random.uniform(60, 95), 1),
            "soil_moisture": round(random.uniform(30, 80), 1),
            "light_intensity": round(random.uniform(500, 10000), 0),
            "pH": round(random.uniform(5.5, 7.5), 1)
        }
    }

# Xử lý API dự đoán tùy chỉnh
async def handle_custom_predict(data):
    """
    Xử lý yêu cầu dự đoán tùy chỉnh từ API
    """
    try:
        # Kiểm tra dữ liệu đầu vào cần thiết
        if not data.get("user_id"):
            return {
                "success": False,
                "error": "Thiếu thông tin user_id",
                "message": "Không thể tạo dự đoán tùy chỉnh"
            }
            
        user_id = data.get("user_id")
        
        # Tạo dữ liệu sensor giả nếu cần thiết
        device_id = data.get("device_id", f"device_{random.randint(100, 999)}")
        sensor_data = await generate_sensor_data(device_id)
        
        # Lấy thông tin từ dữ liệu người dùng gửi lên
        crop_type = data.get("crop_type", random.choice(CROPS))
        
        # Tạo thông điệp
        message = f"[AI dự đoán] {data.get('message', f'Dự đoán cho {crop_type}')}"
        
        # Tạo prediction từ dữ liệu người dùng gửi lên
        prediction_data = {
            **data,  # Giữ tất cả dữ liệu người dùng gửi lên
            "device_id": device_id,
            "sensor_data": sensor_data["sensors"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Tạo payload để gửi qua WebSocket
        ws_payload = {
            "type": "ai_prediction",
            "user_id": user_id,
            "message": message,
            "prediction": prediction_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Gửi thông báo qua WebSocket
        await broadcast_relay_update(ws_payload)
        
        return {
            "success": True,
            "message": "Dự đoán AI đã được gửi thành công",
            "prediction": prediction_data
        }
        
    except Exception as e:
        logger.error(f"Lỗi khi xử lý dự đoán tùy chỉnh: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Không thể tạo dự đoán tùy chỉnh"
        }

# Xử lý API cảnh báo đơn lẻ tùy chỉnh
async def handle_custom_monitor_single(data):
    """
    Xử lý yêu cầu cảnh báo đơn lẻ tùy chỉnh từ API
    """
    try:
        # Kiểm tra dữ liệu đầu vào cần thiết
        if not data.get("user_id"):
            return {
                "success": False,
                "error": "Thiếu thông tin user_id",
                "message": "Không thể tạo cảnh báo tùy chỉnh"
            }
            
        user_id = data.get("user_id")
        device_id = data.get("device_id", data.get("device", f"device_{random.randint(100, 999)}"))
        
        # Tạo dữ liệu sensor giả
        sensor_data = await generate_sensor_data(device_id)
        
        # Tạo thông điệp từ dữ liệu người dùng hoặc mặc định
        message = data.get("message", f"[Cảnh báo] {data.get('description', 'Phát hiện vấn đề với thiết bị ' + device_id)}")
        
        # Tạo dữ liệu cảnh báo
        alert_data = {
            **data,  # Giữ tất cả dữ liệu người dùng gửi lên
            "device_id": device_id,
            "sensor_data": sensor_data["sensors"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Tạo payload để gửi qua WebSocket
        alert_payload = {
            "type": "ai_alert",
            "user_id": user_id,
            "device_id": device_id,
            "message": message,
            "alert": alert_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Gửi cảnh báo qua WebSocket
        await broadcast_relay_update(alert_payload)
        
        return {
            "success": True,
            "message": "Cảnh báo AI đã được gửi thành công",
            "alert": alert_data
        }
        
    except Exception as e:
        logger.error(f"Lỗi khi xử lý cảnh báo tùy chỉnh: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Không thể tạo cảnh báo tùy chỉnh"
        }

# Mô phỏng AI phân tích và đưa ra dự đoán (giữ lại cho khả năng tương thích)
async def simulate_ai_analysis(user_id, device_id=None, crop_type=None):
    """
    Mô phỏng AI phân tích dữ liệu và đưa ra dự đoán
    """
    try:
        # Tạo dữ liệu cảm biến giả
        sensor_data = await generate_sensor_data(device_id)
        
        # Chọn ngẫu nhiên loại cây nếu không được cung cấp
        if not crop_type:
            crop_type = random.choice(CROPS)
            
        # Tạo dữ liệu dự đoán
        days_to_harvest = random.randint(15, 90)
        harvest_date = (datetime.now() + timedelta(days=days_to_harvest)).strftime("%Y-%m-%d")
        confidence = round(random.uniform(0.70, 0.99), 2)
        
        # Phân tích tình trạng sức khỏe cây trồng dựa trên dữ liệu cảm biến
        temp = sensor_data["sensors"]["temperature"]
        humidity = sensor_data["sensors"]["humidity"]
        soil_moisture = sensor_data["sensors"]["soil_moisture"]
        
        # Logic đơn giản để xác định sức khỏe cây trồng
        health_score = 0
        health_issues = []
        
        # Kiểm tra nhiệt độ
        if temp < 15:
            health_score -= 20
            health_issues.append("Nhiệt độ quá thấp")
        elif temp > 35:
            health_score -= 25
            health_issues.append("Nhiệt độ quá cao")
        else:
            health_score += 20
            
        # Kiểm tra độ ẩm
        if humidity < 40:
            health_score -= 15
            health_issues.append("Độ ẩm không khí quá thấp")
        elif humidity > 90:
            health_score -= 10
            health_issues.append("Độ ẩm không khí quá cao")
        else:
            health_score += 15
            
        # Kiểm tra độ ẩm đất
        if soil_moisture < 20:
            health_score -= 30
            health_issues.append("Đất quá khô")
        elif soil_moisture > 80:
            health_score -= 20
            health_issues.append("Đất quá ẩm")
        else:
            health_score += 25
            
        # Xác định tình trạng sức khỏe
        if health_score >= 40:
            crop_health = "Tuyệt vời"
            estimated_yield = f"{random.randint(90, 120)}%"
        elif health_score >= 20:
            crop_health = "Tốt"
            estimated_yield = f"{random.randint(80, 100)}%"
        elif health_score >= 0:
            crop_health = "Trung bình"
            estimated_yield = f"{random.randint(60, 85)}%"
        else:
            crop_health = "Cần chú ý"
            estimated_yield = f"{random.randint(40, 70)}%"
            
        # Tạo khuyến nghị
        recommendations = []
        if "Đất quá khô" in health_issues:
            recommendations.append("Tăng tưới nước")
        if "Đất quá ẩm" in health_issues:
            recommendations.append("Giảm tưới nước")
        if "Nhiệt độ quá cao" in health_issues:
            recommendations.append("Tăng độ che phủ")
        
        # Tạo dữ liệu dự đoán đầy đủ
        prediction_data = {
            "crop_type": crop_type,
            "device_id": sensor_data["device_id"],
            "harvest_date": harvest_date,
            "days_remaining": days_to_harvest,
            "confidence": confidence,
            "crop_health": crop_health,
            "estimated_yield": estimated_yield,
            "health_issues": health_issues if health_issues else ["Không phát hiện vấn đề"],
            "recommendations": recommendations if recommendations else ["Tiếp tục chăm sóc như hiện tại"],
            "sensor_data": sensor_data["sensors"]
        }
        
        # Tạo thông báo
        message = (
            f"[AI dự đoán cho {crop_type}] Ngày thu hoạch dự kiến: {harvest_date} "
            f"(còn {days_to_harvest} ngày). Tình trạng cây: {crop_health}. "
            f"Năng suất ước tính: {estimated_yield}."
        )
        
        # Tạo payload để gửi qua WebSocket
        ws_payload = {
            "type": "ai_prediction",
            "user_id": user_id,
            "message": message,
            "prediction": prediction_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Gửi thông báo qua WebSocket
        await broadcast_relay_update(ws_payload)
        
        return {
            "success": True,
            "message": "Dự đoán AI đã được gửi thành công",
            "prediction": prediction_data
        }
        
    except Exception as e:
        logger.error(f"Lỗi khi mô phỏng AI: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Không thể tạo dự đoán AI"
        }

# Mô phỏng theo dõi cây trồng và cảnh báo (giữ lại cho khả năng tương thích)
async def simulate_ai_monitoring(user_id, device_id=None, duration=None):
    """
    Mô phỏng AI theo dõi cây trồng và gửi cảnh báo nếu phát hiện vấn đề
    duration: Số giây mô phỏng (mặc định là None - chỉ chạy một lần)
    """
    try:
        if not device_id:
            device_id = f"device_{random.randint(100, 999)}"
            
        if duration:
            end_time = datetime.now() + timedelta(seconds=duration)
            while datetime.now() < end_time:
                await simulate_single_monitoring_event(user_id, device_id)
                await asyncio.sleep(random.randint(5, 15))  # Đợi 5-15 giây giữa các lần cảnh báo
        else:
            await simulate_single_monitoring_event(user_id, device_id)
            
        return {
            "success": True,
            "message": f"Mô phỏng theo dõi AI hoàn tất cho thiết bị {device_id}"
        }
        
    except Exception as e:
        logger.error(f"Lỗi khi mô phỏng theo dõi AI: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Không thể mô phỏng theo dõi AI"
        }

async def simulate_single_monitoring_event(user_id, device_id):
    """
    Mô phỏng một sự kiện theo dõi đơn lẻ
    """
    # Tạo dữ liệu cảm biến
    sensor_data = await generate_sensor_data(device_id)
    
    # Ngẫu nhiên quyết định có phát hiện vấn đề hay không
    if random.random() < 0.7:  # 70% cơ hội phát hiện vấn đề
        # Chọn ngẫu nhiên một vấn đề
        issue_type = random.choice([
            "temperature", "humidity", "soil_moisture", "pest", "disease"
        ])
        
        if issue_type == "temperature":
            if sensor_data["sensors"]["temperature"] > 32:
                issue = "Nhiệt độ quá cao"
                recommendation = "Tăng cường che phủ hoặc phun sương"
            else:
                issue = "Nhiệt độ quá thấp"
                recommendation = "Bảo vệ cây khỏi gió lạnh"
                
        elif issue_type == "humidity":
            issue = "Độ ẩm không khí bất thường"
            recommendation = "Điều chỉnh hệ thống tưới và thoát nước"
            
        elif issue_type == "soil_moisture":
            if sensor_data["sensors"]["soil_moisture"] < 30:
                issue = "Đất quá khô"
                recommendation = "Tăng cường tưới nước"
            else:
                issue = "Đất quá ẩm"
                recommendation = "Giảm tưới nước, cải thiện thoát nước"
                
        elif issue_type == "pest":
            issue = "Phát hiện dấu hiệu có sâu bệnh"
            recommendation = "Kiểm tra cây trồng và sử dụng biện pháp phòng trừ thích hợp"
            
        else:  # disease
            issue = "Phát hiện dấu hiệu bệnh hại"
            recommendation = "Kiểm tra và áp dụng biện pháp phòng trừ bệnh"
            
        # Tạo mức độ nghiêm trọng
        severity = random.choice(["Thấp", "Trung bình", "Cao", "Nghiêm trọng"])
        
        # Tạo tin nhắn cảnh báo
        message = f"[Cảnh báo {severity}] {issue} trên thiết bị {device_id}. {recommendation}."
        
        # Tạo payload để gửi qua WebSocket
        alert_payload = {
            "type": "ai_alert",
            "user_id": user_id,
            "device_id": device_id,
            "message": message,
            "alert": {
                "issue": issue,
                "severity": severity,
                "recommendation": recommendation,
                "sensor_data": sensor_data["sensors"],
                "timestamp": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Gửi cảnh báo qua WebSocket
        await broadcast_relay_update(alert_payload)
        
        logger.info(f"Đã gửi cảnh báo AI: {message}")