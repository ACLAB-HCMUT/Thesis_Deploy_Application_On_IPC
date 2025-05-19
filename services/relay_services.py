from databases.databases import *
from datetime import datetime
from constant.constant import nutnhan
import pytz
from schemas import RelayData
from pymongo  import DESCENDING
import requests
from bson import ObjectId
from datetime import datetime
import json
import time
import aio_pika
import json
import pytz
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

# Dictionary lưu thời gian request cuối cùng
request_timestamps = {}

# def service_update_relay(body):
#     data = body
#     email_user = data.get('email_user')  # Vẫn giữ để ghi log nếu cần
#     relay_name = data.get('relayName')
#     status_relay = data.get('status')
    
#     if relay_name not in nutnhan:
#         return {'message': 'Relay not in server', 'errCode': 1}, 400
    
#     vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
#     vietnam_time = datetime.now(vietnam_tz)
    
#     # Dữ liệu cập nhật không phụ thuộc email_user
#     data = {
#         'relayName': relay_name,
#         'status': status_relay,
#         'timestamp': vietnam_time,
#         'updated_by': email_user  # Lưu email_user như thông tin phụ
#     }
    
#     # Tìm relay dựa trên relayName duy nhất
#     relay = collection_relay.find_one({'relayName': relay_name})
#     collection_relay.insert_one(data)
#     # if relay is None:
#     #     # Tạo mới nếu chưa tồn tại
#     #     collection_relay.insert_one(data)
#     # else:
#     #     # Cập nhật trạng thái
#     #     query = {"relayName": relay_name}
#     #     new_values = {
#     #         "$set": {
#     #             "status": status_relay,
#     #             "timestamp": vietnam_time,
#     #             "updated_by": email_user
#     #         }
#     #     }
#     #     collection_relay.update_one(query, new_values)
    
#     # Gửi lệnh đến Core IOT
#     relay_number = "".join(char for char in relay_name if char.isdigit()) or "1"
#     core_iot_url = "https://app.coreiot.io/api/plugins/telemetry/DEVICE/21c4e8a0-f63f-11ef-a887-6d1a184f2bb5/SHARED_SCOPE"
#     core_iot_body = {
#         "method": f"setDataRelay{relay_number}",
#         "value": status_relay == "ON"
#     }
    
#     token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ2aW5oLm5ndXllbjEyM0BoY211dC5lZHUudm4iLCJ1c2VySWQiOiJjOWY5OGNmMC1lMTQ2LTExZWYtYWQwOS01MTVmNzkwZWQ5ZGYiLCJzY29wZXMiOlsiVEVOQU5UX0FETUlOIl0sInNlc3Npb25JZCI6ImU4MzU5YzgxLWQ2NmEtNDljYi05NjgyLWE3MTg0MDFlOTQ4YyIsImV4cCI6MTc0MjAyMDQzMSwiaXNzIjoiY29yZWlvdC5pbyIsImlhdCI6MTc0MjAxMTQzMSwiZmlyc3ROYW1lIjoiVklOSCIsImxhc3ROYW1lIjoiTkdVWeG7hE4gS0jhuq5DIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6ImM5ZTk4NzYwLWUxNDYtMTFlZi1hZDA5LTUxNWY3OTBlZDlkZiIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.mS-l5RJ-zRfHzJ237nGnnBNidf2KsQqnb0mgJWJtw8voOdkpMlOH3wuQvUtaKIV9qn8BZhr60E_DRrCzaDvp7w"
#     headers = {
#         "Content-Type": "application/json",
#         "X-Authorization": f"Bearer {token}"
#     }
    
