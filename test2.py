
import uuid
from datetime import datetime

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

class GuestRegistration:
    def __init__(self):
        self.registered_guests = set()
        self.all_guests = []
        self.reservation_system = None  # Will be set by IntegratedHotelSystem
    
    def set_reservation_system(self, reservation_system):
        self.reservation_system = reservation_system
    
    def register_guest(self):
        print("\n--- Hotel Guest Registration ---")
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        gender = input("Enter your gender (M & F): ")
        phone_num = input("Enter your phone number: ")
        email = input("Enter your email: ")
        id_doc = input("Enter your ID document (passport or driver license): ")

        temp_guest = Guest(name, age, gender, phone_num, email, id_doc)
        uid = temp_guest.unique_id()

        if uid in self.registered_guests:
            print("Duplicate entry: A guest with the same name and ID already exists.")
        else:
            self.registered_guests.add(uid)
            self.all_guests.append(temp_guest)
            print(f"\nGuest Registered: {temp_guest.name}")
            print(f"Details: Age {temp_guest.age}, Gender {temp_guest.gender}, "
                  f"Phone {temp_guest.phone_num}, Email {temp_guest.email}, ID {temp_guest.id_doc}")
            print(f"Generated Unique ID: {uid}")
            print("\nIMPORTANT: Registration only adds you to our system.")
            print("You must still CHECK IN (option 4) to get a room and reservation ID.")
        
        return temp_guest
    
    def find_guest(self, name, id_doc):
        uid = f"{name.strip().lower()}-{id_doc.strip().lower()}"
        for guest in self.all_guests:
            if guest.unique_id() == uid:
                return guest
        return None
    
    def show_stats(self):
        print("\n--- Guest Statistics ---")
        print(f"Total registered guests: {len(self.all_guests)}")
        
        # Gender statistics
        male_count = sum(1 for guest in self.all_guests if guest.gender.upper() == 'M')
        female_count = sum(1 for guest in self.all_guests if guest.gender.upper() == 'F')
        
        print(f"Male guests: {male_count}")
        print(f"Female guests: {female_count}")
        
        # Age statistics
        if self.all_guests:
            avg_age = sum(guest.age for guest in self.all_guests) / len(self.all_guests)
            print(f"Average age: {avg_age:.1f}")
        else:
            print("No guests registered yet.")
            
        # Revenue statistics - only if reservation system is connected
        if self.reservation_system:
            self.show_revenue_stats()
    
    def show_revenue_stats(self):
        if not self.reservation_system or not self.reservation_system.reservations:
            print("\n--- Revenue Statistics ---")
            print("No revenue data available yet.")
            return
            
        print("\n--- Revenue Statistics ---")
        
        # Calculate total revenue from completed reservations
        total_revenue = 0
        completed_count = 0
        active_count = 0
        
        # Room type statistics
        standard_count = 0
        deluxe_count = 0
        suite_count = 0
        
        for res_id, reservation in self.reservation_system.reservations.items():
            # Only count completed (checked out) reservations for revenue
            if reservation.checkout_time is not None:
                completed_count += 1
                room_num = reservation.room_number
                
                # Calculate room rate based on room number
                if room_num.startswith("1"):  # Standard room
                    rate = 17000
                    standard_count += 1
                elif room_num.startswith("2"):  # Deluxe room
                    rate = 26000
                    deluxe_count += 1
                else:  # Suite or other
                    rate = 35000
                    suite_count += 1
                
                # Calculate nights stayed (at least 1)
                check_in = reservation.checkin_time
                check_out = reservation.checkout_time
                nights = max(1, (check_out - check_in).days + (1 if (check_out - check_in).seconds > 0 else 0))
                
                # Add to total revenue
                reservation_revenue = nights * rate
                total_revenue += reservation_revenue
            else:
                active_count += 1
                # Count room types for active reservations too
                room_num = reservation.room_number
                if room_num.startswith("1"):
                    standard_count += 1
                elif room_num.startswith("2"):
                    deluxe_count += 1
                else:
                    suite_count += 1
        
        # Display revenue information
        print(f"Total revenue: ${total_revenue:,}")
        print(f"Completed reservations: {completed_count}")
        print(f"Active reservations: {active_count}")
        print(f"Total reservations: {len(self.reservation_system.reservations)}")
        
        # Room type distribution
        print("\nRoom usage:")
        print(f"Standard rooms: {standard_count}")
        print(f"Deluxe rooms: {deluxe_count}")
        print(f"Suite rooms: {suite_count}")
        
        # Revenue by room type (estimate based on room rates)
        standard_revenue = standard_count * 17000
        deluxe_revenue = deluxe_count * 26000
        suite_revenue = suite_count * 35000
        
        print("\nRevenue by room type (completed reservations only):")
        if completed_count > 0:
            print(f"Standard rooms: ${standard_revenue:,} ({standard_revenue/total_revenue*100:.1f}%)")
            print(f"Deluxe rooms: ${deluxe_revenue:,} ({deluxe_revenue/total_revenue*100:.1f}%)")
            print(f"Suite rooms: ${suite_revenue:,} ({suite_revenue/total_revenue*100:.1f}%)")
        else:
            print("No completed reservations yet.")

