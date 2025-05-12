from flask_security import SQLAlchemyUserDatastore
from app import db
from app.models import Parent, Role

user_datastore = SQLAlchemyUserDatastore(db, Parent, Role)

