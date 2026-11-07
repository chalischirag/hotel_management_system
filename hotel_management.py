"""Hotel Nirvana - Hotel Management System (Python + MySQL, console based)."""
import os
from datetime import date

import mysql.connector

# python-dotenv is optional; env vars can be set manually
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  
    pass

GST_PERCENT = float(os.getenv("GST_PERCENT", 5))
SERVICE_TAX_PERCENT = float(os.getenv("SERVICE_TAX_PERCENT", 2))

# you can set the env vars according to your system host and user.

def get_connection():
    """Open a MySQL connection using settings from environment / .env file."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "myproject"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
    )


def clear():
    print("\n" * 60)


def pause():
    input("\n\nPress Enter to continue...")


def ask_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        return None


def get_room(cursor, room_no):
    cursor.execute("SELECT * FROM rooms WHERE room_no = %s", (room_no,))
    return cursor.fetchone()


# ---------------------------------------------------------------- features
def hotel_info():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, field_name, value FROM hotel_info")
    for row in cursor.fetchall():
        print("{} | {:15s} : {}".format(*row))
    conn.close()
    pause()


def rooms():
    clear()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT room_no, room_type, room_rent, room_bed, status FROM rooms")
    print("{:8s}{:16s}{:12s}{:14s}{}".format("Room", "Type", "Rent", "Bed", "Status"))
    print("-" * 65)
    for r in cursor.fetchall():
        print("{:<8}{:16s}{:<12}{:14s}{}".format(r[0], r[1], r[2], r[3], r[4]))
    conn.close()
    pause()


def room_booking():
    clear()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    room_no = input("Enter room no to book: ")
    room = get_room(cursor, room_no)
    if room is None:
        print("Room does not exist.")
    elif room["status"] != "free":
        print("Room is not available. Right now it is", room["status"])
    else:
        name = input("Customer name: ")
        address = input("Customer address: ").upper()
        phone = input("Customer phone no: ")
        email = input("Customer email: ").upper()
        id_proof = input("ID type (Aadhar/Passport/DL/VoterID): ").upper()
        id_proof_no = input("ID proof no: ").upper()

        cursor.execute(
            "INSERT INTO customer (name, address, phone, email, id_proof, id_proof_no) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (name, address, phone, email, id_proof, id_proof_no),
        )
        cust_id = cursor.lastrowid
        print("Your customer id is:", cust_id)
        print("-" * 60)

        check_in = input("Date of occupancy (yyyy-mm-dd): ")
        guests = ask_int("Number of guests: ") or 1
        try:
            advance = float(input("Advance amount: "))
        except ValueError:
            advance = 0.0

        cursor.execute("UPDATE rooms SET status = 'occupied' WHERE room_no = %s", (room_no,))
        cursor.execute(
            "INSERT INTO booking (room_id, cust_id, check_in, guests, advance) "
            "VALUES (%s, %s, %s, %s, %s)",
            (room_no, cust_id, check_in, guests, advance),
        )
        conn.commit()
        print("\nRoom {} booked for customer id {}".format(room_no, cust_id))
    conn.close()
    pause()


def bill_generation():
    clear()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    room_no = input("Enter room no: ")
    cust_id = input("Enter customer ID: ")

    cursor.execute(
        "SELECT * FROM booking WHERE cust_id = %s AND room_id = %s AND check_out IS NULL",
        (cust_id, room_no),
    )
    booking = cursor.fetchone()
    room = get_room(cursor, room_no)
    if booking is None or room is None:
        print("No active booking found for this room and customer.")
        conn.close()
        pause()
        return

    check_in, check_out = booking["check_in"], date.today()
    total_days = max((check_out - check_in).days, 1)  # minimum one day charged
    rent = float(room["room_rent"])
    advance = float(booking["advance"] or 0)
    amount = total_days * rent
    gst_amount = amount * GST_PERCENT / 100
    st_amount = amount * SERVICE_TAX_PERCENT / 100
    payable = amount - advance + gst_amount + st_amount

    cursor.execute("UPDATE rooms SET status = 'free' WHERE room_no = %s", (room_no,))
    cursor.execute("UPDATE booking SET check_out = %s WHERE book_id = %s",
                   (check_out, booking["book_id"]))
    cursor.execute(
        "INSERT INTO bill (book_id, amount, bill_date, gst, st) VALUES (%s, %s, %s, %s, %s)",
        (booking["book_id"], payable, check_out, GST_PERCENT, SERVICE_TAX_PERCENT),
    )
    bill_no = cursor.lastrowid
    conn.commit()

    clear()
    print("BILL")
    print("-" * 60)
    print("Bill no            :", bill_no)
    print("Room               :", room_no)
    print("Date of occupancy  :", check_in)
    print("Date of leaving    :", check_out)
    print("Total days         :", total_days)
    print("Room rent per day  :", rent)
    print("Total amount       :", amount)
    print("Advance paid       :", advance)
    print("GST ({}%)         : {:.2f}".format(GST_PERCENT, gst_amount))
    print("Service tax ({}%) : {:.2f}".format(SERVICE_TAX_PERCENT, st_amount))
    print("Amount payable     : {:.2f}".format(payable))
    conn.close()
    pause()


def search_rooms():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    room = get_room(cursor, input("Enter room no: "))
    clear()
    if room is None:
        print("Room not found.")
    else:
        print("Room Status\n" + "*" * 40)
        print("Room no   :", room["room_no"])
        print("Room type :", room["room_type"])
        print("Room rent :", room["room_rent"])
        print("Room bed  :", room["room_bed"])
        print("Status    :", room["status"])
    conn.close()
    pause()


SEARCH_FIELDS = {1: "name", 2: "address", 3: "phone", 4: "email",
                 5: "id_proof", 6: "id_proof_no"}  # whitelist -> safe in SQL


def search_customer():
    clear()
    print("Search Customer Database\n" + "*" * 40)
    print("0. All customers\n1. Name\n2. Address\n3. Phone\n4. Email\n"
          "5. ID proof type\n6. ID proof number")
    choice = ask_int("Enter your choice: ")
    conn = get_connection()
    cursor = conn.cursor()
    if choice == 0:
        cursor.execute("SELECT * FROM customer")
        label = "ALL"
    elif choice in SEARCH_FIELDS:
        field = SEARCH_FIELDS[choice]
        value = input("Enter value to search: ")
        cursor.execute("SELECT * FROM customer WHERE {} LIKE %s".format(field),
                       ("%" + value + "%",))
        label = "{} = {}".format(field, value)
    else:
        print("Invalid choice.")
        conn.close()
        pause()
        return
    records = cursor.fetchall()
    clear()
    print("Search result for", label)
    print("*" * 120)
    print("{:<5}{:20s}{:30s}{:15s}{:30s}{:15s}{}".format(
        "ID", "Name", "Address", "Phone", "Email", "ID Used", "ID No"))
    for r in records:
        print("{:<5}{:20s}{:30s}{:15s}{:30s}{:15s}{}".format(*[str(x or "") for x in r]))
    conn.close()
    pause()


def search_menu():
    while True:
        clear()
        print(" Search Menu\n" + "*" * 40)
        print("\n1. Room status\n2. Customer details\n3. Back to main menu\n")
        choice = ask_int("Enter your choice: ")
        if choice == 1:
            search_rooms()
        elif choice == 2:
            search_customer()
        elif choice == 3:
            break


def clear_records():
    clear()
    if input("This deletes ALL customers, bookings and bills. Type YES to confirm: ") != "YES":
        print("Cancelled.")
        pause()
        return
    conn = get_connection()
    cursor = conn.cursor()
    for table in ("customer", "booking", "bill"):
        cursor.execute("TRUNCATE TABLE " + table)
    cursor.execute("UPDATE rooms SET status = 'free'")
    conn.commit()
    conn.close()
    print("All records cleared.")
    pause()


def main_menu():
    actions = {1: room_booking, 2: rooms, 3: bill_generation,
               4: search_menu, 5: hotel_info, 6: clear_records}
    while True:
        clear()
        print(" H O T E L   N I R V A N A ")
        print("*" * 60)
        print("\n1. Room booking\n2. Rooms\n3. Bill generation\n4. Search details"
              "\n5. Hotel info\n6. Clear records\n7. Exit\n")
        choice = ask_int("Enter your choice: ")
        if choice == 7:
            break
        if choice in actions:
            actions[choice]()
        else:
            input("Please enter a valid choice. Press Enter...")


if __name__ == "__main__":
    main_menu()
