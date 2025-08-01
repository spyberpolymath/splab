# 🧪 Splab Elite Hacker Lab

A unified Django dashboard to organize, track, and optimize every aspect of your cybersecurity lab projects. Built for hackers, researchers, and security professionals who want to manage bugs, tools, logs and media in one place.

---

## 🚀 Project Vision

**Goal:** Earn between $100K and $10M via bug bounty programs, real-world security practice, and scalable cybersecurity tools. 

**Philosophy:** _“Build. Hack. Automate. Scale. Protect.”_

**Brand:** `@spyberpolymath`  

---

## ✨ Key Features

- 🐞 **Bug Tracking:** Log, track, and resolve bugs efficiently. Assign issues, set priorities, and monitor progress.
- 📝 **Log Management:** Record, view, and manage lab activity logs for traceability and auditing.
- 🛠️ **Tool Management:** Maintain an organized inventory of lab tools. Link tools to bug
- 🖼️ **Media Files:** Upload, manage, and view media files related to your lab work. Attach images to bugs, tools.
- ✉️ **Contact & Support:** Submit contact messages directly from the dashboard.
- 🔒 **Authentication:** Secure login/logout, dashboard access control.

---

## 🛠️ Technology Stack

- **Backend:** Django 5.2.4
- **Database:** SQLite3 (default, easy to swap)
- **Frontend:** Django Templates, Bootstrap (via CDN), custom CSS
- **Other:** Pillow (media), requests, and more (see requirements.txt)

---

## ⚙️ Setup & Installation

### 1. **Clone the Repo**
```bash
git clone http://github.com/spyberpolymath/splab
cd splab
```

### 2. **Create Virtual Environment**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Database Migration**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. **Create Superuser (for admin access)**
```bash
python manage.py createsuperuser
```

### 6. **Run the Server**
```bash
python manage.py runserver
```
## 🖥️ Usage Guide

- **Dashboard:** View bug, log, tool, and report counts at a glance.
- **Bugs:** Log, track, and resolve issues in your lab projects.
- **Tools:** Manage your lab equipment and software inventory.
- **Media:** Upload and view files for project documentation and evidence.
- **Contact:** Send feedback or support requests.
- **Docs/Setup/Usage:** Access in-app documentation and setup guides.

---

## 🗂️ App Structure & Modules

### **Models**
- **Bug:** Title, description, severity, status, created_at
- **Tool:** Name, version, description
- **LogEntry:** Title, content, timestamp, related_bug, tool_used
- **MediaFile:** File, uploaded_at, related_log, related_bug, related_tool
- **ContactMessage:** Name, email, phone, subject, message, created_at

### **Forms**
- Model forms for each model (BugForm, ToolForm, LogEntryForm, MediaFileForm, ContactForm)

### **Views**
- CRUD for all models (list, detail, create)
- Public: Home, Contact, Docs, Usage, Setup
- Authenticated: Dashboard, Bugs, Logs, Tools, Media

### **Admin**
- Custom admin for all models with search, filters, and read-only fields
---

## 🌐 URL Structure

- `/` – Home
- `/dashboard/` – Dashboard (login required)
- `/bugs/`, `/bugs/create/`, `/bugs/<id>/` – Bug management
- `/logs/`, `/logs/create/`, `/logs/<id>/` – Log management
- `/tools/`, `/tools/create/`, `/tools/<id>/` – Tool management
- `/mediafiles/`, `/mediafiles/create/`, `/mediafiles/<id>/` – Media management
- `/contact/` – Contact form
- `/docs/` – Documentation
- `/usage/` – Usage guide
- `/setup/` – Setup instructions
- `/admin/` – Django admin
- `/accounts/` – Auth (login/logout/password)

---

## 🗃️ Templates & Static Assets

- **Templates:** All major pages (dashboard, bugs, logs, tools, media, contact, docs, setup, usage, etc.)
- **Static:** Custom CSS in `static/css/setup.css` for enhanced visuals

---

## 🗺️ Project Roadmap & Phases

### **Phase 1: Complete Lab Setup**
- Hardware, OS, tools, and study sources for cybersecurity mastery

### **Phase 2: Bug Bounties & Tool Development**
- Start on bug bounty platforms, build custom tools, automate workflows

### **Phase 3: Scale Earnings & AI Automation**
- Private programs, AI-powered pipelines, cyber intelligence, and defense

### **Phase 4: Enterprise & Government Deployment**
- Build and deploy tools for BFSI, healthcare, government, education, and more

### **Phase 5: Define Your Legacy**
- Become a thought leader, educator, and innovator in cybersecurity

---

## 🏆 Credits & Motivation

> _Stay curious, keep building, and never stop learning. The future belongs to those who create it._

---

⚠️ **For educational and ethical hacking purposes only!**

🛡️ Use responsibly, legally, and with integrity. The authors are not responsible for any misuse.

©️ 2025 Spyber Polymath | 🧑‍💻 Stay ethical, stay curious!

---