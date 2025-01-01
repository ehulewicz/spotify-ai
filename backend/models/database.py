from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_app(app):
  db.init_app(app)
  with app.app_context():
    db.create_all()

class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  user_name = db.Column(db.String(100), unique=True, nullable=False)
  alias = db.Column(db.String(100), unique=True, nullable=True)
  is_tracked = db.Column(db.Boolean, default=False)

  def __repr__(self):
    return f"<User: {self.user_name}>"
  
class Song(db.Model):
  __tablename__ = "songs"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  artist = db.Column(db.String(255), nullable=False)
  album = db.Column(db.String(255), nullable=False)
  genre = db.Column(db.String(100))
  duration = db.Column(db.Integer, nullable=False) # milliseconds

  def __repr__(self):
    return f"<Song: {self.title}>"
  
class ListeningHistory(db.Model):
  __tablename__ = "listening_history"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  song_id = db.Column(db.Integer, db.ForeignKey("songs.id"), nullable=False)
  played_at = db.Column(db.DateTime, default=datetime.utcnow())
  play_duration = db.Column(db.Integer) # milliseconds
  context = db.Column(db.String(255)) # playlist or album listend on

  def __repre__(self):
    return f"<Listening History User_ID: {self.user_id}, Song_ID: {self.song_id}"