from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime, date, time, timedelta

# ——— Domain Enums ———————————————————————————————————————————————

class RoomType(Enum):
    STANDARD = "Standard"
    DELUXE = "Deluxe"
    SUITE = "Suite"

class RoomStatus(Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"

# ——— Room & Guest Models —————————————————————————————————————————

class Guest:
    def __init__(self, name: str):
        self.name = name

class Room:
    def __init__(self, number: int, room_type: RoomType):
        self.number = number
        self.room_type = room_type
        self.capacity = {
            RoomType.STANDARD: 2,
            RoomType.DELUXE: 2,
            RoomType.SUITE: 4,
        }[room_type]
        self.amenities = {
            RoomType.STANDARD: ["TV", "Wi-Fi"],
            RoomType.DELUXE: ["TV", "Wi-Fi", "Mini-Bar"],
            RoomType.SUITE: ["TV", "Wi-Fi", "Mini-Bar", "Kitchenette"],
        }[room_type].copy()
        self.status = RoomStatus.AVAILABLE
        self.current_guest: Optional[Guest] = None
        self.cleaning_schedule: List[Dict[str, datetime]] = []

    def is_available(self) -> bool:
        return self.status == RoomStatus.AVAILABLE

# ——— Inventory (Single allocate function) ——————————————————————————————

class Inventory:
    def __init__(self):
        self._items = {
            "extra bed": 5,
            "baby crib": 3,
            "suite upgrade": 2,
            "better view": 4
        }

    def options(self) -> List[str]:
        return list(self._items.keys())

    def count(self, name: str) -> int:
        return self._items.get(name, 0)

    def allocate(self, name: str) -> bool:
        """Allocate one unit of `name`, return True if successful."""
        if self._items.get(name, 0) > 0:
            self._items[name] -= 1
            return True
        return False

# ——— Task & Scheduling Pattern ——————————————————————————————————————

class Task(ABC):
    def __init__(self, room: Room):
        self._room = room
        self._timestamp: Optional[datetime] = None

    @abstractmethod
    def execute(self, logs: Dict[str, List]):
        ...

class CleaningTask(Task):
    def __init__(self, room: Room, scheduled_time: datetime):
        super().__init__(room)
        self._scheduled_time = scheduled_time

    def execute(self, logs: Dict[str, List]):
        self._room.status = RoomStatus.AVAILABLE
        self._timestamp = self._scheduled_time
        logs["cleaning"].append((self._timestamp, self._room.number))

class ServiceTask(Task):
    def __init__(self, room: Room, request_type: str):
        super().__init__(room)
        self._request_type = request_type

    def execute(self, logs: Dict[str, List]):
        self._room.status = RoomStatus.OCCUPIED
        self._timestamp = datetime.now()
        logs["service"].append((self._timestamp, self._room.number, self._request_type))

# ——— Hotel System Controller ———————————————————————————————————————

class HotelSystem:
    SERVICE_OPTIONS = ["New sheets/towels", "Mini bar restock", "Cleaning", "Other"]

    def __init__(self):
        # Initialize 30 rooms: 1–10 Standard, 11–20 Deluxe, 21–30 Suite
        self.rooms: Dict[int, Room] = {
            i: Room(i,
                    RoomType.STANDARD if i <= 10 else
                    RoomType.DELUXE if i <= 20 else
                    RoomType.SUITE)
            for i in range(1, 31)
        }
        self.inventory = Inventory()
        self.logs = {
            "cleaning": [],  # list of (timestamp, room_number)
            "service": []    # list of (timestamp, room_number, request_type)
        }

    def _get_yes_no(self, prompt: str) -> bool:
        while True:
            resp = input(f"{prompt} (yes/no/back): ").strip().lower()
            if resp in ("yes", "y"):
                return True
            if resp in ("no", "n", "back", "b"):
                return False
            print("Enter 'yes', 'no' or 'back'.")

    def _choose_option(self, options: List[str], prompt: str) -> Optional[int]:
        for idx, opt in enumerate(options, 1):
            print(f"{idx}. {opt}")
        while True:
            resp = input(f"{prompt} (or 'back'): ").strip().lower()
            if resp in ("b", "back"):
                return None
            if resp.isdigit() and 1 <= int(resp) <= len(options):
                return int(resp) - 1
            print(f"Enter a number 1–{len(options)}, or 'back'.")

    # — Guest Check-In & Allocation ——————————————————————

    def check_in_guest(self):
        name = input("Guest name: ").strip()
        if not name:
            print("Invalid name.")
            return

        # Room type preference
        types = [rt.value for rt in RoomType]
        idx = self._choose_option(types, "Select room type")
        if idx is None:
            return
        chosen_type = list(RoomType)[idx]

        # Special request at check-in
        if self._get_yes_no("Any upgrade or special request?"):
            self._submit_special_request()

        # Assign first available room
        for room in self.rooms.values():
            if room.is_available() and room.room_type == chosen_type:
                room.current_guest = Guest(name)
                room.status = RoomStatus.OCCUPIED
                print(f"Assigned Guest '{name}' to Room {room.number}")
                return

        print("No available rooms of that type.")

    # — Simplified Special Request Handler —————————————————————————

    def _submit_special_request(self):
        options = self.inventory.options()
        print("\nAvailable special requests:")
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt.title()} ({self.inventory.count(opt)} left)")
        idx = self._choose_option(options, "Choose a request")
        if idx is None:
            return

        req_name = options[idx]
        if self.inventory.allocate(req_name):
            print(f"Confirmed request for '{req_name}'.")
        else:
            print(f"'{req_name}' is unavailable.")

    # — Cleaning Scheduler ——————————————————————————————————

    def run_cleaning_cycle(self):
        base = datetime.combine(date.today(), time(8, 0))
        for i, room in self.rooms.items():
            scheduled = base + timedelta(minutes=20 * (i - 1))
            CleaningTask(room, scheduled).execute(self.logs)
        print("Cleaning cycle scheduled (8:00 start, 20 min intervals).")

    # — Room Service & Maintenance ————————————————————————————

    def handle_service_request(self):
        idx = self._choose_option(self.SERVICE_OPTIONS, "Select service")
        if idx is None:
            return
        req = self.SERVICE_OPTIONS[idx]

        resp = input("Room number (1–30): ").strip()
        if not resp.isdigit() or not (1 <= int(resp) <= 30):
            print("Invalid room number.")
            return
        room_num = int(resp)

        ServiceTask(self.rooms[room_num], req).execute(self.logs)
        print(f"Service '{req}' for Room {room_num} completed.")

    # — Logs Viewer ——————————————————————————————————————————

    def view_logs(self):
        print("\n-- Cleaning Log --")
        for ts, rn in self.logs["cleaning"]:
            print(f"  {ts:%H:%M} – Room {rn}")
        print("\n-- Service Log --")
        for ts, rn, req in self.logs["service"]:
            print(f"  {ts:%H:%M} – Room {rn}, {req}")
        print()

    # — Main Menu —————————————————————————————————————————————

    def run(self):
        while True:
            print(
                "\n1. Check-in guest\n"
                "2. Submit special request\n"
                "3. Run cleaning cycle\n"
                "4. Service request\n"
                "5. View logs\n"
                "6. Exit"
            )
            choice = input("Select 1–6: ").strip()
            if choice == "1":
                self.check_in_guest()
            elif choice == "2":
                self._submit_special_request()
            elif choice == "3":
                self.run_cleaning_cycle()
            elif choice == "4":
                self.handle_service_request()
            elif choice == "5":
                self.view_logs()
            elif choice in ("6", "b", "back"):
                print("Goodbye!")
                break
            else:
                print("Enter a number between 1 and 6 (or 'back').")

if __name__ == "__main__":
    HotelSystem().run()
