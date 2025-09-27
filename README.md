# 🏗️ StavMat

**StavMat** is a management system for construction companies, built with **Django**.  
It provides tools to manage materials, customers, employees, and invoices in one place,  
with a secure admin panel and authentication system.

---

## ✨ Features

- ✅ Add and manage **Materials**
- ✅ Add and manage **Customers**
- ✅ Add and manage **Employees**
- ✅ Track **Invoices**
- ✅ Track **Material**
- ✅ Admin panel for full database control
- 🔐 Secure user authentication with Django's built-in system
- 👥 **Role-based access control** – different roles (e.g. Admin, Manager, Employee)  
  have different permissions and access levels across the web application

---

## 🧑‍💻 Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** Django templates + Bootstrap
- **Authentication:** Django built-in auth system with role-based access  

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/kostelnikp/StavMat.git
cd StavMat
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
## 🔑 Admin Panel
 - URL: http://127.0.0.1:8000/admin/
 - Use the superuser credentials you created.
 - From here you can fully manage materials, customers, employees, and invoices.

## 📸 API Communication

### Homepage
![Homepage](/Screenshots/Homepage.jpg?raw=true "Homepage")

### Employees
![Employees](/Screenshots/Employees.jpg?raw=true "Exercise")

### Invoices
![Workout](/Screenshots/Invoices.jpg?raw=true "Workout")

