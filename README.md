# 🏨 Hotel Management System

A console-based hotel management application built with **Python** and **MySQL**. It handles room booking, guest records, check-out billing (with GST and service tax), and searching rooms and customers for the fictional *Hotel Nirvana*.

## Features

- **Room booking**: register a guest, choose a free room, record check-in date, guests and advance payment
- **Room overview**: list all rooms with type, rent, bed type and live status (free / occupied)
- **Bill generation**: automatic check-out, stay duration, GST + service tax, advance deducted, bill saved to the database
- **Search**: look up room status, or search customers by name, address, phone, email, ID type or ID number
- **Hotel info**: view hotel details stored in the database
- **Clear records**: reset customers, bookings and bills (asks for confirmation)

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Language | Python 3.8+                         |
| Database | MySQL 5.7+ / 8.x                    |
| Library  | `mysql-connector-python`, `python-dotenv` |

## Project Structure

```
hotel-management-system/
├── hotel_management.py     # Main application
├── database/
│   └── schema.sql          # Tables + sample rooms + hotel info
├── requirements.txt
├── .env.example            # Template for your DB credentials
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/hotel-management-system.git
cd hotel-management-system
```

### 2. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate        # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

### 3. Set up the database
Make sure MySQL is running, then:
```bash
mysql -u root -p < database/schema.sql
```
This creates the `myproject` database, all tables and sample data (25 rooms).

### 4. Configure credentials
Copy `.env.example` to `.env` and put in your MySQL password:
```bash
copy .env.example .env       # Windows  (macOS/Linux: cp .env.example .env)
```

### 5. Run
```bash
python hotel_management.py
```

## Database Schema

| Table        | Purpose                                         |
|--------------|-------------------------------------------------|
| `customer`   | Guest details and ID proof                      |
| `rooms`      | Room number, type, rent, bed type, status       |
| `booking`    | Links a customer to a room with dates + advance |
| `bill`       | Final bill per booking with GST / service tax   |
| `hotel_info` | Hotel name, address, contact, website           |

## Billing Formula

```
amount  = days_stayed × room_rent        (minimum 1 day)
payable = amount − advance + GST% of amount + service tax% of amount
```
Tax rates default to GST 5% and service tax 2%, and can be changed in `.env`.

## Future Improvements

- Date validation and room availability by date range
- Guest-facing booking receipts (PDF)
- GUI (Tkinter) or web version (Flask / Django)
- Admin login and role-based access

## License

Released under the [MIT License](LICENSE).
