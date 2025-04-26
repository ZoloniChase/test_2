import uuid
from enum import Enum
from typing import List, Dict
from datetime import datetime

class RoomType(Enum):
    STANDARD = "Standard"
    DELUXE = "Deluxe"
    SUITE = "Suite"
    PRESIDENTIAL = "Presidential"

class RoomStatus(Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"
    RESERVED = "Reserved"

DEFAULT_CAPACITY: Dict[RoomType, int] = {
    RoomType.STANDARD: 2,
    RoomType.DELUXE: 2,
    RoomType.SUITE: 4,
    RoomType.PRESIDENTIAL: 6
}

DEFAULT_RATE: Dict[RoomType, float] = {
    RoomType.STANDARD: 5000.0,
    RoomType.DELUXE: 10000.0,
    RoomType.SUITE: 20000.0,
    RoomType.PRESIDENTIAL: 50000.0
}

DEFAULT_AMENITIES = {
    RoomType.STANDARD: ["TV", "Wi-Fi"],
    RoomType.DELUXE: ["TV", "Wi-Fi", "Mini-Bar"],
    RoomType.SUITE: ["TV", "Wi-Fi", "Mini-Bar", "Kitchenette"],
    RoomType.PRESIDENTIAL: ["TV", "Wi-Fi", "Mini-Bar", "Kitchenette", "Private Pool", "Butler Service"]
}

class Room:
    def __init__(self, room_number: str, room_type: RoomType, capacity: int = None, rate: float = None, amenities: List[str] = None):
        self.room_number = room_number
        self.room_type = room_type
        self.capacity = capacity if capacity is not None else DEFAULT_CAPACITY[room_type]
        self.base_rate = rate if rate is not None else DEFAULT_RATE[room_type]
        self.amenities = amenities if amenities is not None else DEFAULT_AMENITIES[room_type]
        self.status = RoomStatus.AVAILABLE
        self.current_guest = None
        self.cleaning_schedule = []
        
    def update_status(self, new_status: RoomStatus):
        self.status = new_status
        
    def add_cleaning_task(self, task: str, time: datetime):
        self.cleaning_schedule.append({"task": task, "time": time})
        
    def is_available(self) -> bool:
        return self.status == RoomStatus.AVAILABLE

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}  

    def add_room(self, room: Room) -> bool:
        if room.room_number in self.rooms:
            return False  
        self.rooms[room.room_number] = room
        return True

    def get_room(self, room_number: str) -> Optional[Room]:
        return self.rooms.get(room_number)

    def get_available_rooms(self) -> List[Room]:
        return [room for room in self.rooms.values() if room.is_available()]

    def assign_guest_to_room(self, guest: Guest, room_type: RoomType, 
    check_in_date: datetime, duration_days: int, preferred_room_number: str = None) -> Optional[Room]:

        if preferred_room_number:
            room = self.get_room(preferred_room_number)
            if (room and room.is_available() and room.room_type == room_type):
                self._assign_guest(room, guest, check_in_date, duration_days)
                return room
        
        for room in self.rooms.values():
            if (room.is_available() and room.room_type == room_type):
                self._assign_guest(room, guest, check_in_date, duration_days)
                return room
        
        return None

    def update_room_status(self, room_number: str, new_status: RoomStatus) -> bool:
        ns True if successful, False if room not found.
        
        room = self.get_room(room_number)
        if not room:
            return False
            
        room.update_status(new_status)
        
        if new_status == RoomStatus.AVAILABLE:
            room.current_guest = None
            room.check_in_date = None
            room.check_out_date = None
            
        return True

    def check_out_guest(self, room_number: str) -> bool:
        room = self.get_room(room_number)
        if not room or room.status != RoomStatus.OCCUPIED:
            return False
            
        room.update_status(RoomStatus.MAINTENANCE)
        
        now = datetime.now()
        room.add_cleaning_task("Post-checkout deep clean", now)
        room.add_cleaning_task("Linen replacement", now + timedelta(minutes=30))
        room.add_cleaning_task("Final inspection", now + timedelta(hours=1))
        
        room.current_guest = None
        room.check_in_date = None
        room.check_out_date = None
        
        return True

    def complete_cleaning(self, room_number: str) -> bool:
        room = self.get_room(room_number)
        if not room or room.status != RoomStatus.MAINTENANCE:
            return False
            
        room.update_status(RoomStatus.AVAILABLE)
        room.cleaning_schedule = []  
        return True