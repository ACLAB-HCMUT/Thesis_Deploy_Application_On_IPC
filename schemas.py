from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime  # Import datetime để sử dụng
from typing import Optional, Dict, Any
import uuid
class SensorData(BaseModel):
    lux: float
    temperature: float
    humidity: float
    timestamp: str 
    
    class Config:
        # Dùng để hỗ trợ chuyển đổi ObjectId sang string trong Pydantic model
        json_encoders = {
            ObjectId: str
        }

class RelayData(BaseModel):
    relayName: str
    email_user: str
    status: str
    timestamp: str 

    class Config:
        # Dùng để hỗ trợ chuyển đổi ObjectId sang string trong Pydantic model
        json_encoders = {
            ObjectId: str
        }

class SensorDataMonth(BaseModel):
    lux: float
    temperature: float
    humidity: float
    month: str  # Thay đổi kiểu dữ liệu thành datetime
    year: int

    class Config:
        # Dùng để hỗ trợ chuyển đổi ObjectId sang string trong Pydantic model
        json_encoders = {
            ObjectId: str
        }

class SchedulerData(BaseModel):
    id: str
    email_user: str
    relayName: str
    timeStart: str  
    timeEnd: str
    timestamps: str
    repeatDaily: bool
    class Config:
        # Dùng để hỗ trợ chuyển đổi ObjectId sang string trong Pydantic model
        json_encoders = {
            ObjectId: str
        }

class SensorDataWeek(BaseModel):
    lux: float
    temperature: float
    humidity: float
    day: str  # Thay đổi kiểu dữ liệu thành datetime

    class Config:
        # Dùng để hỗ trợ chuyển đổi ObjectId sang string trong Pydantic model
        json_encoders = {
            ObjectId: str
        }

class SensorDataDay(BaseModel):
    lux: float
    temperature: float
    humidity: float
    hour: int  # Thay đổi kiểu dữ liệu thành datetime

    class Config:
        # Dùng để hỗ trợ chuyển đổi ObjectId sang string trong Pydantic model
        json_encoders = {
            ObjectId: str
        }

class User(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    firstName: str
    lastName: str
    username: str
    email: str
    phoneNumber: str
    address: str

# class Notification:
#     def __init__(self, user_id, message, timestamp=None, seen=False):
#         self.user_id = user_id
#         self.message = message
#         self.timestamp = timestamp if timestamp else datetime.utcnow()
#         self.seen = seen

#     def to_dict(self):
#         return {
#             'user_id': self.user_id,
#             'message': self.message,
#             'timestamp': self.timestamp,
#             'seen': self.seen
#         }
class Notification(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int
    message: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    seen: bool = False
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self):
        return {
            "_id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "created_at": self.created_at,
            "seen": self.seen,
            "metadata": self.metadata or {}
        }