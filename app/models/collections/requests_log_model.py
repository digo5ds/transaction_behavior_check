"""Model for knowleged_destinations_account collection"""

from datetime import datetime, timedelta

from mongoengine import DateTimeField, DictField, Document, IntField, StringField


class RequestLog(Document):
    """
    Model for knowleged_destinations_account collection
    Attributes:
        origin_user: IntField(required=True, unique=True)
        destination_user: IntField(required=True, unique=True)
        created_at: DateTimeField
    """

    response_status_code = IntField(required=True)
    response_json = IntField(required=True)
    created_at = DateTimeField(default=datetime.now())
    params = DictField(required=True)
    method = StringField(required=True)
    # TTL to expire the document
    meta = {
        "indexes": [
            {"fields": ["created_at"], "expireAfterSeconds": 2592000}
        ],  # 30 days
        "collection": "request_log",
    }
