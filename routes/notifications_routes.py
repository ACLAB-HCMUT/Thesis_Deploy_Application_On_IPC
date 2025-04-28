# # app/routes/notifications.py

# from fastapi import APIRouter, Depends, Request, HTTPException, status, Body, WebSocket
# from controller.notification_controller import predict_harvest, controller_create_notification, controller_get_notifications, controller_mark_as_seen
# from fastapi.security import OAuth2PasswordBearer
# from typing import Dict, Any, List

# from controller.notification_controller import predict_harvest
# router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


# #test AI notification


# @router.post("/create")
# async def create_notification(request: Request, token: str = Depends(oauth2_scheme)):
#     body = await request.json()
#     return await controller_create_notification(body, token)

# @router.get("/user/{user_id}")
# async def get_notifications(user_id: int, token: str = Depends(oauth2_scheme)):
#     return await controller_get_notifications(user_id, token)

# @router.patch("/mark_as_seen/{user_id}/{notification_id}")
# async def mark_as_seen(user_id: int, notification_id: int, token: str = Depends(oauth2_scheme)):
#     return await controller_mark_as_seen(user_id, notification_id, token)


# # Thêm endpoint dự đoán ngày thu hoạch
# @router.post("/predict_harvest")
# async def api_predict_harvest(request: Request):
#     body = await request.json()
#     return await predict_harvest(body)