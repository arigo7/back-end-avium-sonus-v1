from app import db      #won't need this if I don't use database
from flask import current_app


# Not a good model anymore - each file may have 1 or many birds
class OutputFile(db.Model): #Audio File
    text_file_id = db.Column(db.Integer, primary_key=True)
    text_file_name = db.Column(db.String)
    text_file_size = db.Column(db.Integer, default=0)  # is size of a file an integer?
    # user_name = db.Column(db.String) ## or user id
    # board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)
    file_collection_id = db.Column(db.Integer, db.ForeignKey('collection.file_collection_id'), nullable=True)


    # def to_json(self):
    #     return {
    #         "card_id": self.card_id,
    #         "message": self.message,
    #         "likes_count": self.likes_count,
    #         "board_id": self.board_id 
    #     }