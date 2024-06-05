from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    user_id: Mapped[int] = mapped_column('user_id', primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(nullable=True)
    pasword_hash: Mapped[str] = mapped_column()
    
    def set_password(self, password):
        self.pasword_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.pasword_hash, password)
    
    def get_id(self):
        return self.user_id
    