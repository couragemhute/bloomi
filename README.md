

# Bloomi Website – Django Version

This project was originally built with pure **HTML & CSS**, but we are now migrating to **Django** to add backend functionality.

The goal is to keep the existing front-end templates while adding backend features (authentication, database integration, API connections, etc.).

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/couragemhute/bloomi.git
cd bloomi
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

* **Mac/Linux**

  ```bash
  source venv/bin/activate
  ```

* **Windows**

  ```bash
  venv\Scripts\activate
  ```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment Variables

Create a `.env` file in the project root (⚠️ never commit this file).

Example `.env`:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

👉 Ask the backend team if any extra keys (like API tokens) are required.

---

### 5. Database Setup

```bash
python manage.py migrate
```

(Optional: create a superuser for admin panel)

```bash
python manage.py createsuperuser
```

---

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit the site at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🖼 Templates & Static Files

### Where to Add Your HTML/CSS:

* **Templates** → Place HTML files in:

  ```
  project_name/templates/
  ```
* **Static files (CSS/JS/images)** → Place them in:

  ```
  project_name/static/
  ```

Example:

```
project_name/
templates/
├── layouts/
│   ├── base.html       # main HTML skeleton, includes header, footer, scripts
│   ├── header.html     # site header
│   ├── footer.html     # site footer
│   └── scripts.html    # JS scripts includes
├── home/
│   └── index.html      # homepage content, extends layouts/base.html
├── contact/
│   └── index.html      # contact page content, extends layouts/base.html
├── blog/
│   └── index.html      # blog listing page, extends layouts/base.html
├── about/
│   └── index.html      # about page, extends layouts/base.html
└── other_pages/
    └── index.html      # other pages, same structure

└── static/assets/
    ├── css/
    │   └── styles.css
    ├── js/
    │   └── scripts.js
    └── images/
        └── logo.png
```

In Django templates, use:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

---

## 🛠 Development Workflow

1. **Frontend Team**

   * Focus on editing templates inside `templates/`
   * Update CSS/JS inside `static/`
   * Work with `base.html` for shared layouts.

2. **Backend Team**

   * Add models, views, and routes in Django apps.
   * Connect templates to dynamic data.

---

## 🤝 Contributing

* Create a new branch for your feature:

  ```bash
  git checkout -b feature-name
  ```
* Commit your changes:

  ```bash
  git commit -m "Added about page template"
  ```
* Push and open a pull request.

---

## 📌 Notes

* Never commit `.env` or secrets.
* Keep frontend assets inside `static/`.



## Environment Variables

This project uses environment variables for configuration, such as debug mode, allowed hosts, secret key, and email settings.

### Steps to set up your `.env` file:

1. **Create a new `.env` file** in the project root:

```bash
touch .env
```

2. **Copy the example contents** below into your `.env` file:

```dotenv
# Debug mode
DEBUG="True"

ALLOWED_HOSTS="localhost,127.0.0.1"

# Secret key (replace with your own secret in production)
SECRET_KEY="your-secret-key-here"

# Email configuration
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.your-email-provider.com"
EMAIL_PORT="465"
EMAIL_USE_TLS="False"
EMAIL_USE_SSL="True"
EMAIL_HOST_USER="your-email@example.com"
EMAIL_HOST_PASSWORD="your-email-password"
DEFAULT_FROM_EMAIL="webmaster@localhost"
```

3. **Update the values** as needed for your local environment:

* `SECRET_KEY` – generate a secure key for Django
* `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` – your email credentials

> ⚠️ **Important:** Do **not** commit your `.env` file to version control.



