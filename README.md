**## Overview**

**This project demonstrates how modern financial applications use adaptive security instead of simple username-password authentication.**



**The system evaluates multiple risk signals during login and dynamically decides whether to:**

**- Allow full access**

**- Allow partial access with restrictions**

**- Require step-up verification**

**- Block access**



**## Key Features**

**- Behavioral biometrics using typing pattern enrollment**

**- Device fingerprinting with similarity-based matching**

**- Geo-velocity and impossible travel detection**

**- OTP misuse detection and rate limiting**

**- Partial access control (portfolio locked under risk)**

**- Interactive dashboard with market data and charts**



**## Tech Stack**

**- Python 3.12**

**- FastAPI (Backend API)**

**- Machine Learning (risk scoring \& fusion logic)**

**- HTML, CSS, JavaScript (Frontend)**

**- Chart.js (Data visualization)**



**## Project Structure**

**Project2/**

**├── backend/**

**│ ├── app.py**

**│ ├── routes/**

**│ ├── utils/**

**│ ├── models/**

**│ └── requirements.txt**

**│**

**├── frontend/**

**│ ├── landing.html**

**│ ├── register.html**

**│ ├── login.html**

**│ ├── dashboard.html**

**│ ├── verify.html**

**│ ├── style.css**

**│ └── js/**

**│**

**├── .gitignore**

**└── README.md**





**## How to Run the Project**



**### 1. Start the Backend**

**```bash**

**cd backend**

**uvicorn app:app --reload**

**Backend will run at:**



**http://127.0.0.1:8000**



**2. Start the Frontend**

**Open a new terminal:**



**cd frontend**

**python -m http.server 5500**



**Open in browser:**



**http://127.0.0.1:5500/landing.html**



**Notes**

**This project is a prototype built for learning and demonstration purposes**



**In production, persistent databases and secure OTP delivery would be required**