# 📄 Resume-GPT

**Resume-GPT** is a Django-based web application designed to assist users in building professional resumes. The application provides a user-friendly interface for inputting personal and professional information, which is then formatted into a structured resume.

---

## 🚀 Features

- 📝 Input personal details, education, work experience, and skills
- 📄 Generate a formatted resume based on user input
- 💾 Save resumes for future editing or downloading
- 🔒 Secure handling of user data

---

## 🛠 Tech Stack

| Tool / Tech | Purpose                          |
|-------------|----------------------------------|
| Python      | Core programming language        |
| Django      | Web framework for backend        |
| HTML/CSS    | Frontend structure and styling   |
| JavaScript  | Frontend interactivity           |

---

## 📁 Folder Structure

```
Resume-GPT/
├── resume_builder/          # Main application directory
│   ├── templates/           # HTML templates
│   ├── static/              # Static files (CSS, JS)
│   ├── __init__.py          # Package initialization
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # Application configuration
│   ├── models.py            # Database models
│   ├── tests.py             # Test cases
│   ├── urls.py              # URL routing
│   └── views.py             # View functions
├── Resume-GPT/              # Project configuration directory
│   ├── __init__.py          # Package initialization
│   ├── asgi.py              # ASGI configuration
│   ├── settings.py          # Project settings
│   ├── urls.py              # Project URL routing
│   └── wsgi.py              # WSGI configuration
├── db.sqlite3               # SQLite database file
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```
git clone https://github.com/Sahil24680/Resume-GPT.git
cd Resume-GPT
```

### 2. Set Up the Virtual Environment

```
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Apply Migrations

```
python manage.py migrate
```

### 5. Run the Development Server

```
python manage.py runserver
```

### 6. Access the Application

Open your browser and navigate to:

```
http://127.0.0.1:8000
```

---


