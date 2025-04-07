import hashlib
import os

# --- File where credentials will be stored ---
filename = "users.txt"

# --- Registration Step ---
def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password (minimum 12 characters): ")

    if len(password) < 12:
        print("❌ Password must be at least 12 characters.")
        return

    salt = os.urandom(4)  # 4 bytes = 32 bits
    combined = password.encode() + salt
    hashed_password = hashlib.sha3_256(combined).hexdigest()

    # Convert salt to hex for storage
    salt_hex = salt.hex()

    # Save username, hashed password, and salt to file
    with open(filename, "a") as file:
        file.write(f"{username},{hashed_password},{salt_hex}\n")

    print("✅ Registration complete and data stored securely.\n")


# --- Login Step ---
def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        with open(filename, "r") as file:
            users = file.readlines()

            for user in users:
                stored_username, stored_hash, stored_salt_hex = user.strip().split(",")
                if username == stored_username:
                    stored_salt = bytes.fromhex(stored_salt_hex)
                    combined = password.encode() + stored_salt
                    verify_hash = hashlib.sha3_256(combined).hexdigest()

                    if verify_hash == stored_hash:
                        print("✅ Login successful. User authenticated.")
                        return
                    else:
                        print("❌ Incorrect password.")
                        return
            print("❌ Username not found.")

    except FileNotFoundError:
        print("⚠️ No user data found. Please register first.\n")


# --- Main Menu ---
def main():
    print("Welcome to Garuda Sentinel Login System 🛡️")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option.")

main()
