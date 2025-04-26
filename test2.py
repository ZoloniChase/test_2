import uuid
from datetime import datetime
registered_guests = set()
all_guests = []

class Guest:
    def __init__(self, name, age, gender, phone_num, email, id_doc):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone_num = phone_num
        self.email = email
        self.id_doc = id_doc

    def unique_id(self):
        return f"{self.name.strip().lower()}-{self.id_doc.strip().lower()}"

while True:
    print("\n--- Hotel Guest Registration ---")
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (M & F): ")
    phone_num = input("Enter your phone number: ")
    email = input("Enter your email: ")
    id_doc = input("Enter your ID document (passport or driver license): ")

    temp_guest = Guest(name, age, gender, phone_num, email, id_doc)
    uid = temp_guest.unique_id()

    if uid in registered_guests:
        print("❌ Duplicate entry: A guest with the same name and ID already exists.")
    else:
        registered_guests.add(uid)
        all_guests.append(temp_guest)
        print(f"\n✅ Guest Registered: {temp_guest.name}")
        print(f"Details: Age {temp_guest.age}, Gender {temp_guest.gender}, "
              f"Phone {temp_guest.phone_num}, Email {temp_guest.email}, ID {temp_guest.id_doc}")
        print(f"Generated Unique ID: {uid}")

    again = input("\nRegister another guest? (y/n): ").strip().lower()
    if again != 'y':
        break
    # Room and reservation data
available_rooms = ["(Standard ->)","101", "102", "103","(Deluxe ->)","201", "202","203","(Suite ->)","301","302","303"]
room_status = {room: False for room in available_rooms}  # False = Available
reservations = {}

# Reservation class
class Reservation:
    def __init__(self, guest, room_number):
        self.reservation_id = str(uuid.uuid4())[:8]
        self.guest = guest
        self.room_number = room_number
        self.checkin_time = datetime.now()
        self.checkout_time = None
        self.paid = False

    def check_out(self):
        self.checkout_time = datetime.now()
        self.paid = True

    def get_invoice(self):
        nights = 1  # Static for now
        if self.room_number.startswith("1"):
            rate = 17000  # Standard
        elif self.room_number.startswith("2"):
            rate = 26000  # Deluxe
        else:
            rate = 35000  # Suite/Other
        total = nights * rate
        return f"Room {self.room_number} (${rate}/night) x {nights} night = ${total}"

# Check-in function
def check_in_guest():
    name = input("Enter your name for check-in: ").strip().lower()
    id_doc = input("Enter your ID document: ").strip().lower()
    uid = f"{name}-{id_doc}"

    guest = None
    for g in all_guests:
        if g.unique_id() == uid:
            guest = g
            break

    if guest is None:
        print("❌ Guest not found. Please register first.")
        return

    available = [r for r, status in room_status.items() if not status]
    if not available:
        print("❌ No rooms available.")
        return

    print("Available rooms:", ", ".join(available))
    selected = input("Select a room: ").strip()
    if selected not in available:
        print("❌ Invalid room selection.")
        return

    reservation = Reservation(guest, selected)
    reservations[reservation.reservation_id] = reservation
    room_status[selected] = True

    print(f"\n✅ Check-in Successful! Reservation ID: {reservation.reservation_id}")
    print(f"Room {selected} assigned. Check-in time: {reservation.checkin_time.strftime('%Y-%m-%d %H:%M')}")

# Check-out function
def check_out_guest():
    res_id = input("Enter Reservation ID to check-out: ").strip()
    if res_id not in reservations:
        print("❌ Reservation not found.")
        return

    reservation = reservations[res_id]
    reservation.check_out()
    room_status[reservation.room_number] = False

    print(f"\n✅ Check-out Successful for {reservation.guest.name}")
    print(f"Room: {reservation.room_number}")
    print(f"Check-in: {reservation.checkin_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"Check-out: {reservation.checkout_time.strftime('%Y-%m-%d %H:%M')}")
    print("💸 Invoice:", reservation.get_invoice())

# Menu
while True:
    print("\n--- Hotel System Menu ---")
    print("1. Register Guest")
    print("2. Check-in Guest")
    print("3. Check-out Guest")
    print("4. Exit")
    choice = input("Choose option: ").strip()

    if choice == "1":
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        gender = input("Enter your gender (M & F): ")
        phone_num = input("Enter your phone number: ")
        email = input("Enter your email: ")
        id_doc = input("Enter your ID document (passport or driver license): ")

        temp_guest = Guest(name, age, gender, phone_num, email, id_doc)
        uid = temp_guest.unique_id()

        if uid in registered_guests:
            print("❌ Duplicate entry: Guest already exists.")
        else:
            registered_guests.add(uid)
            all_guests.append(temp_guest)
            print(f"\n✅ Guest Registered: {temp_guest.name}")
            print(f"Generated Unique ID: {uid}")

    elif choice == "2":
        check_in_guest()

    elif choice == "3":
        check_out_guest()

    elif choice == "4":
        print("👋😁 Bye! Come again.")
        break

    else:
        print("Invalid choice.")