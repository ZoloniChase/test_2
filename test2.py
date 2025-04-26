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
