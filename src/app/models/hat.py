from src.app import db
from datetime import datetime


class Hat(db.Model):
    __tablename__ = 'hat'

    id = db.Column(db.Integer, primary_key=True)
    hat_number = db.Column(db.String(100), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    # Virtual property
    names = db.relationship('Name', backref='hat')
