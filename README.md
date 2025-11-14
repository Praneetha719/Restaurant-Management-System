🍽️ Restaurant Management System (Flask + SQLite)

A simple and efficient Restaurant Management System built using Flask, SQLite, and Jinja2 templates, featuring Admin and Cashier user roles.
This project manages menu items, orders, user access, and billing in a lightweight web environment.

📌 Features
🔑 User Roles
👨‍💼 Admin

Add, edit, and delete menu items

Manage user accounts (add/edit/delete Cashiers)

View daily and monthly sales reports

Full control over menu & system settings

💵 Cashier

Create customer orders

Add menu items to cart

Generate and print bills

View only menu items (no editing)

Handles customer checkouts

🧾 Core Modules
🍔 Menu Management (Admin)

Add new food items (name, price, category)

Edit item details

Delete menu items

Menu automatically updates for Cashiers

🛒 Order & Billing System (Cashier)

Select items and add to order cart

Auto calculation of total + taxes

Discount option (manual or predefined)

Generates printable invoice

Saves order to database

📊 Reports (Admin)

Total sales for the day

Order count

Sales grouped by Cashier

Export reports to CSV

👥 Authentication System

Secure login

Password hashing

Role-based access control (Admin/Cashier)

🛠️ Tech Stack
Layer	Technology
Backend	Flask
Database	SQLite
Frontend	HTML, CSS, JavaScript
Templates	Jinja2
Authentication	Flask Sessions
Reporting (optional)	Chart.js
📁 Project Structure
restaurant_management_system/
│── app.py
│── auth.py
│── database.py
│── requirements.txt
│── README.md
│
├── instance/
│   └── restaurant.db
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── cashier_dashboard.html
│   ├── menu.html
│   ├── add_item.html
│   ├── update_item.html
│   ├── order_page.html
│   └── bill.html
│
└── models/
    └── menu_model.py

▶️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/restaurant-management-system
cd restaurant-management-system

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Initialize the Database
python database.py

4️⃣ Run the Application
python app.py

🌐 Access the App

Visit in your browser:

http://127.0.0.1:5000

📸 Screenshots (Add After Uploading)

Add the following images in your GitHub repo and embed them:

![Login Page](screenshots/login.png)
![Admin Dashboard](screenshots/admin_dashboard.png)
![Cashier Order Page](screenshots/order_page.png)
![Generated Bill](screenshots/bill.png)

🔮 Future Enhancements

Inventory management

Table reservation system

Printer support for receipts

GST/Tax configuration panel

Customer mobile ordering app

Dark mode UI

Role-based dashboards with charts

🤝 Contribution

Contributions are welcome!
Feel free to submit pull requests or open issues.

📜 License

This project is licensed under the MIT License.
