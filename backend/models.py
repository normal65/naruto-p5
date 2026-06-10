from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Character(db.Model):
    """角色模型"""
    __tablename__ = 'characters'

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    name_en = db.Column(db.String(50))
    role = db.Column(db.String(100))
    image = db.Column(db.String(200))
    summary = db.Column(db.Text)
    tags = db.Column(db.JSON)  # PostgreSQL/MySQL 5.7+ 都支持JSON类型
    quotes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nameEn': self.name_en,
            'role': self.role,
            'image': self.image,
            'summary': self.summary,
            'tags': self.tags or [],
            'quotes': self.quotes
        }


class Event(db.Model):
    """剧情事件模型"""
    __tablename__ = 'events'

    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(50))
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联子事件
    children = db.relationship('EventChild', backref='event', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'period': self.period,
            'summary': self.summary,
            'children': [child.to_dict() for child in self.children]
        }


class EventChild(db.Model):
    """子事件模型"""
    __tablename__ = 'event_children'

    id = db.Column(db.String(20), primary_key=True)
    event_id = db.Column(db.String(20), db.ForeignKey('events.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'detail': self.detail
        }
