
class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.is_occupied = False
        self.requires_cleaning = False
        self.maintenance_needed = False

    def display_info(self):
        status = "Occupied" if self.is_occupied else "Available"
        cleaning = "Needs cleaning" if self.requires_cleaning else "Clean"
        maintenance = "Needs maintenance" if self.maintenance_needed else "Good condition"
        return f"Room {self.room_number} ({self.room_type}) - ${self.price}/night - {status}, {cleaning}, {maintenance}"

class HotelSystem:
    def __init__(self):
        self.rooms = []
        self._initialize_rooms()
    
    def _initialize_rooms(self):
        # Standard rooms
        for i in range(101, 104):
            self.rooms.append(Room(str(i), "Standard", 17000))
        
        # Deluxe rooms
        for i in range(201, 204):
            self.rooms.append(Room(str(i), "Deluxe", 26000))
        
        # Suite rooms
        for i in range(301, 304):
            self.rooms.append(Room(str(i), "Suite", 35000))
    
    def view_all_rooms(self):
        print("\n--- All Rooms ---")
        for room in self.rooms:
            print(room.display_info())
    
    def view_available_rooms(self):
        print("\n--- Available Rooms ---")
        available = [room for room in self.rooms if not room.is_occupied]
        
        if not available:
            print("No rooms available at the moment.")
            return
        
        for room in available:
            print(room.display_info())
    
    def set_room_status(self):
        room_number = input("Enter room number: ")
        room = self._find_room(room_number)
        
        if not room:
            print("Room not found.")
            return
        
        print(f"\nCurrent status for Room {room_number}:")
        print(f"Occupied: {room.is_occupied}")
        print(f"Needs cleaning: {room.requires_cleaning}")
        print(f"Needs maintenance: {room.maintenance_needed}")
        
        print("\nUpdate status:")
        print("1. Toggle occupied status")
        print("2. Toggle cleaning status")
        print("3. Toggle maintenance status")
        choice = input("Select option (1-3): ")
        
        if choice == "1":
            room.is_occupied = not room.is_occupied
            print(f"Room {room_number} is now {'occupied' if room.is_occupied else 'available'}")
        elif choice == "2":
            room.requires_cleaning = not room.requires_cleaning
            print(f"Room {room_number} {'needs cleaning' if room.requires_cleaning else 'is clean'}")
        elif choice == "3":
            room.maintenance_needed = not room.maintenance_needed
            print(f"Room {room_number} {'needs maintenance' if room.maintenance_needed else 'is in good condition'}")
        else:
            print("Invalid choice")
    
    def _find_room(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number:
                return room
        return None
    
    def run(self):
        while True:
            print("\n--- Room Management ---")
            print("1. View all rooms")
            print("2. View available rooms")
            print("3. Update room status")
            print("4. Return to main menu")
            
            choice = input("Select option (1-4): ")
            
            if choice == "1":
                self.view_all_rooms()
            elif choice == "2":
                self.view_available_rooms()
            elif choice == "3":
                self.set_room_status()
            elif choice == "4":
                return
            else:
                print("Invalid choice")