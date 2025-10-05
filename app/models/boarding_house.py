from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RoomType(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"
    SHARED = "shared"
    SUITE = "suite"

class RoomStatus(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"

class TenantStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    room_number: str
    room_type: RoomType
    price_per_month: float
    capacity: int
    amenities: List[str] = []

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: str
    status: RoomStatus
    current_occupancy: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

class TenantBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    emergency_contact: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: str
    status: TenantStatus
    check_in_date: Optional[datetime] = None
    check_out_date: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    tenant_id: str
    room_id: str
    start_date: datetime
    end_date: datetime

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: str
    status: str
    created_at: datetime
    total_amount: float
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None