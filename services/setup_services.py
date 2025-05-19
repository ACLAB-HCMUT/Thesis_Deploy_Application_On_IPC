from databases.databases import *
from datetime import datetime
from constant.constant import nutnhan
import json
import pytz
import time
from bson import ObjectId
from datetime import datetime
from pytz import timezone
import aio_pika
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

# Service cho API /setup/scheduler
async def service_create_setup_scheduler(body):
    data = body
    
    email_user = data.get('email')
    relay_name = data.get('relayName')
    time_start = data.get('timeStart')
    time_end = data.get('timeEnd')
    repeat_daily = data.get('repeatDaily')
    
    # Kiểm tra user tồn tại
    if collection_user.count_documents({"email": email_user}) == 0:
        return {
            'message': 'User was not registed',
            'data': []
        }, 200
    
    # Kiểm tra định dạng datetime
    try:
        start_datetime = datetime.fromisoformat(time_start)
        end_datetime = datetime.fromisoformat(time_end)
    except ValueError:
        return {
            'message': 'Invalid datetime format. Please use YYYY-MM-DDTHH:MM:SS format',
            'data': []
        }, 400
    
    # Kiểm tra xung đột thời gian
    existing_schedules = collection_setup_scheduler.find({'relayName': relay_name})
    
    for schedule in existing_schedules:
        existing_start = datetime.fromisoformat(schedule['timeStart'])
        existing_end = datetime.fromisoformat(schedule['timeEnd'])
        
        # Kiểm tra overlap
        if (start_datetime < existing_end and end_datetime > existing_start):
            recommended_start = existing_end.strftime("%Y-%m-%dT%H:%M:%S")
            recommended_end = end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            return {
                'message': 'Time conflict detected',
                'data': {
                    'conflict': True,
                    'conflicting_schedule': {
                        'timeStart': schedule['timeStart'],
                        'timeEnd': schedule['timeEnd']
                    },
                    'recommendation': f'You should schedule from {recommended_start} to {recommended_end}'
                }
            }, 409
    
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = datetime.now(vietnam_tz)
    
    # Dữ liệu scheduler
    scheduler_data = {
        'email': email_user,
        'relayName': relay_name,
        'timeStart': time_start,
        'timeEnd': time_end,
        'timestamp': vietnam_time.isoformat(),
        'repeatDaily': repeat_daily
    }
    
    # Dữ liệu Core IOT
    inserted_id = "temp_id"  # Sẽ được cập nhật sau khi lưu vào MongoDB
    core_iot_data = {
        'scheduler': f'0_{inserted_id}_{relay_name}_{time_start}_{time_end}_{int(repeat_daily)}',
        'timestamp': vietnam_time.isoformat()
    }
    
    # Gửi scheduler data vào RabbitMQ
    SCHEDULER_QUEUE_NAME = "scheduler_data_queue"
    try:
        connection = await aio_pika.connect_robust(f"amqp://guest:guest@{RABBITMQ_HOST}/")
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(SCHEDULER_QUEUE_NAME, durable=True)
            
            message = json.dumps(scheduler_data)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode(), delivery_mode=2),
                routing_key=SCHEDULER_QUEUE_NAME
            )
            print(f"Sent scheduler data to RabbitMQ: {message}")
    except Exception as e:
        raise Exception(f"Failed to send scheduler data to RabbitMQ: {str(e)}")
    
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
        'message': 'Create scheduler successful',
        'data': {
            'email': email_user,
            'relayName': relay_name,
            'timeStart': time_start,
            'timeEnd': time_end,
            'repeatDaily': repeat_daily,
            'timestamp': vietnam_time.isoformat()
        }
    }, 200