#     max_retries = 2
#     for attempt in range(max_retries):
#         try:
#             response = requests.post(core_iot_url, headers=headers, json=core_iot_body)
#             if response.status_code == 401 and "Token has expired" in response.text:
#                 login_url = "https://app.coreiot.io/api/auth/login"
#                 login_body = {"username": "vinh.nguyen123@hcmut.edu.vn", "password": "Vinhnguyen1$"}
#                 login_response = requests.post(login_url, json=login_body)
#                 if login_response.status_code == 200:
#                     token = login_response.json().get('token')
#                     headers["X-Authorization"] = f"Bearer {token}"
#                     continue
#             if response.status_code == 200:
#                 print(f"Successfully sent command to Core IOT: {response.text}")
#                 break
#             else:
#                 print(f"Error sending command to Core IOT: {response.status_code}, {response.text}")
#         except Exception as e:
#             print(f"Exception when calling Core IOT API: {str(e)}")
#         if attempt < max_retries - 1:
#             time.sleep(1)
    
#     return {
#         'message': 'Relay update successful',
#         'data': {
#             'relayName': relay_name,
#             'status': status_relay,
#             'timestamp': vietnam_time,
#             'updated_by': email_user
#         }
#     }, 200
    
def service_get_relay(body):
    data = body
    relay_name = data.get('relayName')
    
    if relay_name not in nutnhan:
        return {'message': 'Relay not in server', 'errCode': 1}, 400
    
    # Trực tiếp tìm bản ghi có thời gian lớn nhất
    latest_relay = collection_relay.find(
        {'relayName': relay_name}
    ).sort('timestamp', -1).limit(1)
    
    latest_relay_doc = next(latest_relay, None)
    
    if latest_relay_doc is None:
        return {'message': 'Relay not in system', 'errCode': 1}, 400
    
    # Loại bỏ trường _id (nếu không muốn trả về)
    if '_id' in latest_relay_doc:
        latest_relay_doc.pop('_id')
    
    return {
        'message': 'Get Relay successful',
        'data': latest_relay_doc
    }, 200


