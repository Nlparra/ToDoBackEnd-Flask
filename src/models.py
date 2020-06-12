from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    label = db.Column(db.String(80), unique=False, nullable=False)
    done = db.Column(db.Boolean) 
    
    def __repr__(self):
        return '<ToDo %r>' % self.Label

    def serialize(self):
        return {
            "label": self.label,
            "done": false
        }