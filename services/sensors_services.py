from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder  # Thêm thư viện này
from databases.databases import *
from schemas import SensorData, SensorDataWeek, SensorDataDay, SensorDataMonth
import asyncio
from datetime import datetime, timedelta, timezone
import pandas as pd
from dateutil.relativedelta import relativedelta
import pytz
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from fastapi.encoders import jsonable_encoder
import time
import aio_pika
import json

async def service_post_all_data(body):
    data = body
    
    temperature = float(data.get('temperature', 0))
    humidity_soil = float(data.get('humidity_soil', 0))
    lux = float(data.get('lux', 0))
    N_soil = float(data.get('N_soil', 0))
    P_soil = float(data.get('P_soil', 0))
    K_soil = float(data.get('K_soil', 0))
    
    user_id = data.get('user_id', 1)
    
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = datetime.now(vietnam_tz)
    formatted_time = vietnam_time.strftime("%Y-%m-%dT%H:%M:%S")
    print(f"Thời gian nhận dữ liệu: {formatted_time}")
    
    sensor_data = {
        'temperature': temperature,
        'humidity_soil': humidity_soil,
        'lux': lux,
        'N_soil': N_soil,
        'P_soil': P_soil,
        'K_soil': K_soil,
        'timestamp': formatted_time,
        'user_id': user_id
    }
    
    RABBITMQ_HOST = "localhost"
    QUEUE_NAME = "sensor_data_queue"
    
    try:
        connection = await aio_pika.connect_robust(f"amqp://guest:guest@{RABBITMQ_HOST}/")
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(QUEUE_NAME, durable=True)
            
            message = json.dumps(sensor_data)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode(), delivery_mode=2),
                routing_key=QUEUE_NAME
            )

            print(f"Sent to RabbitMQ: {message}")
        
        response = {
            'message': 'Data sensors sent to queue successfully',
            'data': {
                'temperature': sensor_data['temperature'],
                'humidity_soil': sensor_data['humidity_soil'],
                'lux': sensor_data['lux'],
                'N_soil': sensor_data['N_soil'],
                'P_soil': sensor_data['P_soil'],
                'K_soil': sensor_data['K_soil'],
                'timestamp': formatted_time,
                'user_id': user_id
            }
        }
        return response, 201
    
    except Exception as e:
        raise Exception(f"Failed to send to RabbitMQ: {str(e)}")
    