def service_getAllStatus_relay(body):
    """
    Lấy trạng thái của tất cả các relay với cache thông minh
    """
    # Cache system - Simple in-memory cache
    if not hasattr(service_getAllStatus_relay, 'cache'):
        service_getAllStatus_relay.cache = {}
        
    cache = service_getAllStatus_relay.cache
    CACHE_TIMEOUT = 30  # 30 giây (có thể điều chỉnh theo nhu cầu)
    
    # Tạo key cache đơn giản
    current_time = datetime.now(timezone.utc)
    time_key = (current_time.second // 10) * 10  # Phân chia theo từng khoảng 10 giây
    cache_key = f"relay_status_{current_time.strftime('%Y-%m-%d_%H_%M')}_{time_key}"
    
    # Kiểm tra cache
    if cache_key in cache and time.time() - cache[cache_key]['time'] < CACHE_TIMEOUT:
        print(f"Using cached relay status for {cache_key}")
        return cache[cache_key]['data']
        
    print(f"Fetching latest relay status")
    
    try:
        relay_names = ['nutnhan1', 'nutnhan2', 'nutnhan3', 'nutnhan4']
        latest_relay_status = {}
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        
        for relay_name in relay_names:
            relay = collection_relay.find_one(
                {'relayName': relay_name},
                sort=[('timestamp', DESCENDING)]
            )
            
            if relay:
                if relay["timestamp"].tzinfo is None:
                    # Assume MongoDB timestamp is in UTC
                    utc_time = relay["timestamp"].replace(tzinfo=pytz.UTC)
                else:
                    utc_time = relay["timestamp"]
                    
                # Convert to Vietnam time
                vietnam_time = utc_time.astimezone(vietnam_tz)
                print(vietnam_time)
                
                latest_relay_status[relay_name] = {
                    'status': relay['status'],
                    'timestamp': vietnam_time.strftime("%Y-%m-%dT%H:%M:%S") 
                        if isinstance(relay["timestamp"], datetime) else relay["timestamp"],
                    'updated_by': relay.get('updated_by', 'Unknown')
                }
            else:
                latest_relay_status[relay_name] = {
                    'status': 'OFF',
                    'timestamp': None,
                    'updated_by': 'Unknown'
                }
        
        result = {
            'message': 'Get Relay successful',
            'data': latest_relay_status
        }, 200
        
        # Cập nhật cache
        cache[cache_key] = {
            'data': result,
            'time': time.time()
        }
        
        # Dọn dẹp cache cũ để tránh rò rỉ bộ nhớ
        for old_key in list(cache.keys()):
            if time.time() - cache[old_key]['time'] > CACHE_TIMEOUT * 3:
                del cache[old_key]
        
        return result
        
    except Exception as e:
        print(f"Error fetching relay status: {e}")
        return {
            'message': f'Error fetching relay status: {str(e)}',
            'data': {}
        }, 500

# Hàm để xóa cache khi có cập nhật trạng thái relay
def invalidate_relay_cache():
    """
    Gọi hàm này sau khi thay đổi trạng thái relay
    để đảm bảo lần gọi tiếp theo sẽ lấy dữ liệu mới
    """
    if hasattr(service_getAllStatus_relay, 'cache'):
        service_getAllStatus_relay.cache.clear()
        print("Relay status cache cleared")
    
def service_delete_relay(body):
    data = body
    relay_name = data.get('relayName')

    if relay_name not in nutnhan:
        return {'message': 'Relay not in server', 'errCode': 1}, 400
    
    relay = collection_relay.find_one({'relayName': relay_name})
    if relay is None:
        return {'message': 'Relay not in system', 'errCode': 1}, 400
    
    collection_relay.delete_one({'relayName': relay_name})
    return {
        'message': 'Delete Relay successful',
        'data': {'relayName': relay_name}
    }, 200

def service_create_relay(body):
    data = body
    email_user = data.get('email_user')
    relay_name = data.get('relayName')
    status_relay = data.get('status')

    if relay_name not in nutnhan:
        return {'message': 'Relay not in server', 'errCode': 1}, 400
    
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = datetime.now(vietnam_tz)
    
    data = {
        'relayName': relay_name,
        'status': status_relay,
        'timestamp': vietnam_time,
        'updated_by': email_user
    }

    relay = collection_relay.find_one({'relayName': relay_name})
    if relay:
        query = {"relayName": relay_name}
        new_values = {"$set": {'status': status_relay, "timestamp": vietnam_time, "updated_by": email_user}}
        collection_relay.update_one(query, new_values)
    else:
        collection_relay.insert_one(data)

    return {
        'message': 'Create Relay successful',
        'data': {
            'relayName': relay_name,
            'status': status_relay,
            'timestamp': vietnam_time,
            'updated_by': email_user
        }
    }, 200


# def service_get_relay_history(body):
#     data = body
#     relay_name = data.get('relayName')

#     if relay_name not in nutnhan:
#         return {'message': 'Relay not in server', 'errCode': 1}, 400
    
#     relayList = collection_relay.find({'relayName': relay_name})
#     relay_list_data = list(relayList)

#     vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
#     relay_data_list = [
#         {
#             "_id": str(relay["_id"]),
#             "relayName": relay["relayName"],
#             "email_user": relay.get("updated_by", "Unknown"),
#             "status": relay["status"],
#             # In service_get_relay_history, ensure timestamps are properly converted:
# "timestamp": relay["timestamp"].replace(tzinfo=pytz.UTC).astimezone(vietnam_tz).isoformat() if isinstance(relay["timestamp"], datetime) else relay["timestamp"],
#         }
#         for relay in relay_list_data
#     ]
        
#     return {
#         'message': 'Get Relay successful',
#         'data': relay_data_list
#     }, 200

def service_delete_relay_history(body):
    data = body
    history_id = data.get('history_id')  # ID của bản ghi lịch sử cần xóa

    if not history_id:
        return {'message': 'Missing history_id', 'errCode': 1}, 400

    try:
        # Chuyển history_id thành ObjectId để tìm trong MongoDB
        result = collection_relay.delete_one({'_id': ObjectId(history_id)})
        if result.deleted_count == 0:
            return {'message': 'History record not found', 'errCode': 1}, 404
        
        return {
            'message': 'Delete relay history successful',
            'data': {'history_id': history_id}
        }, 200
    except Exception as e:
        return {'message': f'Error deleting history: {str(e)}', 'errCode': 1}, 500
def service_delete_all_relay_history(body):
    data = body
    relay_name = data.get('relayName')

    if not relay_name:
        return {'message': 'Missing relayName', 'errCode': 1}, 400

    if relay_name not in nutnhan:
        return {'message': 'Relay not in server', 'errCode': 1}, 400

    try:
        result = collection_relay.delete_many({'relayName': relay_name})
        if result.deleted_count == 0:
            return {'message': 'No history records found for this relay', 'errCode': 1}, 404
        
        return {
            'message': 'Delete all relay history successful',
            'data': {'relayName': relay_name, 'deleted_count': result.deleted_count}
        }, 200
    except Exception as e:
        return {'message': f'Error deleting all history: {str(e)}', 'errCode': 1}, 500

# Hàm lưu scheduler
def service_create_scheduler(body):
    data = body
    email = data.get('email')
    relay_name = data.get('relayName')
    time_start = data.get('timeStart')
    time_end = data.get('timeEnd')
    repeat_daily = data.get('repeatDaily') 
    if relay_name not in nutnhan:
        return {'message': 'Relay not in server', 'errCode': 1}, 400

    if not email or not time_start or not time_end:
        return {'message': 'Missing required fields', 'errCode': 1}, 400

    scheduler_data = {
        'email': email,
        'relayName': relay_name,
        'timeStart': time_start,
        'timeEnd': time_end,
        'repeatDaily': repeat_daily
    }

    result = collection_setup_scheduler.insert_one(scheduler_data)
    return {
        'message': 'Scheduler created successfully',
        'data': {
            'id': str(result.inserted_id),
            'email': email,
            'relayName': relay_name,
            'timeStart': time_start,
            'timeEnd': time_end,
            'repeatDaily': repeat_daily
        }
    }, 201
# Hàm lấy tất cả scheduler
def service_get_all_schedulers():
    schedulers = list(collection_setup_scheduler.find())
    scheduler_list = [
        {
            'id': str(scheduler['_id']),
            'email': scheduler['email'],
            'relayName': scheduler['relayName'],
            'timeStart': scheduler['timeStart'],
            'timeEnd': scheduler['timeEnd'],
            'repeatDaily': scheduler['repeatDaily']
        }
        for scheduler in schedulers
    ]
    return {
        'message': 'Get all schedulers successful',
        'data': scheduler_list
    }, 200

# Hàm xóa scheduler
def service_delete_scheduler(body):
    data = body
    scheduler_id = data.get('id')

    if not scheduler_id:
        return {'message': 'Missing scheduler_id', 'errCode': 1}, 400

    try:
        result = collection_setup_scheduler.delete_one({'_id': ObjectId(scheduler_id)})
        if result.deleted_count == 0:
            return {'message': 'Scheduler not found', 'errCode': 1}, 404
        
        return {
            'message': 'Delete scheduler successful',
            'data': {'scheduler_id': scheduler_id}
        }, 200
    except Exception as e:
        return {'message': f'Error deleting scheduler: {str(e)}', 'errCode': 1}, 500
    

    # Hàm kiểm tra và tự động bật/tắt relay theo scheduler
# Hàm kiểm tra và tự động bật/tắt relay theo scheduler
def service_check_and_update_relay():
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(vietnam_tz)
    print(f"Running service_check_and_update_relay at {current_time}")

    schedulers = collection_setup_scheduler.find()
    for scheduler in schedulers:
        relay_name = scheduler['relayName']
        
        # Chuẩn hóa thời gian từ scheduler
        try:
            start_time = datetime.fromisoformat(scheduler['timeStart'].replace('Z', '+07:00')).astimezone(vietnam_tz)
            end_time = datetime.fromisoformat(scheduler['timeEnd'].replace('Z', '+07:00')).astimezone(vietnam_tz)
        except Exception as e:
            print(f"Error processing time for scheduler {scheduler['_id']}: {str(e)}")
            continue

        repeat_daily = scheduler.get('repeatDaily', False)
        should_turn_on = False
        should_turn_off = False

        if repeat_daily:
            # So sánh giờ và phút cho lịch lặp lại hàng ngày
            current_hour_min = current_time.hour * 60 + current_time.minute
            start_hour_min = start_time.hour * 60 + start_time.minute
            end_hour_min = end_time.hour * 60 + end_time.minute
            
            if start_hour_min <= end_hour_min:
                should_turn_on = start_hour_min <= current_hour_min <= end_hour_min
                should_turn_off = current_hour_min < start_hour_min or current_hour_min > end_hour_min
            else:
                should_turn_on = current_hour_min >= start_hour_min or current_hour_min <= end_hour_min
                should_turn_off = end_hour_min < current_hour_min < start_hour_min
        else:
            # So sánh toàn bộ thời gian cho lịch không lặp lại
            should_turn_on = start_time <= current_time <= end_time
            should_turn_off = current_time > end_time
            
            if should_turn_off:
                try:
                    collection_setup_scheduler.delete_one({'_id': scheduler['_id']})
                    print(f"One-time scheduler {scheduler['_id']} deleted as it has expired")
                except Exception as e:
                    print(f"Failed to delete scheduler {scheduler['_id']}: {str(e)}")

        latest_relay = collection_relay.find_one({'relayName': relay_name}, sort=[('timestamp', -1)])
        current_status = latest_relay.get('status') if latest_relay else 'OFF'

        if should_turn_on and current_status != 'ON':
            _update_relay_status(relay_name, 'ON', current_time, scheduler.get('email', 'Scheduler'))
        elif should_turn_off and current_status != 'OFF':
            _update_relay_status(relay_name, 'OFF', current_time, scheduler.get('email', 'Scheduler'))

def _update_relay_status(relay_name, status, timestamp, updated_by):
    data = {
        'relayName': relay_name,
        'status': status,
        'timestamp': timestamp.isoformat(),
        'updated_by': updated_by
    }
    collection_relay.insert_one(data)
    
    relay_number = "".join(char for char in relay_name if char.isdigit()) or "1"
    core_iot_url = "https://app.coreiot.io/api/plugins/telemetry/DEVICE/21c4e8a0-f63f-11ef-a887-6d1a184f2bb5/SHARED_SCOPE"
    core_iot_body = {
        "method": f"setDataRelay{relay_number}",
        "value": status == "ON"
    }
    
    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ2aW5oLm5ndXllbjEyM0BoY211dC5lZHUudm4iLCJ1c2VySWQiOiJjOWY5OGNmMC1lMTQ2LTExZWYtYWQwOS01MTVmNzkwZWQ5ZGYiLCJzY29wZXMiOlsiVEVOQU5UX0FETUlOIl0sInNlc3Npb25JZCI6ImU4MzU5YzgxLWQ2NmEtNDljYi05NjgyLWE3MTg0MDFlOTQ4YyIsImV4cCI6MTc0MjAyMDQzMSwiaXNzIjoiY29yZWlvdC5pbyIsImlhdCI6MTc0MjAxMTQzMSwiZmlyc3ROYW1lIjoiVklOSCIsImxhc3ROYW1lIjoiTkdVWeG7hE4gS0jhuq5DIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6ImM5ZTk4NzYwLWUxNDYtMTFlZi1hZDA5LTUxNWY3OTBlZDlkZiIsImN1c3RvbWVySWQiOiIxMzg1NDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.mS-l5RJ-zRfHzJ237nGnnBNidf2KsQqnb0mgJWJtw8voOdkpMlOH3wuQvUtaKIV9qn8BZhr60E_DRrCzaDvp7w"
    headers = {
        "Content-Type": "application/json",
        "X-Authorization": f"Bearer {token}"
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
                    headers["X-Authorization"] = f"Bearer {token}"
                    continue
            if response.status_code == 200:
                print(f"Successfully set relay {relay_name} to {status} via Core IOT")
                break
            else:
                print(f"Error sending command to Core IOT: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Exception when calling Core IOT API: {str(e)}")
        if attempt < max_retries - 1:
            time.sleep(1)


async def service_update_relay(body):
    data = body
    email_user = data.get('email_user')
    relay_name = data.get('relayName')
    status_relay = data.get('status')
    
    # Rate limiting
    rate_limit_key = f"{email_user}:{relay_name}"
    current_time = datetime.now()
    last_request = request_timestamps.get(rate_limit_key)
    
    if last_request and (current_time - last_request) < timedelta(seconds=1):
        return {
            'message': 'Too many requests. Please wait 1 second before trying again.',
            'errCode': 1
        }, 429
    
    request_timestamps[rate_limit_key] = current_time
    
    # Kiểm tra relay hợp lệ
    if relay_name not in nutnhan:
        return {
            'message': 'Relay not in server',
            'errCode': 1
        }, 400
    
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = datetime.now(vietnam_tz)
    
    # Dữ liệu relay
    relay_data = {
        'relayName': relay_name,
        'email_user': email_user,
        'status': status_relay,
        'timestamp': vietnam_time.isoformat(),
        'updated_by': email_user
    }
    
    # Dữ liệu Core IOT
    relay_number = relay_name.split("nutnhan")
    core_iot_data = {
        'method': f"setDataRelay{relay_number[1]}",
        'value': status_relay == "ON",
        'relayName': relay_name,
        'email_user': email_user,
        'timestamp': vietnam_time.isoformat()
    }
    
    # Gửi relay data vào RabbitMQ
    RELAY_QUEUE_NAME = "relay_data_queue"
    try:
        connection = await aio_pika.connect_robust(f"amqp://guest:guest@{RABBITMQ_HOST}/")
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(RELAY_QUEUE_NAME, durable=True)
            
            message = json.dumps(relay_data)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode(), delivery_mode=2),
                routing_key=RELAY_QUEUE_NAME
            )
            print(f"Sent relay data to RabbitMQ: {message}")
    except Exception as e:
        raise Exception(f"Failed to send relay data to RabbitMQ: {str(e)}")
    
    # Gửi Core IOT data vào RabbitMQ
    CORE_IOT_QUEUE_NAME = "core_iot_queue"
    try:
        connection = await aio_pika.connect_robust(f"amqp://guest:guest@{RABBITMQ_HOST}/")
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(CORE_IOT_QUEUE_NAME, durable=True)
            
            message = json.dumps(core_iot_data)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode(), delivery_mode=2),
                routing_key=CORE_IOT_QUEUE_NAME
            )
            print(f"Sent Core IOT data to RabbitMQ: {message}")
    except Exception as e:
        raise Exception(f"Failed to send Core IOT data to RabbitMQ: {str(e)}")
    
    return {
        'message': 'Relay update successful',
        'data': {
            'relayName': relay_name,
            'status': status_relay,
            'timestamp': vietnam_time.isoformat(),
            'updated_by': email_user
        }
    }, 200

