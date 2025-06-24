# MailHook

MailHook is a lightweight FastAPI application that allows users to submit queries along with optional file attachments. Submitted queries are stored in a SQLite database, and email notifications are sent to administrators and managers. The frontend provides a simple form interface served via Jinja2 templates.

The application is now deployed and accessible at: `https://<your-render-service>.onrender.com`

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Running Locally](#running-locally)
  - [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [License](#license)

---

## Features

- **User Query Submission**: Collects username, email, query text, and multiple file attachments via a web form.
- **Database Storage**: Persists users, queries, and files in an SQLite database (`Database/database.db`).
- **Email Notifications**: Sends notifications to admin and manager email addresses upon new query submissions.
- **Simple Frontend**: Jinja2 templates for the form interface, with static assets (CSS, favicon).
- **CORS Support**: Cross-Origin Resource Sharing enabled for broad compatibility.

---

## Prerequisites

- Python 3.9 or higher
- `pip`
- (Optional) Virtual environment tool like `venv` or `conda`

---

## Installation

1. **Clone the repository**
   
```bash
   git clone https://github.com/adityakhode/MailHook.git
   cd MailHook
```

2. **Create and activate a virtual environment (optional but recommended)**

```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\\Scripts\\activate  # Windows
```

3. **Install dependencies**

```bash
   pip install --upgrade pip
   pip install -r requirements.txt
```

---

## Configuration

1. Copy the sample environment file:

```bash
   cp config/.env-shared .env
```

2. Open `.env` and set your email credentials:

```env
   ADMIN_EMAIL="<sender_email@example.com>"
   ADMIN_PASSWORD="<sender_email_password>"
   MANAGER_EMAIL="<wo will get notification email>"
```

3. The app will read these variables on startup to send email notifications.

---

## Project Structure

```
MailHook-main/
├── config/
│   └── .env-shared        # Sample environment variables
├── Database/
│   └── database.db        # SQLite database (auto-created)
├── Src/
│   ├── clearCache.py      # Utility to clear cache files
│   ├── loadCredentials.py # Loads .env and returns email credentials
│   └── mailsender.py      # Sends email notifications
├── templates/
│   ├── assets/            # Static assets (favicon, images)
│   ├── cssFiles/          # Stylesheets
│   └── htmlFiles/
│       └── index.html     # Main form template
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## Usage

### Running Locally

```bash
# Ensure you're in the project root and virtual environment is activated
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser and navigate to `http://localhost:8000` to access the query form.

### API Endpoints

| Method | Endpoint               | Description                                                                              |
| ------ | ---------------------- | ---------------------------------------------------------------------------------------- |
| GET    | `/`                    | Serves the HTML form page                                                                |
| POST   | `/submit/`             | Accepts form data (`username`, `email`, `query`) and files; returns JSON with `query_id` |
| GET    | `/queries/{query_id}/` | Retrieves stored query and filenames as JSON                                             |

Example `curl` request to retrieve a query:

```bash
curl https://<your-render-service>.onrender.com/queries/1/
```

---

## Deployment

This application is deployed on [Render](https://render.com). To deploy your own:

1. Create a new Web Service on Render and connect your GitHub repository.
2. Set the following build commands:

   ```bash
   pip install -r requirements.txt
   ```
3. Set the **Start Command** to:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 80
   ```
4. Add environment variables (`ADMIN_EMAIL`, `ADMIN_PASSWORD`, `MANAGER_EMAIL`) in the Render dashboard.
5. Deploy and visit the provided Render URL.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

```
```
