# simple_notifications_routes.py
from fastapi import APIRouter, Request
from controller.simple_notification_controller import predict_harvest
# from controller.simple_notification_controller import predict_harvest, manage_prediction_scheduler
router = APIRouter()

@router.post("/predict_harvest")
async def api_predict_harvest(request: Request):
    """
    Endpoint đơn giản để test dự đoán thu hoạch
    """
    body = await request.json()
    return await predict_harvest(body)

@router.post("/predict")
async def api_ai_simulator_predict(request: Request):
    """
    Endpoint mới cho AI simulator predict với các trường mới
    """
    body = await request.json()
    return await predict_harvest(body)
# @router.post("/scheduler/{action}")
# async def api_manage_scheduler(action: str):
#     """
#     Endpoint để quản lý scheduler tự động dự đoán
#     """
#     return await manage_prediction_scheduler(action)