from app.database.neo4j_connector import neo4j_connector
from app.models.boarding_house import *
from app.auth.security import get_password_hash
from typing import List, Optional
from datetime import datetime
import uuid

class BoardingService:
    
    def _convert_neo4j_to_dict(self, record):
        """Convert Neo4j record to JSON-serializable dict"""
        result = {}
        for key, value in record.items():
            if hasattr(value, 'iso_format'):
                # Convert Neo4j DateTime to ISO string
                result[key] = value.iso_format()
            elif hasattr(value, '__dict__'):
                # Handle other Neo4j types
                result[key] = str(value)
            else:
                result[key] = value
        return result
    
    def _process_room_data(self, room_data):
        """Process room data for JSON serialization"""
        room_dict = dict(room_data)
        # Convert Neo4j DateTime to string
        if 'created_at' in room_dict and hasattr(room_dict['created_at'], 'iso_format'):
            room_dict['created_at'] = room_dict['created_at'].iso_format()
        return room_dict
    
    def _process_tenant_data(self, tenant_data):
        """Process tenant data for JSON serialization"""
        tenant_dict = dict(tenant_data)
        # Convert Neo4j DateTime fields to strings
        date_fields = ['created_at', 'check_in_date', 'check_out_date']
        for field in date_fields:
            if field in tenant_dict and tenant_dict[field] and hasattr(tenant_dict[field], 'iso_format'):
                tenant_dict[field] = tenant_dict[field].iso_format()
        return tenant_dict
    
    def _process_booking_data(self, booking_data):
        """Process booking data for JSON serialization"""
        booking_dict = dict(booking_data)
        # Convert Neo4j DateTime fields to strings
        date_fields = ['created_at', 'start_date', 'end_date']
        for field in date_fields:
            if field in booking_dict and booking_dict[field] and hasattr(booking_dict[field], 'iso_format'):
                booking_dict[field] = booking_dict[field].iso_format()
        return booking_dict
    
    # User Management
    def create_user(self, user: UserCreate):
        session = neo4j_connector.get_session()
        user_id = str(uuid.uuid4())
        
        # Hash the password before storing
        hashed_password = get_password_hash(user.password)
        
        query = """
        CREATE (u:User {
            id: $id,
            username: $username,
            email: $email,
            full_name: $full_name,
            hashed_password: $hashed_password,
            is_active: true,
            created_at: datetime()
        })
        RETURN u
        """
        
        result = session.run(query, 
                           id=user_id,
                           username=user.username,
                           email=user.email,
                           full_name=user.full_name,
                           hashed_password=hashed_password)
        
        return user_id
    
    def get_user_by_username(self, username: str):
        session = neo4j_connector.get_session()
        
        query = "MATCH (u:User {username: $username}) RETURN u"
        result = session.run(query, username=username)
        record = result.single()
        
        if record:
            user_data = dict(record["u"])
            # Process user data for JSON serialization
            if 'created_at' in user_data and hasattr(user_data['created_at'], 'iso_format'):
                user_data['created_at'] = user_data['created_at'].iso_format()
            return user_data
        return None
    
    # Room Management
    def create_room(self, room: RoomCreate):
        session = neo4j_connector.get_session()
        room_id = str(uuid.uuid4())
        
        query = """
        CREATE (r:Room {
            id: $id,
            room_number: $room_number,
            room_type: $room_type,
            price_per_month: $price_per_month,
            capacity: $capacity,
            amenities: $amenities,
            status: 'available',
            current_occupancy: 0,
            created_at: datetime()
        })
        RETURN r
        """
        
        result = session.run(query,
                           id=room_id,
                           room_number=room.room_number,
                           room_type=room.room_type,
                           price_per_month=room.price_per_month,
                           capacity=room.capacity,
                           amenities=room.amenities)
        
        return room_id
    
    def get_all_rooms(self):
        session = neo4j_connector.get_session()
        
        query = "MATCH (r:Room) RETURN r ORDER BY r.room_number"
        result = session.run(query)
        
        rooms = []
        for record in result:
            room_data = dict(record["r"])
            rooms.append(self._process_room_data(room_data))
        
        return rooms
    
    def get_available_rooms(self):
        session = neo4j_connector.get_session()
        
        query = "MATCH (r:Room {status: 'available'}) WHERE r.current_occupancy < r.capacity RETURN r"
        result = session.run(query)
        
        rooms = []
        for record in result:
            room_data = dict(record["r"])
            rooms.append(self._process_room_data(room_data))
        
        return rooms
    
    def get_room_by_id(self, room_id: str):
        session = neo4j_connector.get_session()
        
        query = "MATCH (r:Room {id: $room_id}) RETURN r"
        result = session.run(query, room_id=room_id)
        record = result.single()
        
        if record:
            room_data = dict(record["r"])
            return self._process_room_data(room_data)
        return None
    
    def update_room_status(self, room_id: str, status: RoomStatus):
        session = neo4j_connector.get_session()
        
        query = "MATCH (r:Room {id: $room_id}) SET r.status = $status RETURN r"
        result = session.run(query, room_id=room_id, status=status)
        
        return result.single() is not None
    
    # Tenant Management
    def create_tenant(self, tenant: TenantCreate):
        session = neo4j_connector.get_session()
        tenant_id = str(uuid.uuid4())
        
        query = """
        CREATE (t:Tenant {
            id: $id,
            full_name: $full_name,
            email: $email,
            phone: $phone,
            emergency_contact: $emergency_contact,
            status: 'pending',
            created_at: datetime()
        })
        RETURN t
        """
        
        result = session.run(query,
                           id=tenant_id,
                           full_name=tenant.full_name,
                           email=tenant.email,
                           phone=tenant.phone,
                           emergency_contact=tenant.emergency_contact)
        
        return tenant_id
    
    def get_all_tenants(self):
        session = neo4j_connector.get_session()
        
        query = "MATCH (t:Tenant) RETURN t ORDER BY t.full_name"
        result = session.run(query)
        
        tenants = []
        for record in result:
            tenant_data = dict(record["t"])
            tenants.append(self._process_tenant_data(tenant_data))
        
        return tenants
    
    def get_tenant_by_id(self, tenant_id: str):
        session = neo4j_connector.get_session()
        
        query = "MATCH (t:Tenant {id: $tenant_id}) RETURN t"
        result = session.run(query, tenant_id=tenant_id)
        record = result.single()
        
        if record:
            tenant_data = dict(record["t"])
            return self._process_tenant_data(tenant_data)
        return None
    
    # Booking Management
    def create_booking(self, booking: BookingCreate):
        session = neo4j_connector.get_session()
        booking_id = str(uuid.uuid4())
        
        # Get room price
        room = self.get_room_by_id(booking.room_id)
        if not room:
            raise ValueError("Room not found")
        
        # Calculate total amount (simplified)
        from datetime import datetime
        start_date = datetime.fromisoformat(booking.start_date) if isinstance(booking.start_date, str) else booking.start_date
        end_date = datetime.fromisoformat(booking.end_date) if isinstance(booking.end_date, str) else booking.end_date
        
        months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        total_amount = room['price_per_month'] * max(months, 1)
        
        query = """
        MATCH (t:Tenant {id: $tenant_id}), (r:Room {id: $room_id})
        CREATE (b:Booking {
            id: $booking_id,
            start_date: datetime($start_date),
            end_date: datetime($end_date),
            status: 'confirmed',
            total_amount: $total_amount,
            created_at: datetime()
        })
        CREATE (t)-[:HAS_BOOKING]->(b)
        CREATE (b)-[:FOR_ROOM]->(r)
        SET r.current_occupancy = r.current_occupancy + 1
        SET r.status = CASE 
            WHEN r.current_occupancy >= r.capacity THEN 'occupied' 
            ELSE r.status 
        END
        SET t.status = 'active'
        SET t.check_in_date = datetime($start_date)
        RETURN b
        """
        
        result = session.run(query,
                           tenant_id=booking.tenant_id,
                           room_id=booking.room_id,
                           booking_id=booking_id,
                           start_date=booking.start_date.isoformat(),
                           end_date=booking.end_date.isoformat(),
                           total_amount=total_amount)
        
        return booking_id
    
    def get_bookings_by_tenant(self, tenant_id: str):
        session = neo4j_connector.get_session()
        
        query = """
        MATCH (t:Tenant {id: $tenant_id})-[:HAS_BOOKING]->(b:Booking)-[:FOR_ROOM]->(r:Room)
        RETURN b, r
        ORDER BY b.created_at DESC
        """
        
        result = session.run(query, tenant_id=tenant_id)
        
        bookings = []
        for record in result:
            booking_data = self._process_booking_data(dict(record["b"]))
            booking_data["room"] = self._process_room_data(dict(record["r"]))
            bookings.append(booking_data)
        
        return bookings
    
    def get_all_bookings(self):
        session = neo4j_connector.get_session()
        
        query = """
        MATCH (t:Tenant)-[:HAS_BOOKING]->(b:Booking)-[:FOR_ROOM]->(r:Room)
        RETURN b, t, r
        ORDER BY b.created_at DESC
        """
        
        result = session.run(query)
        
        bookings = []
        for record in result:
            booking_data = self._process_booking_data(dict(record["b"]))
            booking_data["tenant"] = self._process_tenant_data(dict(record["t"]))
            booking_data["room"] = self._process_room_data(dict(record["r"]))
            bookings.append(booking_data)
        
        return bookings
    
    def cancel_booking(self, booking_id: str):
        session = neo4j_connector.get_session()
        
        query = """
        MATCH (b:Booking {id: $booking_id})-[r1:FOR_ROOM]->(room:Room)
        MATCH (tenant:Tenant)-[r2:HAS_BOOKING]->(b)
        SET b.status = 'cancelled'
        SET room.current_occupancy = room.current_occupancy - 1
        SET room.status = 'available'
        SET tenant.status = 'inactive'
        SET tenant.check_out_date = datetime()
        RETURN b
        """
        
        result = session.run(query, booking_id=booking_id)
        return result.single() is not None

boarding_service = BoardingService()