class ReservationEntry:
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
        # Calculate nights stayed (at least 1)
        check_in = self.checkin_time
        check_out = self.checkout_time
        nights = max(1, (check_out - check_in).days + (1 if (check_out - check_in).seconds > 0 else 0))
        
        if self.room_number.startswith("1"):
            rate = 17000  # Standard
        elif self.room_number.startswith("2"):
            rate = 26000  # Deluxe
        else:
            rate = 35000  # Suite/Other
        total = nights * rate
        return f"Room {self.room_number} (${rate:,}/night) x {nights} night{'s' if nights > 1 else ''} = ${total:,}"

class Reservation:
    def __init__(self):
        self.available_rooms = ["101", "102", "103", "201", "202", "203", "301", "302", "303"]
        self.room_status = {room: False for room in self.available_rooms}  # False = Available
        self.reservations = {}
        self.guest_system = None  # Will be set by IntegratedHotelSystem
    
    def set_guest_system(self, guest_system):
        self.guest_system = guest_system
    
    def list_active_reservations(self):
        """List all active reservations to help users find their reservation ID."""
        if not self.reservations:
            print("\n No active reservations found in the system.")
            return False
            
        print("\n--- Active Reservations ---")
        active_found = False
        for res_id, reservation in self.reservations.items():
            if reservation.checkout_time is None:  # Only show active reservations
                active_found = True
                print(f"ID: {res_id} - {reservation.guest.name} - Room {reservation.room_number} - " 
                      f"Checked in: {reservation.checkin_time.strftime('%Y-%m-%d %H:%M')}")
        
        if not active_found:
            print("No active reservations found.")
            return False
        return True
    
    def check_in(self):
        if self.guest_system is None:
            print("Guest registration system not connected.")
            return
            
        name = input("Enter your name for check-in: ").strip().lower()
        id_doc = input("Enter your ID document: ").strip().lower()
        
        guest = self.guest_system.find_guest(name, id_doc)
        
        if guest is None:
            print("Guest not found. Please register first using option 1.")
            return

        # Display room categories
        print("\nAvailable rooms:")
        print("Standard ($17,000/night): ", end="")
        standard = [r for r in ["101", "102", "103"] if not self.room_status.get(r, True)]
        print(", ".join(standard) if standard else "None available")
        
        print("Deluxe ($26,000/night): ", end="")
        deluxe = [r for r in ["201", "202", "203"] if not self.room_status.get(r, True)]
        print(", ".join(deluxe) if deluxe else "None available")
        
        print("Suite ($35,000/night): ", end="")
        suite = [r for r in ["301", "302", "303"] if not self.room_status.get(r, True)]
        print(", ".join(suite) if suite else "None available")

        available = [r for r, status in self.room_status.items() if not status]
        if not available:
            print("No rooms available.")
            return

        selected = input("Select a room: ").strip()
        if selected not in available:
            print(" Invalid room selection.")
            return

        reservation = ReservationEntry(guest, selected)
        self.reservations[reservation.reservation_id] = reservation
        self.room_status[selected] = True

        print(f"\n Check-in Successful! Reservation ID: {reservation.reservation_id}")
        print(f"Room {selected} assigned. Check-in time: {reservation.checkin_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"\n IMPORTANT: Please write down your reservation ID: {reservation.reservation_id}")
        print("You will need this ID to check out later.")

    def check_out(self):
        # First list all active reservations to help the user
        has_reservations = self.list_active_reservations()
        
        if not has_reservations:
            print("\n You need to check in (option 4) before you can check out!")
            return
            
        res_id = input("\nEnter Reservation ID to check-out: ").strip()
        if res_id not in self.reservations:
            print(" Reservation not found. Please make sure you've checked in first (option 4).")
            print("  If you've already checked in, please verify your reservation ID.")
            return

        reservation = self.reservations[res_id]
        if reservation.checkout_time is not None:
            print(f"This reservation has already been checked out on {reservation.checkout_time.strftime('%Y-%m-%d %H:%M')}.")
            return
            
        reservation.check_out()
        self.room_status[reservation.room_number] = False

        print(f"\n Check-out Successful for {reservation.guest.name}")
        print(f"Room: {reservation.room_number}")
        print(f"Check-in: {reservation.checkin_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Check-out: {reservation.checkout_time.strftime('%Y-%m-%d %H:%M')}")
        print("Invoice:", reservation.get_invoice())