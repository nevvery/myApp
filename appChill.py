from app import create_app
from config import Config

app = create_app(config=Config)

from app.models import Parent, Role, Payment, Child
