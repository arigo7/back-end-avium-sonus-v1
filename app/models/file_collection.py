from app import db
from flask import current_app # WHAT IS THIS USED FOR?

class Collection(db.Model):
    collection_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    user = db.Column(db.String) ## user_id?
    # cards = db.relationship('Card', lazy = True)
    files = db.relationship('File', backref='collection', lazy = True)

    # def to_json(self):
    #     return {
    #         "collection_id": self.collection_id,
    #         "title": self.title,
    #         "user": self.user,
    #         "files": ?
    #     }