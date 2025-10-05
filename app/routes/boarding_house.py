from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.boarding_service import boarding_service
from app.routes.auth import get_current_user
from app.models.boarding_house import *

router = APIRouter(prefix="/api", tags=["boarding house"])

# Room endpoints
@router.post("/rooms", response_model=dict)
async def create_room(room: RoomCreate, current_user: dict = Depends(get_current_user)):
    room_id = boarding_service.create_room(room)
    return {"message": "Room created successfully", "room_id": room_id}

@router.get("/rooms", response_model=List[dict])
async def get_rooms(current_user: dict = Depends(get_current_user)):
    return boarding_service.get_all_rooms()

@router.get("/rooms/available", response_model=List[dict])
async def get_available_rooms(current_user: dict = Depends(get_current_user)):
    return boarding_service.get_available_rooms()

@router.get("/rooms/{room_id}", response_model=dict)
async def get_room(room_id: str, current_user: dict = Depends(get_current_user)):
    room = boarding_service.get_room_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.put("/rooms/{room_id}/status")
async def update_room_status(room_id: str, status: RoomStatus, current_user: dict = Depends(get_current_user)):
    success = boarding_service.update_room_status(room_id, status)
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room status updated successfully"}

# Tenant endpoints
@router.post("/tenants", response_model=dict)
async def create_tenant(tenant: TenantCreate, current_user: dict = Depends(get_current_user)):
    tenant_id = boarding_service.create_tenant(tenant)
    return {"message": "Tenant created successfully", "tenant_id": tenant_id}

@router.get("/tenants", response_model=List[dict])
async def get_tenants(current_user: dict = Depends(get_current_user)):
    return boarding_service.get_all_tenants()

@router.get("/tenants/{tenant_id}", response_model=dict)
async def get_tenant(tenant_id: str, current_user: dict = Depends(get_current_user)):
    tenant = boarding_service.get_tenant_by_id(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

# Booking endpoints
@router.post("/bookings", response_model=dict)
async def create_booking(booking: BookingCreate, current_user: dict = Depends(get_current_user)):
    try:
        booking_id = boarding_service.create_booking(booking)
        return {"message": "Booking created successfully", "booking_id": booking_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/bookings", response_model=List[dict])
async def get_all_bookings(current_user: dict = Depends(get_current_user)):
    return boarding_service.get_all_bookings()

@router.get("/tenants/{tenant_id}/bookings", response_model=List[dict])
async def get_tenant_bookings(tenant_id: str, current_user: dict = Depends(get_current_user)):
    return boarding_service.get_bookings_by_tenant(tenant_id)

@router.put("/bookings/{booking_id}/cancel")
async def cancel_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    success = boarding_service.cancel_booking(booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking cancelled successfully"}