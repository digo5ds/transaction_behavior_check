import unittest
from datetime import datetime, timedelta

from app.core.config import rules
from app.helpers.risk_engine_helper import RiskEvaluator
from app.models.account_model import Account
from app.models.customer_model import Customer
from app.models.transaction_model import Transaction


def build_transaction(
    amount, channel, created_at, transaction_id="tx1", destination="dest123"
):
    customer = Customer(id=1, name="John Doe", age=30)
    origin_acc = Account(id=1, agency=123, account=456, rel_customer=customer)
    destination_acc = Account(id=2, rel_customer=customer)

    trx = Transaction(
        amount=amount,
        channel=channel,
        origin_account_rel=origin_acc,
        destination_account_rel=destination_acc,
        created_at=created_at,
    )
    trx.transaction_id = transaction_id
    trx.destination = destination
    trx.value = amount
    return trx


class RiskEngineTest(unittest.TestCase):

    def setUp(self):
        self.risk_evaluator = RiskEvaluator()

    def test_teller_before_10am(self):
        trx = build_transaction(
            amount=500,
            channel="TELLER",
            created_at=datetime.now().replace(hour=9, minute=30),
        )
        self.assertTrue(self.risk_evaluator.calculate_risk(trx, rules))

    def test_teller_after_4pm(self):
        trx = build_transaction(
            amount=500,
            channel="TELLER",
            created_at=datetime.now().replace(hour=17, minute=0),
        )
        self.assertTrue(self.risk_evaluator.calculate_risk(trx, rules))

    def test_teller_during_business_hours(self):
        trx = build_transaction(
            amount=500,
            channel="TELLER",
            created_at=datetime.now().replace(hour=11, minute=0),
        )
        self.assertFalse(self.risk_evaluator.calculate_risk(trx, rules))

    def test_high_value_atm_during_dawn(self):
        trx = build_transaction(
            amount=1000,
            channel="ATM",
            created_at=datetime.now().replace(hour=2, minute=0),
        )
        self.assertTrue(self.risk_evaluator.calculate_risk(trx, rules))

    def test_high_value_atm_during_day(self):
        trx = build_transaction(
            amount=1000,
            channel="ATM",
            created_at=datetime.now().replace(hour=14, minute=0),
        )
        self.assertFalse(self.risk_evaluator.calculate_risk(trx, rules))

    def test_multiple_ibk_transactions(self):
        now = datetime.now()
        trx = build_transaction(
            amount=200, channel="IBK", created_at=now, transaction_id="tx1"
        )
        history = [
            {"channel": "IBK", "transaction_id": "tx2"},
            {"channel": "IBK", "transaction_id": "tx3"},
        ]
        self.assertTrue(self.risk_evaluator.calculate_risk(trx, rules))

    def test_not_enough_ibk_transactions(self):
        now = datetime.now()
        trx = build_transaction(
            amount=200, channel="IBK", created_at=now, transaction_id="tx1"
        )
        history = [{"channel": "IBK", "transaction_id": "tx2"}]
        self.assertFalse(self.risk_evaluator.calculate_risk(trx, rules))

    # TODO:  wait implement dynamic functions
    # def test_repeated_transaction_recently(self):
    #     now = datetime.now()
    #     trx = build_transaction(
    #         amount=150,
    #         channel="MBK",
    #         created_at=now,
    #         transaction_id="tx5",
    #         destination="dest123",
    #     )
    #     history = [
    #         {
    #             "value": 150,
    #             "destination": "dest123",
    #             "created_at": now - timedelta(minutes=5),
    #             "transaction_id": "tx6",
    #         },
    #         {
    #             "value": 150,
    #             "destination": "dest123",
    #             "created_at": now - timedelta(minutes=2),
    #             "transaction_id": "tx7",
    #         },
    #     ]
    #     self.assertTrue(self.risk_evaluator.calculate_risk(trx, rules))

    # def test_no_repeated_transaction(self):
    #     now = datetime.now()
    #     trx = build_transaction(
    #         amount=150,
    #         channel="MBK",
    #         created_at=now,
    #         transaction_id="tx5",
    #         destination="dest123",
    #     )
    #     history = []
    #     self.assertFalse(self.risk_evaluator.calculate_risk(trx, rules))


if __name__ == "__main__":
    unittest.main()
