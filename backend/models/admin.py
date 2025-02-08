from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_default_admin():
        """Creates a default admin if none exists"""
        if not Admin.query.first():
            admin = Admin(username='admin')
            admin.set_password('admin123')  # Change this password in production!
            db.session.add(admin)
            db.session.commit()
