from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import JSONResponse
from controller.relay_controller import (
    controller_update_relay,
    controller_create_relay,
    controller_get_relay,
    controller_delete_relay,
    controller_get_relay_history,
    controller_getAllStatus_relay,
    controller_delete_relay_history,
    controller_delete_all_relay_history,
    controller_create_scheduler,
    controller_get_all_schedulers,
    controller_delete_scheduler,
    controller_check_and_update_relay,
    controller_get_relay_history_test
)
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from middleware.websocket_manager import broadcast_relay_update
import json

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

async def get_all_status_for_broadcast(email_user: str):
    try:
        response = controller_getAllStatus_relay({"email_user": email_user})
        if isinstance(response, JSONResponse):
            return json.loads(response.body.decode('utf-8'))
        elif isinstance(response, tuple) and response[1] == 200:
            return response[0]
        return None
    except Exception as e:
        print(f"Error fetching all status for broadcast: {e}")
        return None

# gui tat ca trang thai thay doi cua cac relay
# @router.post("/update")
# async def update_relay_data(request: Request):
#     body = await request.json()
#     response = controller_update_relay(body)
    
#     if isinstance(response, JSONResponse):
#         if response.status_code == 200:
#             response_data = json.loads(response.body.decode('utf-8'))
#             all_status_response = await get_all_status_for_broadcast(body.get("email_user"))
#             print("All status response for broadcast:", all_status_response)
#             if all_status_response and all_status_response.get("data"):
#                 print("Broadcasting update to WebSocket clients")
#                 await broadcast_relay_update(all_status_response)
#         return response
#     else:
#         response_dict, status_code = response
#         if status_code == 200:
#             all_status_response = await get_all_status_for_broadcast(body.get("email_user"))
#             print("All status response for broadcast:", all_status_response)
#             if all_status_response and all_status_response.get("data"):
#                 print("Broadcasting update to WebSocket clients")
#                 await broadcast_relay_update(all_status_response)
#         return JSONResponse(content=response_dict, status_code=status_code)
@router.post("/update")
async def update_relay_data(request: Request):
    body = await request.json()
    response = await controller_update_relay(body)
    
    if isinstance(response, JSONResponse):
        if response.status_code == 200:
            response_data = json.loads(response.body.decode('utf-8'))
            # Định dạng dữ liệu để phù hợp với frontend
            relay_name = response_data["data"]["relayName"]
            broadcast_data = {
                "message": "Relay update successful",
                "data": {
                    relay_name: {
                        "status": response_data["data"]["status"],
                        "timestamp": response_data["data"]["timestamp"],
                        "updated_by": response_data["data"]["updated_by"]
                    }
                }
            }
            print("Broadcasting update for single relay:", broadcast_data)
            await broadcast_relay_update(broadcast_data)
        return response
    else:
        response_dict, status_code = response
        if status_code == 200:
            # Định dạng dữ liệu để phù hợp với frontend
            relay_name = response_dict["data"]["relayName"]
            broadcast_data = {
                "message": "Relay update successful",
                "data": {
                    relay_name: {
                        "status": response_dict["data"]["status"],
                        "timestamp": response_dict["data"]["timestamp"],
                        "updated_by": response_dict["data"]["updated_by"]
                    }
                }
            }
            print("Broadcasting update for single relay:", broadcast_data)
            
            await broadcast_relay_update(broadcast_data)
        return JSONResponse(content=response_dict, status_code=status_code)
    
@router.get("/getStatus")
async def get_relay_data(request: Request):
    body = await request.json()
    return controller_get_relay(body)

@router.get("/getAllStatus")
async def get_all_relay_data(email_user: str):
    return controller_getAllStatus_relay({"email_user": email_user})

@router.get("/getHistory")
async def get_relay_data_history(request: Request):
    body = await request.json()
    return controller_get_relay_history(body)

@router.get("/getHistoryTest")
async def get_relay_data_history_test(nut_nhan: str):
    return controller_get_relay_history_test({"relayName": nut_nhan})

@router.post("/deleteHistory")
async def delete_relay_history(request: Request):
    body = await request.json()
    return controller_delete_relay_history(body)
@router.post("/deleteAllHistory")
async def delete_all_relay_history(request: Request):
    body = await request.json()
    return controller_delete_all_relay_history(body)

@router.post("/create")
async def create_relay_data(request: Request):
    body = await request.json()
    return controller_create_relay(body)

@router.delete("/delete")
async def delete_relay_data(request: Request):
    body = await request.json()
    response = controller_delete_relay(body)
    
    if isinstance(response, JSONResponse):
        if response.status_code == 200:
            all_status_response = await get_all_status_for_broadcast(body.get("email_user"))
            if all_status_response and all_status_response.get("data"):
                await broadcast_relay_update(all_status_response)
        return response
    else:
        response_dict, status_code = response
        if status_code == 200:
            all_status_response = await get_all_status_for_broadcast(body.get("email_user"))
            if all_status_response and all_status_response.get("data"):
                await broadcast_relay_update(all_status_response)
        return JSONResponse(content=response_dict, status_code=status_code)
@router.post("/scheduler")
async def create_scheduler(request: Request):
    body = await request.json()
    response = controller_create_scheduler(body)
    
    if isinstance(response, JSONResponse):
        return response
    else:
        response_dict, status_code = response
        return JSONResponse(content=response_dict, status_code=status_code)

@router.get("/scheduler")
async def get_all_schedulers():
    response = controller_get_all_schedulers()
    
    if isinstance(response, JSONResponse):
        return response
    else:
        response_dict, status_code = response
        return JSONResponse(content=response_dict, status_code=status_code)

@router.delete("/scheduler")
async def delete_scheduler(request: Request):
    body = await request.json()
    response = controller_delete_scheduler(body)
    
    if isinstance(response, JSONResponse):
        return response
    else:
        response_dict, status_code = response
        return JSONResponse(content=response_dict, status_code=status_code)

