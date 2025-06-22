import os
from session import get_session


if __name__=="__main__":

    if not os.path.exists(".env"):
        password_inputs = input(">>> Enter your password (4 x 3) eg aaaa-bbbb-cccc > ")
    else:
        password_inputs = open(".env", "r").read().strip()

    print(">>> Starting session...")
    
    sesssion = get_session(password_inputs)

    print(">>> Session created successfully!")

    while True:
        try:
            command = input("> ").strip().lower()
        except KeyboardInterrupt:
            break

        if command == "update_name" or command == "un":
            new_name = input(">>> Enter new name: ").strip()
            sesssion.update_name(new_name)
            print(f">>> Name updated to: {new_name}")

        elif command == "upload_picture" or command == "up":
            pic_path = input(">>> Enter picture path: ").strip()
            sesssion.upload_picture(pic_path)
            print(f">>> Picture uploaded from: {pic_path}")

        elif command == "test" or command == "t":
            if sesssion.test():
                print(">>> Session is active and valid.")
            else:
                print(">>> Session is inactive or invalid, renewing...")
                sesssion.renew()