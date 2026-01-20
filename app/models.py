from . import db
from datetime import datetime

class Tenant(db.Model):
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(50), unique=True, nullable=False)
    # Relationship: One Tenant has many Users
    users = db.relationship('User', backref='tenant', lazy=True)
    # Relationship: One Tenant has many Usage Logs
    logs = db.relationship('UsageLog', backref='tenant', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)

class UsageLog(db.Model):
    __tablename__ = 'usage_logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    endpoint = db.Column(db.String(100), nullable=False)
    response_time_ms = db.Column(db.Integer, default=0)
    status_code = db.Column(db.Integer, default=200)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)