# Chathurya Student Developers Club — Technical Workshop Website

A modern, responsive, student-friendly website portal for **Chathurya Student Developers Club** technical workshops.

Built with **HTML5, CSS3, and vanilla JavaScript**, the design features a SaaS-inspired minimal dark interface with neon lime accents (`#b6ff00`), clean typography, interactive form validation, and responsive page navigation.

---

## 📁 Project Folder Structure

```
college-workshop/
│
├── index.html             # Homepage / Main Entry Point (Hero, About Us, Previous Events, Courses, Footer)
├── courses.html           # Dedicated Courses Catalog Page (Full Stack & Data Analytics Cards)
├── fullstack.html         # Full Stack Development Workshop Syllabus & Capstone Page
├── data-analytics.html    # Data Analytics Workshop Syllabus & Capstone Page
├── registration.html      # 9-Field Registration Form & Live Confirmation Page
├── server.py              # Custom Secure Development Server Script (No Directory Listing)
├── README.md              # Project Documentation & Run Procedure
│
├── css/
│   └── style.css          # Core Styling (Design Variables, Reset, Cards, SaaS Layouts, Responsive Rules)
│
├── js/
│   ├── main.js            # Navbar Navigation, Theme Switcher (Dark/Light), Mobile Drawer, Smooth Scroll
│   └── registration.js    # 9-Field Real-Time Form Validation, LocalStorage Caching, Success View Render
│
└── images/
    ├── logo.svg / .png                   # Chathurya Club Logo
    ├── hero-workshop.svg / .jpg         # Hero Coding Illustration
    ├── fullstack.svg / .jpg             # Full Stack Banner Illustration
    ├── data-analytics.svg / .jpg        # Data Analytics Banner Illustration
    ├── cs50p.svg                        # CS50P Previous Event Illustration
    └── webstart.svg                     # WebStart 2.0 Previous Event Illustration
```

---

## 🚀 How to Run the Development Server

Opening `http://localhost:8000/` directly loads the **Homepage** (`index.html`). Directory listings and hidden system folders (`.git`, config files) are protected and disabled.

### Method 1: Using Custom Secure Development Server (`server.py`)

1. Open PowerShell or Command Prompt in the project root directory:
   ```powershell
   cd c:\Users\ajbha\Desktop\csdcf
   ```
2. Run the secure development server:
   ```powershell
   python server.py
   ```
3. Open your browser and navigate to:
   - **[http://localhost:8000](http://localhost:8000)**

### Method 2: Using Python Standard HTTP Server
```powershell
python -m http.server 8000
```
*(Since `index.html` is located directly at the project root, `http://localhost:8000/` immediately displays the website homepage).*

### Method 3: Direct Browser View
Open [`index.html`](file:///c:/Users/ajbha/Desktop/csdcf/index.html) in any web browser.

---

## 🌟 Key Features & Website Flow

### Page Flow
1. **Home Page** (`index.html`) → Click **"View Course"** → Redirects to **Courses Page** (`courses.html`)
2. **Courses Page** (`courses.html`) → Click **"View Detailed Course"** → Redirects to **Full Stack Development** (`fullstack.html`) or **Data Analytics** (`data-analytics.html`)
3. **Course Details Page** → Click **"Register Now"** → Redirects to **Registration Page** (`registration.html`)

### 1. Home Page (`index.html`)
- **Header & Navbar**: Brand logo, Navigation links (**Home | About Us | Previous Events | Courses | Register**), Theme Toggle.
- **Hero Section**: Workshop banner, primary `"View Course"` button, secondary `"Register Now"` button.
- **About Us Section**: Details about college club activities (Technical workshops, events, learning activities, hands-on development programs).
- **Previous Events Section**: CS50P (Harvard Python course by David J. Malan) & WebStart 2.0 crash course cards.
- **Courses Section**: Overview of Full Stack Development & Data Analytics with centered `"View Course"` button.

### 2. Courses Page (`courses.html`)
- Large dedicated cards for **Full Stack Development** and **Data Analytics**.
- Detailed topic lists and `"View Detailed Course"` buttons.

### 3. Full Stack Development Page (`fullstack.html`)
- **Modules 01–06**: `01 HTML`, `02 CSS`, `03 SQL / SQLite`, `04 PYTHON`, `05 FLASK`, `06 GIT & VS CODE`.
- **5 Hands-on Projects**: Canteen menu, order database, Python calculator, Flask web app, full-stack integration.
- **Practical Capstone**: **College Canteen Pre-Order System** (`Frontend` → `Database` → `Backend Logic` → `Web App` → `Test, Run & Deliver`).
- `"Register Now"` button linking to `registration.html`.

### 4. Data Analytics Page (`data-analytics.html`)
- **Modules 01–06**: `01 EXCEL DATA CLEANING`, `02 ADVANCED EXCEL`, `03 DATA MODELING`, `04 AUTOMATION`, `05 TABLEAU ANALYTICS`, `06 DASHBOARDS & STORYTELLING`.
- **5 Hands-on Projects**: 50,000-row dataset cleaning, relational model, VBA automation, Tableau charts, executive dashboard.
- **Practical Capstone**: **Sales and Operations Analytics Dashboard** (Excel, Power Query, Power Pivot, VBA, Tableau).
- `"Register Now"` button linking to `registration.html`.

### 5. Registration Page (`registration.html`)
- 9 mandatory fields: Full Name, College ID Number (`24CA000`), Email Address, Phone Number, Stream, Course, Year of Study, Section, Laptop availability.
- Live real-time validation for all fields.
- Dynamic **"Registration Successful!"** confirmation card rendering without full page reload.
