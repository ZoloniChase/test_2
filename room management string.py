hotel_module_code = """\
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime, date, time, timedelta

class RoomType(Enum):
    STANDARD = "Standard"
    DELUXE = "Deluxe"
    SUITE = "Suite"

class RoomStatus(Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"

class Room:
    def __init__(self, number: int, room_type: RoomType):
        self.number = number
        self.room_type = room_type
        self.status = RoomStatus.AVAILABLE

    def is_available(self) -> bool:
        return self.status == RoomStatus.AVAILABLE

class Inventory:
    def __init__(self):
        # simplified counts
        self._items = {"extra bed": 3, "crib": 2, "better view": 2}

    def options(self) -> List[str]:
        return list(self._items.keys())

    def allocate(self, name: str) -> bool:
        if self._items.get(name, 0) > 0:
            self._items[name] -= 1
            return True
        return False

class Task(ABC):
    def __init__(self, room: Room):
        self.room = room
        self.time: Optional[datetime] = None

    @abstractmethod
    def execute(self, logs: Dict[str, List]):
        pass

class CleaningTask(Task):
    def __init__(self, room: Room, schedule_time: datetime):
        super().__init__(room)
        self.time = schedule_time

    def execute(self, logs: Dict[str, List]):
        self.room.status = RoomStatus.AVAILABLE
        logs["cleaning"].append((self.time, self.room.number))

class ServiceTask(Task):
    def __init__(self, room: Room, request: str):
        super().__init__(room)
        self.request = request

    def execute(self, logs: Dict[str, List]):
        self.room.status = RoomStatus.OCCUPIED
        logs["service"].append((datetime.now(), self.room.number, self.request))

class HotelSystem:
    SERVICE_OPTIONS = ["New sheets/towels", "Mini bar restock", "Cleaning", "Other"]

    def __init__(self):
        # just 10 rooms: 1–4 Standard, 5–7 Deluxe, 8–10 Suite
        self.rooms: Dict[int, Room] = {
            i: Room(i,
                    RoomType.STANDARD if i <= 4 else
                    RoomType.DELUXE if i <= 7 else
                    RoomType.SUITE)
            for i in range(1, 11)
        }
        self.inventory = Inventory()
        self.logs = {"cleaning": [], "service": []}

    def run(self):
        while True:
            print("\\n1.Check-in  2.Special req  3.Cleaning  4.Service  5.Logs  6.Exit")
            cmd = input("Choose: ").strip()
            if cmd == "1":
                name = input("Guest name: ").strip()
                print("1.Standard  2.Deluxe  3.Suite")
                t = int(input("Type#: ")) - 1
                chosen = list(RoomType)[t]
                for r in self.rooms.values():
                    if r.is_available() and r.room_type == chosen:
                        r.status = RoomStatus.OCCUPIED
                        print(f"{name} -> Room {r.number}")
                        break
            elif cmd == "2":
                opts = self.inventory.options()
                for i,o in enumerate(opts,1): print(f"{i}.{o}")
                i = int(input("Choose: ")) - 1
                ok = self.inventory.allocate(opts[i])
                print("Confirmed" if ok else "Unavailable")
            elif cmd == "3":
                base = datetime.combine(date.today(), time(8,0))
                for i,r in self.rooms.items():
                    t = base + timedelta(minutes=20*(i-1))
                    CleaningTask(r, t).execute(self.logs)
                print("All rooms cleaned starting at 08:00")
            elif cmd == "4":
                rn = int(input("Room#: "))
                req = input("Service: ").strip()
                if rn in self.rooms:
                    ServiceTask(self.rooms[rn], req).execute(self.logs)
                    print("Service done")
            elif cmd == "5":
                print("Cleaning:", self.logs["cleaning"])
                print("Service:", self.logs["service"])
            else:
                break

if __name__ == "__main__":
    HotelSystem().run()
"""
