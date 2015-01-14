from app import db
from app.models import Message, Channel

Message.query.delete()
Channel.query.delete()
db.session.commit()