def service_get_relay_history(body):
    data = body
    relay_name = data.get('relayName')

    if relay_name not in nutnhan:
        return {'message': 'Relay not in server', 'errCode': 1}, 400
    
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    relay_list = collection_relay.find({'relayName': relay_name}).sort('timestamp', -1)
    relay_data_list = []

    for relay in relay_list:
        timestamp = relay['timestamp']
        
        # Nếu timestamp là string, chuyển thành datetime với múi giờ
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp)
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=vietnam_tz)
            except Exception as e:
                print(f"Error parsing timestamp string: {str(e)}")
                continue
        # Nếu timestamp là datetime nhưng không có múi giờ, thêm múi giờ Việt Nam
        elif isinstance(timestamp, datetime) and timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=vietnam_tz)
        
        # Chuyển đổi sang giờ Việt Nam
        vietnam_time = timestamp.astimezone(vietnam_tz)
        
        relay_data = {
            '_id': str(relay['_id']),
            'relayName': relay['relayName'],
            'email_user': relay.get('updated_by', 'Unknown'),
            'status': relay['status'],
            'timestamp': vietnam_time.isoformat()  # Trả về ISO với múi giờ
        }
        relay_data_list.append(relay_data)
    
    if not relay_data_list:
        return {'message': 'No history found for this relay', 'errCode': 1}, 404
    
    return {
        'message': 'Get Relay successful',
        'data': relay_data_list
    }, 200

