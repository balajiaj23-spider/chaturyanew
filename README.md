# Chathurya Student Developers Club — Workshop Website

A modern, functional, responsive single-page and multi-view website for **Chathurya Student Developers Club**.

Built with **HTML5, CSS3, and vanilla JavaScript**, the design features a SaaS-inspired minimal dark interface with neon lime accents (`#b6ff00`), sleek form inputs, theme toggling, real-time validation, and smooth section redirects.

---

## 🌟 Key Features

* **Club Name**: **Chathurya Student Developers Club** branding across all navbar components, headers, logos, badges, and footers.
* **Unified Single Page + Multi-View Architecture**:
  * All core sections (Hero, About Us, Previous Events, Courses Catalog, Full Stack Syllabus, Data Analytics Syllabus, Registration Form, and Contact Footer) are embedded seamlessly on [`index.html`](file:///c:/Users/admin/Desktop/chaturya%20website%20project/index.html) with smooth redirect scrolling.
  * Dedicated standalone HTML pages (`courses.html`, `fullstack.html`, `data-analytics.html`, `registration.html`) are also provided for direct bookmarking and routing.
* **Minimal & Premium SaaS Aesthetic**: Dark charcoal backgrounds (`#0d0e11`), thin subtle borders, soft shadows, rounded corners, and neon lime primary CTAs.
* **Light / Dark Mode Support**: Theme switcher storing user preference in `localStorage`.
* **Form Validation & State Management**: Real-time error handling for 9 fields (including 10-digit mobile and email format checks), `localStorage` caching, and structured JS object payload ready for Django REST integration.

---

## 📁 Project Structure

```
chaturya-website-project/
│
├── index.html             # Main Unified Single-Page Portal (All Sections + Smooth Scroll Redirects)
├── courses.html           # Standalone Courses Catalog View
├── fullstack.html         # Standalone Full Stack Workshop Syllabus View
├── data-analytics.html    # Standalone Data Analytics Workshop Syllabus View
├── registration.html      # Standalone Registration Form View
│
├── css/
│   └── style.css          # Design System (Variables, Reset, SaaS Components, Responsive Rules)
│
├── js/
│   ├── main.js            # Navigation, Mobile Drawer, Theme Switcher, Smooth Scroll & Scroll Spy
│   └── registration.js    # 9-Field Real-Time Validation, LocalStorage, Confirmation View Switcher
│
├── images/
│   ├── logo.svg / logo.png                # Chathurya Student Developers Club Logo
│   ├── hero-workshop.svg / .jpg          # Hero terminal graphic
│   ├── fullstack.svg / .jpg              # Full Stack banner graphic
│   ├── data-analytics.svg / .jpg         # Data Analytics banner graphic
│   ├── event-1.svg / .jpg                # Web Bootcamp image
│   ├── event-2.svg / .jpg                # Python Beginners image
│   └── event-3.svg / .jpg                # Data Viz Workshop image
│
└── README.md              # Documentation & Django Migration Guide
```

---

## 🚀 How to Run

1. **Local Development Server**: Access [http://localhost:8000](http://localhost:8000) or [http://127.0.0.1:8000](http://127.0.0.1:8000).
2. **Direct Browser View**: Open [`index.html`](file:///c:/Users/admin/Desktop/chaturya%20website%20project/index.html) in any web browser.
