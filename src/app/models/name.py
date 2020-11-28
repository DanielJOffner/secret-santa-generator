from src.app import db


class Name(db.Model):
    __tablename__ = 'name'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    disposition = db.Column(db.String(400))

    hat_id = db.Column(db.Integer, db.ForeignKey('hat.id'))
