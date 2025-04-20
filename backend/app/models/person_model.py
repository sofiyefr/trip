from app.extensions import db  

class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.String)
    photo_url = db.Column(db.String(100))

    def __repr__(self):
        return f"<Person '{self.name}'>"