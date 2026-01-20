# Enterprise Usage Monitoring & Admin Platform

![dashboard_preview.png](dashboard_preview.png)

> A Multi-Tenant SaaS Monitoring System built with Flask, MySQL, and Tailwind CSS.
> Features **Real-Time Usage Tracking**, **Rate Limiting (Blocking)**, and an **Interactive Admin Dashboard**.

---

## 🚀 Key Features
* **Real-Time Monitoring:** Uses JavaScript polling to update usage stats every 2 seconds without page refreshes.
* **Active Rate Limiting:** Automatically blocks tenants with a `429 Too Many Requests` error if they exceed their plan limit.
* **Tenant Authentication:** Secure access using unique `X-API-KEY` headers for each enterprise client.
* **Performance Tracking:** Measures and logs API latency (response time) for every request.
* **Data Persistence:** Uses MySQL to ensure relational data integrity between Tenants, Users, and Logs.

---

## 🛠️ System Design & Architecture

### 1. The Interceptor (Decorator Pattern)
Instead of hardcoding logic into every endpoint, I implemented a Python Decorator (`@monitor_api`) that acts as a middleware.
* **Intercepts** every incoming request.
* **Validates** the `X-API-KEY` against the database.
* **Checks** if the tenant has crossed their usage limit.
* **Logs** the request timestamp and latency asynchronously.

### 2. Database Schema (MySQL)
The system uses a normalized relational schema:
* **Tenants:** Stores Company Name and API Keys.
* **Users:** Linked to Tenants (One-to-Many).
* **UsageLogs:** Stores `timestamp`, `endpoint`, `response_time`, and `status_code` for audit trails.

### 3. Frontend Architecture
* **UI:** Built with **Tailwind CSS** for a responsive, modern interface.
* **Live Updates:** A lightweight JavaScript engine fetches JSON data from `/api/dashboard-data` every 2 seconds to update the DOM dynamically.

---

## 🔌 API Documentation

### 1. Get Users (Protected Route)
Fetches the list of active users for the tenant.
* **Endpoint:** `GET /api/v1/users`
* **Headers:** `X-API-KEY: <Your_Tenant_Key>`
* **Response (Success):**
    ```json
    {
      "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    }
    ```
* **Response (Blocked):**
    ```json
    {
      "error": "Plan Limit Exceeded",
      "message": "Usage: 50/50. Access Blocked."
    }
    ```

### 2. Setup / Reset Data
A utility script to seed the database with tenants ("Acme Corp" and "Wayne Ent") and reset counters to zero.
* **Endpoint:** `GET /setup`

---

## 💻 How to Run Locally

### Prerequisites
* Python 3.x
* MySQL Server (Running)

### Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/Harzh-k/enterprise-usage-monitor.git](https://github.com/Harzh-k/enterprise-usage-monitor.git)
    cd enterprise-usage-monitor
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Database**
    Open `config.py` and update your MySQL credentials:
    ```python
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/enterprise_db'
    ```

4.  **Initialize Database**
    Open MySQL Workbench or Terminal and run:
    ```sql
    CREATE DATABASE enterprise_db;
    ```

5.  **Start the Server**
    ```bash
    python run.py
    ```

6.  **Access the Platform**
    * **Dashboard:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    * **Initialize Data:** Click the **"Reset Data"** button on the dashboard.

---

## 📂 Project Structure
```text
enterprise-monitor/
├── app/
│   ├── templates/
│   │   └── dashboard.html    # Admin UI with Live Polling JS
│   ├── __init__.py           # Flask App Factory
│   ├── models.py             # Database Models (SQLAlchemy)
│   └── routes.py             # Business Logic & Rate Limiting
├── config.py                 # Database Config
├── run.py                    # Entry Point
├── requirements.txt          # Python Dependencies
└── README.md                 # Documentation