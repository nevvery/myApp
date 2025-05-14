from flask_security import SQLAlchemyUserDatastore
from app import db
from app.models import Parent, Role

user_datastore: SQLAlchemyUserDatastore = SQLAlchemyUserDatastore(db, Parent, Role)