def service_get_all_data(user: str):
    """
    Lấy dữ liệu mới nhất từ MongoDB nhanh chóng
    """
    # Cache system - Simple in-memory cache
    if not hasattr(service_get_all_data, 'cache'):
        service_get_all_data.cache = {}
    
    cache = service_get_all_data.cache
    CACHE_TIMEOUT = 300  # 5 phút
    
    # Tạo key cache đơn giản
    current_time = datetime.now(timezone.utc)
    time_key = (current_time.minute // 5) * 5
    cache_key = f"latest_data_{user}_{current_time.strftime('%Y-%m-%d')}_{time_key}"
    
    # Kiểm tra cache
    if cache_key in cache and time.time() - cache[cache_key]['time'] < CACHE_TIMEOUT:
        print(f"Using cached data for {cache_key}")
        return cache[cache_key]['data']
    
    print(f"Fetching latest data for user: {user}")
    
    try:
        # Đảm bảo chỉ mục
        ensure_indexes()
        
        # Lấy document mới nhất trực tiếp
        latest_sensor = collection_sensor_data.find_one(
            {},  # Không lọc
            {
                "_id": 0,
                "lux": 1,
                "temperature": 1,
                "humidity_soil": 1,
                "N_soil": 1,
                "P_soil": 1,
                "K_soil": 1,
                "timestamp": 1
            },
            sort=[("timestamp", -1)]  # Sắp xếp giảm dần theo timestamp
        )
        
        if not latest_sensor:
            result = {
                'message': 'No data available',
                'data': []
            }, 404
            
            # Cache kết quả trống
            cache[cache_key] = {
                'data': result,
                'time': time.time()
            }
            return result
        
        print(f"Got latest data from: {latest_sensor['timestamp']}")
        
        # Tạo đối tượng dữ liệu
        sensor_data = SensorData(
            lux=latest_sensor["lux"],
            temperature=latest_sensor["temperature"],
            humidity_soil=latest_sensor["humidity_soil"],
            N_soil=latest_sensor["N_soil"],
            P_soil=latest_sensor["P_soil"],
            K_soil=latest_sensor["K_soil"],
            timestamp=latest_sensor["timestamp"]
        )
        
        # Chuẩn bị response
        response_data = {
            "total_data": 1,
            "sensor_data": [jsonable_encoder(sensor_data)]
        }
        
        result = {
            'message': 'Get latest data successfully',
            'data': response_data
        }, 200
        
        # Cập nhật cache
        cache[cache_key] = {
            'data': result,
            'time': time.time()
        }
        
        return result
        
    except Exception as e:
        print(f"Error fetching latest data: {e}")
        return {
            'message': f'Error fetching latest data: {str(e)}',
            'data': []
        }, 500

def ensure_indexes():
    """
    Đảm bảo các chỉ mục cần thiết đã được tạo
    """
    # Tạo biến kiểm tra xem đã tạo index chưa
    if not hasattr(ensure_indexes, 'indexes_created'):
        try:
            # Tạo chỉ mục cho trường timestamp (giảm dần)
            collection_sensor_data.create_index([("timestamp", -1)], background=True)
            print("Created index on timestamp field (descending)")
            
            # Đánh dấu đã tạo index
            ensure_indexes.indexes_created = True
        except Exception as e:
            print(f"Error creating indexes: {e}")
            # Không đánh dấu nếu lỗi, để lần sau thử lại
            pass


def service_get_all_data_month(user: str):
    # Tính thời gian bắt đầu và kết thúc cho khoảng thời gian 1 tuần
    # Go back 12 months from the current date
    start_date = (datetime.now(timezone.utc) - relativedelta(months=12)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Lấy thời gian hiện tại
    end_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Debug thông tin thời gian
    print(f"Fetching data from {start_date} to {end_date} for user: {user}")

    sensors = collection_sensor_data.find({
        "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }  # Lọc dữ liệu có timestamp >= one_week_ago
    })
    
    # Nếu không có dữ liệu cảm biến nào cho người dùng
    if collection_sensor_data.count_documents({"timestamp": {
        "$gte": start_date,
        "$lte": end_date
    }}) == 0:
        return {
            'message': 'Data or user do not have data in the last week',
            'data': []
        }, 200
    
    df = pd.DataFrame(sensors)

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M:%S")
    df["year_month"] = df["timestamp"].dt.to_period("M")
    df["lux"] = pd.to_numeric(df["lux"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity_soil"] = pd.to_numeric(df["humidity_soil"], errors="coerce")

    df["N_soil"] = pd.to_numeric(df["N_soil"], errors="coerce")
    df["P_soil"] = pd.to_numeric(df["P_soil"], errors="coerce")
    df["K_soil"] = pd.to_numeric(df["K_soil"], errors="coerce")

    monthly_avg = df.groupby("year_month")[["lux", "temperature", "humidity_soil", "N_soil","P_soil","K_soil"]].mean().reset_index()

    monthly_avg['month_name'] = monthly_avg['year_month'].dt.strftime('%b')
    monthly_avg['year'] = monthly_avg['year_month'].dt.year

    monthly_avg = monthly_avg.reset_index()

    print(monthly_avg)

    sensor_data_list = [
        SensorDataMonth(
            lux=row["lux"],
            temperature=row["temperature"],
            humidity_soil=row["humidity_soil"],
            N_soil=row["N_soil"],
            P_soil=row["P_soil"],
            K_soil=row["K_soil"],
            month=row["month_name"],
            year = row["year"]
        )
        for index, row in monthly_avg.iterrows()
    ]

    print(sensor_data_list)

    # Convert data to JSON response
    response_data = {
        "total_data": len(sensor_data_list),
        "sensor_data": jsonable_encoder(sensor_data_list)  # Converts objects to JSON-compatible format
    }

    # Return JSON response with status code
    return {
        'message': 'Get all data successfully',
        'data': response_data
    }, 200


def service_get_all_data_week(user: str):

    # Cache system - Simple in-memory cache with expiration
    cache = getattr(service_get_all_data_week, 'cache', {})
    CACHE_TIMEOUT = 3600  # 1 hour cache

    # Calculate time range for 1 week
    start_date = (datetime.now(timezone.utc) - relativedelta(weeks=1)).strftime("%Y-%m-%d")
    end_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Create cache key based on date range
    date_key = start_date[:10]
    cache_key = f"weekly_avg_{date_key}_hourly"

    # Check if we have cached result
    if cache_key in cache and time.time() - cache[cache_key]['time'] < CACHE_TIMEOUT:
        print(f"Using cached data for {cache_key}")
        return cache[cache_key]['data']

    print(f"Fetching hourly data from {start_date} to {end_date} for user: {user}")

    # Approach: Query only data at exact hours (00 minutes, 00 seconds)
    try:
        # MongoDB aggregation pipeline to get only data at exact hours
        pipeline = [
            # Match documents in the date range
            {"$match": {
                "timestamp": {
                    "$gte": f"{start_date}T00:00:00", 
                    "$lte": f"{end_date}T23:59:59"
                }
            }},
            
            # Extract hour, minute and second components
            {"$addFields": {
                "parsed_date": {"$dateFromString": {"dateString": "$timestamp"}},
                "minute": {"$minute": {"$dateFromString": {"dateString": "$timestamp"}}},
                "second": {"$second": {"$dateFromString": {"dateString": "$timestamp"}}}
            }},
            
            # Only keep entries where minutes and seconds are close to 0
            # This selects data points closest to the exact hour
            {"$match": {
                "$expr": {
                    "$and": [
                        {"$lte": ["$minute", 5]},  # Within 5 minutes of the hour
                        {"$lte": ["$second", 59]}
                    ]
                }
            }},
            
            # Sort by timestamp to ensure we pick the closest one to the hour
            {"$sort": {"timestamp": 1}},
            
            # Group by date and hour to get one reading per hour
            {"$group": {
                "_id": {
                    "date": {"$substr": ["$timestamp", 0, 10]},
                    "hour": {"$hour": "$parsed_date"}
                },
                "timestamp": {"$first": "$timestamp"},
                "lux": {"$first": {"$toDouble": "$lux"}},
                "temperature": {"$first": {"$toDouble": "$temperature"}},
                "humidity_soil": {"$first": {"$toDouble": "$humidity_soil"}},
                "N_soil": {"$first": {"$toDouble": "$N_soil"}},
                "P_soil": {"$first": {"$toDouble": "$P_soil"}},
                "K_soil": {"$first": {"$toDouble": "$K_soil"}}
            }},
            
            # Add weekday field
            {"$addFields": {
                "weekday": {
                    "$let": {
                        "vars": {
                            "dayOfWeek": {"$dayOfWeek": {"$dateFromString": {"dateString": "$timestamp"}}}
                        },
                        "in": {
                            "$switch": {
                                "branches": [
                                    {"case": {"$eq": ["$$dayOfWeek", 1]}, "then": "Sunday"},
                                    {"case": {"$eq": ["$$dayOfWeek", 2]}, "then": "Monday"},
                                    {"case": {"$eq": ["$$dayOfWeek", 3]}, "then": "Tuesday"},
                                    {"case": {"$eq": ["$$dayOfWeek", 4]}, "then": "Wednesday"},
                                    {"case": {"$eq": ["$$dayOfWeek", 5]}, "then": "Thursday"},
                                    {"case": {"$eq": ["$$dayOfWeek", 6]}, "then": "Friday"},
                                    {"case": {"$eq": ["$$dayOfWeek", 7]}, "then": "Saturday"}
                                ],
                                "default": "Unknown"
                            }
                        }
                    }
                }
            }},
            
            # Group by weekday to get daily averages
            {"$group": {
                "_id": "$weekday",
                "lux": {"$avg": "$lux"},
                "temperature": {"$avg": "$temperature"},
                "humidity_soil": {"$avg": "$humidity_soil"},
                "N_soil": {"$avg": "$N_soil"},
                "P_soil": {"$avg": "$P_soil"},
                "K_soil": {"$avg": "$K_soil"}
            }},
            
            # Format final result
            {"$project": {
                "_id": 0,
                "weekday": "$_id",
                "lux": 1,
                "temperature": 1,
                "humidity_soil": 1,
                "N_soil": 1,
                "P_soil": 1,
                "K_soil": 1
            }}
        ]
        
        # Execute aggregation with disk use allowed for large datasets
        results = list(collection_sensor_data.aggregate(pipeline, allowDiskUse=True))
        
        # Convert results to SensorDataWeek objects
        sensor_data_list = [
            SensorDataWeek(
                lux=row["lux"],
                temperature=row["temperature"],
                humidity_soil=row["humidity_soil"],
                N_soil=row["N_soil"],
                P_soil=row["P_soil"],
                K_soil=row["K_soil"],
                day=row["weekday"]
            )
            for row in results
        ]
        
    except Exception as e:
        print(f"Hourly aggregation failed: {e}, falling back to daily sampling")
        # Fall back to sampling data once per day
        sensor_data_list = sample_daily_data(start_date, end_date)
    
    # Format response
    response_data = {
        "total_data": len(sensor_data_list),
        "sensor_data": jsonable_encoder(sensor_data_list)
    }
    
    # Store in cache
    result = {
        'message': 'Get hourly data successfully',
        'data': response_data
    }, 200
    
    # Update cache
    cache[cache_key] = {
        'data': result,
        'time': time.time()
    }
    service_get_all_data_week.cache = cache
    
    return result


def sample_daily_data(start_date, end_date):
    """Sample sensor data once per day (at noon) to handle situations where hourly data is unavailable"""
    from datetime import datetime, timedelta
    
    daily_results = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Process one day at a time
    while current_date <= end_datetime:
        # Target noon each day
        target_time = current_date.strftime("%Y-%m-%dT12:00:00")
        
        # Find the closest reading to noon
        sample_data = collection_sensor_data.find_one(
            {"timestamp": {"$gte": target_time}},
            sort=[("timestamp", 1)],
            projection={
                "timestamp": 1, 
                "lux": 1, 
                "temperature": 1, 
                "humidity_soil": 1, 
                "N_soil": 1, 
                "P_soil": 1, 
                "K_soil": 1, 
                "_id": 0
            }
        )
        
        if sample_data:
            # Convert to appropriate types
            sample_data["lux"] = float(sample_data["lux"])
            sample_data["temperature"] = float(sample_data["temperature"])
            sample_data["humidity_soil"] = float(sample_data["humidity_soil"])
            sample_data["N_soil"] = float(sample_data["N_soil"])
            sample_data["P_soil"] = float(sample_data["P_soil"])
            sample_data["K_soil"] = float(sample_data["K_soil"])
            
            # Get weekday
            weekday = datetime.strptime(sample_data["timestamp"], "%Y-%m-%dT%H:%M:%S").strftime("%A")
            sample_data["weekday"] = weekday
            
            daily_results.append(sample_data)
        
        current_date += timedelta(days=1)
    
    # Group by weekday and calculate averages
    weekday_data = {}
    for data in daily_results:
        weekday = data["weekday"]
        if weekday not in weekday_data:
            weekday_data[weekday] = {
                "lux": [],
                "temperature": [],
                "humidity_soil": [],
                "N_soil": [],
                "P_soil": [],
                "K_soil": []
            }
        
        weekday_data[weekday]["lux"].append(data["lux"])
        weekday_data[weekday]["temperature"].append(data["temperature"])
        weekday_data[weekday]["humidity_soil"].append(data["humidity_soil"])
        weekday_data[weekday]["N_soil"].append(data["N_soil"])
        weekday_data[weekday]["P_soil"].append(data["P_soil"])
        weekday_data[weekday]["K_soil"].append(data["K_soil"])
    
    # Calculate averages
    result_data = []
    for weekday, values in weekday_data.items():
        result_data.append({
            "weekday": weekday,
            "lux": sum(values["lux"]) / len(values["lux"]) if values["lux"] else 0,
            "temperature": sum(values["temperature"]) / len(values["temperature"]) if values["temperature"] else 0,
            "humidity_soil": sum(values["humidity_soil"]) / len(values["humidity_soil"]) if values["humidity_soil"] else 0,
            "N_soil": sum(values["N_soil"]) / len(values["N_soil"]) if values["N_soil"] else 0,
            "P_soil": sum(values["P_soil"]) / len(values["P_soil"]) if values["P_soil"] else 0,
            "K_soil": sum(values["K_soil"]) / len(values["K_soil"]) if values["K_soil"] else 0
        })
    
    # Convert to SensorDataWeek objects
    sensor_data_list = [
        SensorDataWeek(
            lux=day["lux"],
            temperature=day["temperature"],
            humidity_soil=day["humidity_soil"],
            N_soil=day["N_soil"],
            P_soil=day["P_soil"],
            K_soil=day["K_soil"],
            day=day["weekday"]
        )
        for day in result_data
    ]
    
    return sensor_data_list
    # return "null"


def service_get_all_data_day(user: str):
    # Tính thời gian bắt đầu và kết thúc cho khoảng thời gian 1 tuần
    # Go back 12 months from the current date
    start_date = (datetime.now(timezone.utc) - relativedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Lấy thời gian hiện tại
    end_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Debug thông tin thời gian
    print(f"Fetching data from {start_date} to {end_date} for user: {user}")

    sensors = collection_sensor_data.find({
        "user": user,
        "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }  # Lọc dữ liệu có timestamp >= one_week_ago
    })
    
    # Nếu không có dữ liệu cảm biến nào cho người dùng
    if collection_sensor_data.count_documents({"user": user, "timestamp": {
        "$gte": start_date,
        "$lte": end_date
    }}) == 0:
        return {
            'message': 'Data or user do not have data in the last week',
            'data': []
        }, 200
    
    df = pd.DataFrame(sensors)

    # Chuyển timestamp về dạng datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M:%SZ") 

    # Lấy ngày dạng YYYY-MM-DD
    df["hour"] = df["timestamp"].dt.hour 

    print(df)

    # Chuyển đổi dữ liệu về dạng số
    df["lux"] = pd.to_numeric(df["lux"], errors="coerce")
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")

    # Nhóm theo ngày (date) và thứ (weekday), sau đó tính trung bình
    daily_avg = df.groupby("hour")[["lux", "temperature", "humidity"]].mean().reset_index()

    # In kết quả
    print(daily_avg)

    sensor_data_list = [
        SensorDataDay(
            lux=row["lux"],
            temperature=row["temperature"],
            humidity=row["humidity"],
            hour=row["hour"]
        )
        for index, row in daily_avg.iterrows()
    ]

    print(sensor_data_list)

    # Convert data to JSON response
    response_data = {
        "total_data": len(sensor_data_list),
        "sensor_data": jsonable_encoder(sensor_data_list)  # Converts objects to JSON-compatible format
    }

    # Return JSON response with status code
    return {
        'message': 'Get all data successfully',
        'data': response_data
    }, 200

