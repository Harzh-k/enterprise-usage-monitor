from flask import Blueprint, render_template, jsonify, request, redirect
from functools import wraps
# from datetime import datetime
import time
import uuid
# import random
from . import db
from .models import Tenant, User, UsageLog

main = Blueprint('main', __name__)

# ---GLOBAL SETTINGS ---
TENANT_LIMIT = 5


# MONITOR (With Limit Check)
def monitor_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()

        # Check API Key
        api_key = request.headers.get('X-API-KEY')
        tenant = Tenant.query.filter_by(api_key=api_key).first()

        if not tenant:
            return jsonify({"error": "Unauthorized: Invalid API Key"}), 401

        # RATE LIMIT CHECK
        current_count = UsageLog.query.filter_by(tenant_id=tenant.id).count()
        if current_count >= TENANT_LIMIT:
            return jsonify({
                "error": "Plan Limit Exceeded",
                "message": f"Usage: {current_count}/{TENANT_LIMIT}. Access Blocked."
            }), 429

        # Run Actual Function
        response = f(*args, **kwargs)

        # Log Success
        duration = int((time.time() - start_time) * 1000)
        status_code = response.status_code if hasattr(response, 'status_code') else 200

        log = UsageLog(
            tenant_id=tenant.id,
            endpoint=request.path,
            response_time_ms=duration,
            status_code=status_code
        )
        db.session.add(log)
        db.session.commit()
        return response

    return decorated_function

#THE DASHBORAD
@main.route('/')
def dashboard():
    tenants = Tenant.query.all()
    data = []
    for t in tenants:
        count = UsageLog.query.filter_by(tenant_id=t.id).count()
        data.append({
            'name': t.name,
            'api_key': t.api_key,
            'usage_count': count,
            'limit': TENANT_LIMIT  # Sending the REAL limit to HTML
        })
    return render_template('dashboard.html', stats=data)


#LIVE DATA API
@main.route('/api/dashboard-data')
def get_dashboard_data():
    tenants = Tenant.query.all()
    data = []
    for t in tenants:
        count = UsageLog.query.filter_by(tenant_id=t.id).count()

        # Determine Status
        status = "Normal"
        status_class = "bg-green-200 text-green-800"

        if count >= TENANT_LIMIT:
            status = "BLOCKED"  # ⛔ The new status
            status_class = "bg-red-600 text-white font-bold"  # Bright Red
        elif count > (TENANT_LIMIT * 0.8):
            status = "Warning"
            status_class = "bg-yellow-200 text-yellow-800"

        data.append({
            'api_key': t.api_key,
            'usage_count': count,
            'status': status,
            'status_class': status_class  # Sending color codes to JS
        })
    return jsonify(data)


#REAL API
@main.route('/api/v1/users', methods=['GET'])
@monitor_api
def get_users():
    return jsonify({"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]})


#SETUP DATA (Resets everything)
@main.route('/setup')
def setup_data():
    try:
        #Clear all old data
        db.session.query(UsageLog).delete()
        db.session.query(User).delete()
        db.session.query(Tenant).delete()
        db.session.commit()

        #Create Tenants
        t1 = Tenant(name="Acme Corp", api_key=str(uuid.uuid4()))
        t2 = Tenant(name="Wayne Ent", api_key=str(uuid.uuid4()))
        db.session.add_all([t1, t2])
        db.session.commit()

        #Create Users
        u1 = User(username="alice@acme.com", tenant_id=t1.id)
        db.session.add(u1)
        # for _ in range(50):
        #     db.session.add(UsageLog(tenant_id=t1.id, endpoint='/api/v1/users', response_time_ms=100))

        # for _ in range(12):
        #     db.session.add(UsageLog(tenant_id=t2.id, endpoint='/api/v1/users', response_time_ms=50))

        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error: {e}"