
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role  # 'manager', 'front_desk', 'housekeeping'

class AuthenticationSystem:
    def __init__(self):
        self.users = {
            'manager1': User('manager1', 'mgr123', 'manager'),
            'frontdesk1': User('frontdesk1', 'fd123', 'front_desk'),
            'housekeeping1': User('housekeeping1', 'hk123', 'housekeeping')
        }
        self.current_user = None
    
    def login(self):
        print("\n--- Login ---")
        username = input("Username: ")
        password = input("Password: ")
        
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Welcome, {user.username} ({user.role.replace('_', ' ')})!")
            return True
        else:
            print("Invalid credentials")
            return False
    
    def logout(self):
        if self.current_user:
            print(f"Goodbye, {self.current_user.username}!")
            self.current_user = None
        else:
            print("No user is currently logged in")
    
    def has_permission(self, required_role):
        if not self.current_user:
            return False
        # Manager has all permissions
        if self.current_user.role == 'manager':
            return True
        # Front desk can do most things except some admin functions
        if required_role == 'front_desk' and self.current_user.role == 'front_desk':
            return True
        # Housekeeping has limited access
        if required_role == 'housekeeping' and self.current_user.role == 'housekeeping':
            return True
        return False
    
    def require_permission(self, required_role):
        if not self.has_permission(required_role):
            print(f"Access denied. {required_role.replace('_', ' ')} privileges required.")
            return False
        return True