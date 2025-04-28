# index.py
from room_management import HotelSystem
from test2 import GuestRegistration, Reservation

class IntegratedHotelSystem:
    def __init__(self):
        self.hotel_system = HotelSystem()
        self.guest_system = GuestRegistration()
        self.reservation_system = Reservation()
        
        # Connect the systems bidirectionally
        self.reservation_system.set_guest_system(self.guest_system)
        self.guest_system.set_reservation_system(self.reservation_system)
    
    def show_workflow_guide(self):

        print("1. Register as a guest (option 1)")
        print("2. Check in to get a room (option 4)")
        print("3. Note your reservation ID when you check in")
        print("4. When ready, check out using your ID (option 5)")
        print("5. View revenue statistics (option 3)")
    
    def show_main_menu(self):
        # Show the workflow guide at startup
        self.show_workflow_guide()
        
        while True:
            print("\n=== Hotel Management System ===")
            print("1.Guest Registration")
            print("2.Room Management")
            print("3.View Guest & Revenue Statistics")
            print("4.Check-in Guest")
            print("5.Check-out Guest")
            print("6.Show How To Use")
            print("7.Exit")
            
            choice = input("Select option (1-7): ").strip()
            
            if choice == "1":
                self.guest_system.register_guest()
            elif choice == "2":
                self.hotel_system.run()
            elif choice == "3":
                self.guest_system.show_stats()
            elif choice == "4":
                self.reservation_system.check_in()
            elif choice == "5":
                self.reservation_system.check_out()
            elif choice == "6":
                self.show_workflow_guide()
            elif choice == "7":
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    system = IntegratedHotelSystem()
    system.show_main_menu()