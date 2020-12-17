import os
import config
import json
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_uri = os.getenv('DB_URI')
db_path = 'postgresql://{}:{}@{}/{}'.format(db_user, db_password, db_uri, db_name)

db = SQLAlchemy()
migrate = Migrate()

'''
setup_db(app)
  binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=db_path):
  app.config['SQLALCHEMY_DATABASE_URI'] = database_path
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.app = app
  db.init_app(app)
  migrate.init_app(app, db)

  @app.before_first_request
  def initialize_database():
    db.create_all()

'''
Trail

'''
class Trail(db.Model):  
  __tablename__ = 'trails'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=True)
  distance = Column(Float, nullable=False)
  elevation = Column(Float, nullable=False)
  difficulty = Column(String, nullable=False)
  coordination = Column(String, nullable=False)
  parking = Column(Boolean, default=False, server_default=db.false(), nullable=False)
  reviews = db.relationship('Review', backref="trails", cascade="all,delete", lazy=True)
  
  def __repr__(self):
    return f'<T.ID: {self.id}>'

  def __init__(self, name, distance, elevation, difficulty, coordination, parking):
    self.name = name
    self.distance = distance
    self.elevation = elevation
    self.difficulty = difficulty
    self.coordination = coordination
    self.parking = parking

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'distance': self.distance,
      'elevation': self.elevation,
      'difficulty': self.difficulty,
      'coordination': json.loads(self.coordination),
      'parking': self.parking
    }

'''
Region

'''
class Region(db.Model):  
  __tablename__ = 'regions'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=True)
  reg_type = Column(String, nullable=False)

  def __repr__(self):
    return f'<R.ID: {self.id}>'

  def __init__(self, name, reg_type):
    self.name = name
    self.reg_type = reg_type

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'type': self.reg_type
    }

'''
Review

'''
class Review(db.Model):  
  __tablename__ = 'reviews'

  id = Column(Integer, primary_key=True)
  rating = Column(Integer, nullable=False)
  comment = Column(String, nullable=False)
  user = Column(String, default='anonymous', server_default='anonymous', nullable=False)
  trail_id = Column(Integer, ForeignKey('trails.id'), nullable=False)

  def __repr__(self):
    return f'<RV.ID: {self.id} for T.ID: {self.trail_id}>'

  def __init__(self, trail_id, rating, comment, user):
    self.trail_id = trail_id
    self.rating = rating
    self.comment = comment
    self.user = user

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'trail_id': self.trail_id,
      'rating': self.rating,
      'comment': self.comment,
      'user': self.user
    }