def service_get_setup_scheduler():
    # Lấy tất cả dữ liệu từ MongoDB
    schedulerList = list(collection_setup_scheduler.find())  # ✅ Convert Cursor thành list

    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

    # Kiểm tra nếu không có dữ liệu
    if not schedulerList:  
        return {
            'message': 'No scheduler found in system', 
            'errCode': 1
        }, 400
    
    # Chuyển đổi dữ liệu thành danh sách dictionary
    scheduler_data_list = [
        {
            "id": str(scheduler["_id"]),
            "relayName": scheduler["relayName"],
            "timeStart": scheduler["timeStart"],
            "timeEnd": scheduler["timeEnd"],
            "timestamp": (
                # Nếu timestamp là datetime object
                (
                    # Nếu timestamp đã có timezone info
                    scheduler["timestamp"].astimezone(vietnam_tz) if scheduler["timestamp"].tzinfo
                    # Nếu timestamp không có timezone info, giả định là UTC
                    else pytz.UTC.localize(scheduler["timestamp"]).astimezone(vietnam_tz)
                ).strftime("%Y-%m-%dT%H:%M:%S")
                if isinstance(scheduler["timestamp"], datetime)
                else scheduler["timestamp"]
            ),
        }
        for scheduler in schedulerList
    ]
    print(scheduler_data_list)

    return {
        'message': 'Get Scheduler successful',
        'data': scheduler_data_list
    }, 200

def service_get_setup_scheduler_ByID(body):
    # Lấy tất cả dữ liệu từ MongoDB
    data = body

    id = data.get('id')

    object_id = ObjectId(id)

    scheduler = collection_setup_scheduler.find_one({'_id': object_id})  # ✅ Convert Cursor thành list

    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

    # Kiểm tra nếu không có dữ liệu
    if not scheduler:  
        return {
            'message': 'No scheduler found in system', 
            'errCode': 1
        }, 400
    
    if scheduler["timestamp"].tzinfo is None:
        # Assume MongoDB timestamp is in UTC
        utc_time = scheduler["timestamp"].replace(tzinfo=pytz.UTC)
    else:
        utc_time = scheduler["timestamp"]

    # Convert to Vietnam time
    vietnam_time = utc_time.astimezone(vietnam_tz)
    print(vietnam_time)

    return {
        'message': 'Get scheduler By ID successful',
        'data': {
            'email': scheduler["email"],
            'relayName': scheduler["relayName"],
            'timeStart': scheduler["timeStart"],
            'timeEnd': scheduler["timeEnd"],
            'timestamp': vietnam_time.strftime("%Y-%m-%dT%H:%M:%S") 
                if isinstance(scheduler["timestamp"], datetime) else scheduler["timestamp"]
        }
    }, 200


def service_update_setup_scheduler(body):
    # Lấy tất cả dữ liệu từ MongoDB
    if not body.get('id') or not body.get('email'):
        return {
            'message': 'Email or ID_Device is required', 
            'errCode': 1
        }, 400

    id = body.get('id')
    email = body.get('email')
    timeStart = body.get('timeStart')
    timeEnd = body.get('timeEnd')

    # Chuyển đổi ID sang ObjectId
    object_id = ObjectId(id)

    # Kiểm tra xem scheduler có tồn tại không
    scheduler = collection_setup_scheduler.find_one({'_id': object_id})
    if not scheduler:
        return {
            'message': 'Device not found', 
            'errCode': 1
        }, 404

    # Kiểm tra xem user có tồn tại không
    user = collection_user.find_one({'email': email})
    if not user:
        return {
            'message': 'User not found', 
            'errCode': 1
        }, 404

    # Tạo danh sách giá trị cần update
    new_values = {"$set": {}}

    if email:
        new_values["$set"]['email_user'] = email

    if timeStart:
        new_values["$set"]['timeStart'] = timeStart

    if timeEnd:
        new_values["$set"]['timeEnd'] = timeEnd

    # Thực hiện update
    collection_setup_scheduler.update_one({"_id": object_id}, new_values)

    # Lấy dữ liệu sau khi update để trả về
    updated_scheduler = collection_setup_scheduler.find_one({"_id": object_id})

    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

    return {
        'message': 'Update scheduler successful',
        'data': {
                'email_user': updated_scheduler.get('email_user'),
                'relayName': updated_scheduler.get("relayName"),
                'timeStart': updated_scheduler.get("timeStart"),
                'timeEnd': updated_scheduler.get("timeEnd"),
                'timestamp': updated_scheduler["timestamp"].astimezone(vietnam_tz).strftime("%Y-%m-%dT%H:%M:%S") 
                    if isinstance(updated_scheduler["timestamp"], datetime) else updated_scheduler["timestamp"]
            }
        }, 200



