# routes/ai_simulator_routes.py
from fastapi import APIRouter, Request, BackgroundTasks
from controller.ai_simulator_controller import (
    simulate_ai_analysis, 
    simulate_ai_monitoring,
    handle_custom_predict,
    handle_custom_monitor_single
)
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/predict")
async def trigger_ai_prediction(request: Request):
    """
    Endpoint để kích hoạt một dự đoán AI đơn lẻ
    """
    try:
        body = await request.json()
        user_id = body.get("user_id")
        
        if not user_id:
            return {
                "success": False,
                "error": "Missing user_id"
            }
        
        # Sử dụng hàm handle_custom_predict thay vì simulate_ai_analysis
        result = await handle_custom_predict(body)
        return result
        
    except Exception as e:
        logger.error(f"Error triggering AI prediction: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to trigger AI prediction"
        }

@router.post("/monitor/single")
async def trigger_ai_monitoring_single(request: Request):
    """
    Endpoint để kích hoạt một sự kiện giám sát AI đơn lẻ
    """
    try:
        body = await request.json()
        user_id = body.get("user_id")
        
        if not user_id:
            return {
                "success": False,
                "error": "Missing user_id"
            }
        
        # Sử dụng hàm handle_custom_monitor_single thay vì simulate_ai_monitoring
        result = await handle_custom_monitor_single(body)
        return result
        
    except Exception as e:
        logger.error(f"Error triggering AI monitoring: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to trigger AI monitoring"
        }

@router.post("/monitor/continuous")
async def trigger_ai_monitoring_continuous(request: Request, background_tasks: BackgroundTasks):
    """
    Endpoint để kích hoạt nhiều sự kiện giám sát AI trong một khoảng thời gian
    """
    try:
        body = await request.json()
        user_id = body.get("user_id")
        device_id = body.get("device_id", None)
        duration = body.get("duration", 60)  # Thời gian theo dõi (giây), mặc định 60s
        
        if not user_id:
            return {
                "success": False,
                "error": "Missing user_id"
            }
            
        # Thực hiện giám sát trong background để không chặn response
        background_tasks.add_task(simulate_ai_monitoring, user_id, device_id, duration)
        
        return {
            "success": True,
            "message": f"Bắt đầu giám sát liên tục cho thiết bị trong {duration} giây"
        }
        
    except Exception as e:
        logger.error(f"Error triggering continuous AI monitoring: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to trigger continuous AI monitoring"
        }