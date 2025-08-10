"""Model for knowleged_destinations_account collection"""

from datetime import datetime, timedelta

from mongoengine import DateTimeField, Document, IntField


class KnowlegedDestinations(Document):
    """
    Model for knowleged_destinations_account collection
    Attributes:
        origin_user: IntField(required=True, unique=True)
        destination_user: IntField(required=True, unique=True)
        created_at: DateTimeField
    """

    origin_user = IntField(required=True)
    destination_user = IntField(required=True)
    created_at = DateTimeField(default=datetime.now())

    # TTL to expire the document
    meta = {
        "indexes": [
            {"fields": ["created_at"], "expireAfterSeconds": 2592000}  # 30 days,
        ],
        "collection": "knowleged_destinations_account",
    }