def service_delete_setup_scheduler(body):
    data = body
    
    if not body.get("id"):
         return {
            "message": "ID is required",
            "errCode": 1
        }, 400
    
    id = data.get("id")

    # Chuyển đổi ID từ string -> ObjectId
    object_id = ObjectId(id)

    # Tìm dữ liệu trước khi xóa
    scheduler = collection_setup_scheduler.find_one({"_id": object_id})
    if not scheduler:
        return {
            "message": "No scheduler found in system",
            "errCode": 1
        }, 400

    # Xóa bản ghi theo ID
    collection_setup_scheduler.delete_one({"_id": object_id})

    return {
        "message": "Scheduler deleted successfully",
        "data": {
            "id": str(object_id),
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }
    }, 200

def service_get_setup_threshold():
    # Lấy bản ghi đầu tiên từ collection
    existing_threshold = collection_setup_threshold.find_one()

    # Kiểm tra nếu không tìm thấy threshold
    if not existing_threshold:
        return {
            'message': 'Threshold not found',
            'errCode': 1,
            'data': {
                "temperature_threshold": 0,
                "humidity_threshold": 0,
                "humidity_soil_threshold": 0,
                "light_threshold": 0
            }
        }, 404
       
    temperature_threshold = existing_threshold.get('temperature_threshold')
    humidity_threshold = existing_threshold.get('humidity_threshold')
    humidity_soil_threshold = existing_threshold.get('humidity_soil_threshold')
    light_threshold = existing_threshold.get('light_threshold')

    return {
        'message': 'Get threshold successful',
        'data': {
            "temperature_threshold": temperature_threshold,
            "humidity_threshold": humidity_threshold,
            "humidity_soil_threshold": humidity_soil_threshold,
            "light_threshold": light_threshold
        }
    }, 200

def service_put_setup_threshold(body):
    data = body
   
    temperature = data.get('temperature_threshold')
    humidity = data.get('humidity_threshold')
    humidity_soil = data.get('humidity_soil_threshold')
    light = data.get('light_threshold')
   
    # Lấy bản ghi đầu tiên từ collection
    existing_threshold = collection_setup_threshold.find_one()

    # Khởi tạo các giá trị mặc định
    temperature_threshold = None
    humidity_threshold = None
    humidity_soil_threshold = None
    light_threshold = None
    object_id = None

    if existing_threshold:
        object_id = existing_threshold.get('_id')
        temperature_threshold = existing_threshold.get('temperature_threshold')
        humidity_threshold = existing_threshold.get('humidity_threshold')
        humidity_soil_threshold = existing_threshold.get('humidity_soil_threshold')
        light_threshold = existing_threshold.get('light_threshold')

    new_values = {"$set": {}}

    if temperature is not None:
        new_values["$set"]['temperature_threshold'] = temperature
    else:
        new_values["$set"]['temperature_threshold'] = temperature_threshold

    if humidity is not None:
        new_values["$set"]['humidity_threshold'] = humidity
    else:
        new_values["$set"]['humidity_threshold'] = humidity_threshold

    if humidity_soil is not None:
        new_values["$set"]['humidity_soil_threshold'] = humidity_soil
    else:
        new_values["$set"]['humidity_soil_threshold'] = humidity_soil_threshold

    if light is not None:
        new_values["$set"]['light_threshold'] = light
    else:
        new_values["$set"]['light_threshold'] = light_threshold

    # Thực hiện update - FIX: sử dụng collection_setup_threshold thay vì collection_setup_scheduler
    if object_id:
        collection_setup_threshold.update_one({"_id": object_id}, new_values)
    else:
        # Cập nhật hoặc chèn mới vào collection_setup_threshold
        collection_setup_threshold.update_one(
            {"_id": object_id} if object_id else {},
            new_values,
            upsert=True
        )

    # Gửi dữ liệu đến Core IOT
    core_iot_url = "https://app.coreiot.io/api/plugins/telemetry/DEVICE/21c4e8a0-f63f-11ef-a887-6d1a184f2bb5/SHARED_SCOPE"
    core_iot_body = {
        "temperature_threshold": new_values["$set"]['temperature_threshold'],
        "humidity_threshold": new_values["$set"]['humidity_threshold'],
        "humidity_soil_threshold": new_values["$set"]['humidity_soil_threshold'],
        "light_threshold": new_values["$set"]['light_threshold']
    }
   
    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ2aW5oLm5ndXllbjEyM0BoY211dC5lZHUudm4iLCJ1c2VySWQiOiJjOWY5OGNmMC1lMTQ2LTExZWYtYWQwOS01MTVmNzkwZWQ5ZGYiLCJzY29wZXMiOlsiVEVOQU5UX0FETUlOIl0sInNlc3Npb25JZCI6ImU4MzU5YzgxLWQ2NmEtNDljYi05NjgyLWE3MTg0MDFlOTQ4YyIsImV4cCI6MTc0MjAyMDQzMSwiaXNzIjoiY29yZWlvdC5pbyIsImlhdCI6MTc0MjAxMTQzMSwiZmlyc3ROYW1lIjoiVklOSCIsImxhc3ROYW1lIjoiTkdVWeG7hE4gS0jhuq5DIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6ImM5ZTk4NzYwLWUxNDYtMTFlZi1hZDA5LTUxNWY3OTBlZDlkZiIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.mS-l5RJ-zRfHzJ237nGnnBNidf2KsQqnb0mgJWJtw8voOdkpMlOH3wuQvUtaKIV9qn8BZhr60E_DRrCzaDvp7w"
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
                print(f"Successfully sent command to Core IOT: {response.text}")
                break
            else:
                print(f"Error sending command to Core IOT: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Exception when calling Core IOT API: {str(e)}")
        if attempt < max_retries - 1:
            time.sleep(1)
   
    return {
        'message': 'Create threshold successful',
        'data': {
            "temperature_threshold": new_values["$set"]['temperature_threshold'],
            "humidity_threshold": new_values["$set"]['humidity_threshold'],
            "humidity_soil_threshold": new_values["$set"]['humidity_soil_threshold'],
            "light_threshold": new_values["$set"]['light_threshold']
        }
    }, 200