def service_get_relay_history_test(body):
    """
    Lấy lịch sử của relay với cache 1 phút
    """
    # Cache system - Simple in-memory cache
    if not hasattr(service_get_relay_history_test, 'cache'):
        service_get_relay_history_test.cache = {}
        
    cache = service_get_relay_history_test.cache
    CACHE_TIMEOUT = 60  # 1 phút
    
    data = body
    relay_name = data.get('relayName')
    
    if relay_name not in nutnhan:
        return {'message': 'Relay not in server', 'errCode': 1}, 400
    
    # Tạo cache key dựa trên relay_name và thời gian theo phút
    current_time = datetime.now(timezone.utc)
    time_key = (current_time.hour * 60) + current_time.minute  # Tính theo phút trong ngày
    cache_key = f"relay_history_{relay_name}_{current_time.strftime('%Y-%m-%d')}_{time_key}"
    
    # Kiểm tra cache
    if cache_key in cache and time.time() - cache[cache_key]['time'] < CACHE_TIMEOUT:
        print(f"Using cached relay history for {relay_name}")
        return cache[cache_key]['data']
    
    print(f"Fetching relay history for {relay_name}")
    
    try:
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        relay_list = collection_relay.find({'relayName': relay_name}).sort('timestamp', -1)
        relay_data_list = []
        
        for relay in relay_list:
            timestamp = relay['timestamp']
            
            # Nếu timestamp là string, chuyển thành datetime với múi giờ
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp)
                    if timestamp.tzinfo is None:
                        timestamp = timestamp.replace(tzinfo=vietnam_tz)
                except Exception as e:
                    print(f"Error parsing timestamp string: {str(e)}")
                    continue
            # Nếu timestamp là datetime nhưng không có múi giờ, thêm múi giờ Việt Nam
            elif isinstance(timestamp, datetime) and timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=vietnam_tz)
            
            # Chuyển đổi sang giờ Việt Nam
            vietnam_time = timestamp.astimezone(vietnam_tz)
            
            relay_data = {
                '_id': str(relay['_id']),
                'relayName': relay['relayName'],
                'email_user': relay.get('updated_by', 'Unknown'),
                'status': relay['status'],
                'timestamp': vietnam_time.isoformat()  # Trả về ISO với múi giờ
            }
            relay_data_list.append(relay_data)
        
        if not relay_data_list:
            result = {'message': 'No history found for this relay', 'errCode': 1}, 404
        else:
            result = {
                'message': 'Get Relay successful',
                'data': relay_data_list
            }, 200
        
        # Cập nhật cache
        cache[cache_key] = {
            'data': result,
            'time': time.time()
        }
        
        # Dọn dẹp cache cũ để tránh rò rỉ bộ nhớ
        for old_key in list(cache.keys()):
            if time.time() - cache[old_key]['time'] > CACHE_TIMEOUT * 3:  # Giữ cache trong 3 phút
                del cache[old_key]
        
        return result
        
    except Exception as e:
        print(f"Error fetching relay history: {e}")
        return {
            'message': f'Error fetching relay history: {str(e)}',
            'errCode': 1
        }, 500

# Hàm để xóa cache khi có cập nhật trạng thái relay
def invalidate_relay_history_cache(relay_name=None):
    """
    Gọi hàm này sau khi thay đổi trạng thái relay để đảm bảo lấy dữ liệu mới
    
    Parameters:
    relay_name (str, optional): Tên relay cụ thể cần xóa cache. Nếu None, xóa tất cả cache.
    """
    if hasattr(service_get_relay_history_test, 'cache'):
        if relay_name:
            # Xóa cache liên quan đến relay_name cụ thể
            keys_to_remove = []
            for key in service_get_relay_history_test.cache.keys():
                if f"relay_history_{relay_name}_" in key:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del service_get_relay_history_test.cache[key]
            print(f"Cleared cache for relay {relay_name}")
        else:
            # Xóa tất cả cache
            service_get_relay_history_test.cache.clear()
            print("Cleared all relay history cache")