
from room_management import HotelSystem
from test2 import GuestRegistration, Reservation
from user_auth import AuthenticationSystem

class IntegratedHotelSystem:
    def __init__(self):
        self.hotel_system = HotelSystem()
        self.guest_system = GuestRegistration()
        self.reservation_system = Reservation()
        self.auth_system = AuthenticationSystem()
        
        # Connect the systems bidirectionally
        self.reservation_system.set_guest_system(self.guest_system)
        self.guest_system.set_reservation_system(self.reservation_system)
    
    def show_workflow_guide(self):
        print("\n=== Hotel System Workflow Guide ===")
        print("1. Register as a guest (option 1)")
        print("2. Check in to get a room (option 4)")
        print("3. Note your reservation ID when you check in")
        print("4. When ready, check out using your ID (option 5)")
        print("5. View revenue statistics (option 3)")
    
    def show_main_menu(self):
        # Require login first
        if not self.auth_system.current_user:
            if not self.auth_system.login():
                return
        
        # Show the workflow guide at startup
        self.show_workflow_guide()
        
        while True:
            print(f"\n=== Hotel Management System ({self.auth_system.current_user.role.replace('_', ' ')}) ===")
            print("1. Guest Registration")
            print("2. Room Management")
            print("3. View Guest & Revenue Statistics")
            print("4. Check-in Guest")
            print("5. Check-out Guest")
            print("6. Show How To Use")
            print("7. Switch User")
            print("8. Exit")
            
            choice = input("Select option (1-8): ").strip()
            
            if choice == "1":
                if self.auth_system.require_permission('front_desk'):
                    self.guest_system.register_guest()
            elif choice == "2":
                if self.auth_system.require_permission('front_desk'):
                    self.hotel_system.run(self.auth_system.current_user.role)
            elif choice == "3":
                if self.auth_system.require_permission('manager'):
                    self.guest_system.show_stats()
                    self.guest_system.show_revenue_stats()
            elif choice == "4":
                if self.auth_system.require_permission('front_desk'):
                    self.reservation_system.check_in()
            elif choice == "5":
                if self.auth_system.require_permission('front_desk'):
                    self.reservation_system.check_out()
            elif choice == "6":
                self.show_workflow_guide()
            elif choice == "7":
                self.auth_system.logout()
                if not self.auth_system.login():
                    break
            elif choice == "8":
                self.auth_system.logout()
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    system = IntegratedHotelSystem()
    system.show_main_menu()