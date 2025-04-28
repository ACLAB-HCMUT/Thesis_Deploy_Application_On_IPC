from authenticate.jwt_handler import verify_jwt_token
from services.relay_services import (service_update_relay, service_create_relay, service_get_relay,
service_delete_relay, service_get_relay_history, 
service_getAllStatus_relay, service_delete_relay_history, 
service_delete_all_relay_history,service_create_scheduler,
    service_get_all_schedulers, service_delete_scheduler,
    service_check_and_update_relay)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Query
# Update relay status
def controller_update_relay(body):
# Xác thực token
    try:
        # Truy vấn tất cả các document trong collection
        # payload = verify_jwt_token(token)
        data, status = service_update_relay(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

# Get relay status
def controller_get_relay(body):
# Xác thực token
    try:
        # Truy vấn tất cả các document trong collection
        # payload = verify_jwt_token(token)
        data, status = service_get_relay(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

# Get all relay statuses (updated to use query parameter)

def controller_getAllStatus_relay(body):
    try:
        data, status = service_getAllStatus_relay(body)
        response = {
            "message": data.get('message', 'Get all relay status successful'),
            "data": jsonable_encoder(data.get('data', {})),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
# Get relay status
def controller_delete_relay(body):
# Xác thực token
    try:
        # Truy vấn tất cả các document trong collection
        # payload = verify_jwt_token(token)
        data, status = service_delete_relay(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500


# Create new relay
def controller_create_relay(body):
# Xác thực token
    try:
        # Truy vấn tất cả các document trong collection
        # verify_jwt_token(token)
        data, status = service_create_relay(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def controller_get_relay_history(body):
    # Xác thực token
    try:
        # Truy vấn tất cả các document trong collection
        # verify_jwt_token(token)
        data, status = service_get_relay_history(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    
def controller_delete_relay_history(body):
    try:
        data, status = service_delete_relay_history(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
def controller_delete_all_relay_history(body):
    try:
        data, status = service_delete_all_relay_history(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
def controller_delete_scheduler(body):
    try:
        data, status = service_delete_scheduler(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    
# Create scheduler
def controller_create_scheduler(body):
    try:
        data, status = service_create_scheduler(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
# Get all schedulers
def controller_get_all_schedulers():
    try:
        data, status = service_get_all_schedulers()
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
# Delete scheduler
def controller_delete_scheduler(body):
    try:
        data, status = service_delete_scheduler(body)
        response = {
            "message": data.get('message'),
            "data": jsonable_encoder(data.get('data')),
            "status": status,
            "errCode": 0
        }
        return JSONResponse(content=response, status_code=status)
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500

# Check and update relay based on scheduler
def controller_check_and_update_relay():
    try:
        service_check_and_update_relay()
        return {
            "message": "Checked and updated relays based on schedulers",
            "status": 200,
            "errCode": 0
        }, 200
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500