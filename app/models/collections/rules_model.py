"""Model for rules collection"""

from mongoengine import DictField, Document, ListField, StringField


class Rule(Document):
    """
    Model for rules collection
    Attributes:
        name: StringField(required=True, unique=True)
        conditions: ListField(DictField())
    """

    name = StringField(required=True, unique=True)
    conditions = ListField(DictField())

    meta = {"collection": "rules"}
