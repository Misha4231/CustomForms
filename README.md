# Custom Forms

## 📌 Overview
This project is a clone of **Google Forms** built with **Django**, **GraphQL** and **Vue.js**. It features real-time form creation and editing.
Users can submit answers and review them.

## 🛠️ Tech Stack
- **Django** – Backend framework
- **GraphQL** – Web API
- **SQLite3** – Lightweight database for storing user and game state
- **Vue.js** – Frontend

## 📦 Installation & Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Apply Migrations
```bash
python manage.py migrate
```

### 3. Run Django Development Server
```bash
python manage.py runserver
```

### 4. Install npm packages
```bash
cd frontend
npm i
```

### 4. Run Vue.js Development Server
```bash
cd frontend
npm run dev
```