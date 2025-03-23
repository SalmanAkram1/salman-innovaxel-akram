from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)
    access_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<URL {self.short_code}>"