def service_delete_setup_threshold():
    # Lấy bản ghi đầu tiên từ collection
    existing_threshold = collection_setup_threshold.find_one()


    if len(existing_threshold) == 0:
        return {
                'message': 'Threshold not found',
                'errCode': 1
            }, 404
    object_id = existing_threshold.get('_id')
    new_values = {"$set": {}}
    new_values["$set"]['temperature_threshold'] = 0
    new_values["$set"]['humidity_threshold'] = 0
    new_values["$set"]['humidity_soil_threshold'] = 0
    new_values["$set"]['light_threshold'] = 0


    # print




    # Thực hiện update
    collection_setup_threshold.update_one({"_id": object_id}, new_values)
   


    core_iot_url = "https://app.coreiot.io/api/plugins/telemetry/DEVICE/21c4e8a0-f63f-11ef-a887-6d1a184f2bb5/SHARED_SCOPE"
    core_iot_body = {
        "temperature_threshold": 0,
        "humidity_threshold": 0,
        "humidity_soil_threshold": 0,
        "light_threshold": 0
    }
   
    token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ2aW5oLm5ndXllbjEyM0BoY211dC5lZHUudm4iLCJ1c2VySWQiOiJjOWY5OGNmMC1lMTQ2LTExZWYtYWQwOS01MTVmNzkwZWQ5ZGYiLCJzY29wZXMiOlsiVEVOQU5UX0FETUlOIl0sInNlc3Npb25JZCI6ImU4MzU5YzgxLWQ2NmEtNDljYi05NjgyLWE3MTg0MDFlOTQ4YyIsImV4cCI6MTc0MjAyMDQzMSwiaXNzIjoiY29yZWlvdC5pbyIsImlhdCI6MTc0MjAxMTQzMSwiZmlyc3ROYW1lIjoiVklOSCIsImxhc3ROYW1lIjoiTkdVWeG7hE4gS0jhuq5DIiwiZW5hYmxlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6ImM5ZTk4NzYwLWUxNDYtMTFlZi1hZDA5LTUxNWY3OTBlZDlkZiIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.mS-l5RJ-zRfHzJ237nGnnBNidf2KsQqnb0mgJWJtw8voOdkpMlOH3wuQvUtaKIV9qn8BZhr60E_DRrCzaDvp7w"
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
                print(f"Successfully sent command to Core IOT: {response.text}")
                break
            else:
                print(f"Error sending command to Core IOT: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Exception when calling Core IOT API: {str(e)}")
            if attempt < max_retries - 1:time.sleep(1)


   
    return {
        'message': 'Delete threshold successful',
        'data': {}
    }, 200


