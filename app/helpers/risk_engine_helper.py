"""Helper class for evaluating behavioral transaction risk."""

from datetime import datetime, time
from typing import Any, Callable, Dict, List, Union

from app.core.constants import ChannelEnum
from app.models.transaction_model import Transaction
from app.schemas.rules_schemas import FilterCondition, SimpleCondition

FilterCondition.model_rebuild()


class RiskEvaluator:
    """
    Evaluates financial transaction risk based on configurable rule sets.
    """

    def __init__(self):
        self.special_functions: Dict[str, Callable[..., Any]] = {
            "!count": self.count_transactions,
            "!same_transaction": self.same_transaction,
        }

    def count_transactions(
        self, transactions: List[dict], field: str, params: dict
    ) -> int:
        """
        Count transactions that match given parameters.
        """
        return 0  # Not yet implemented

    def same_transaction(self, transactions: List[dict], current: dict) -> int:
        """
        Count how many past transactions match the current one by value and destination.
        """
        return 0  # Not yet implemented

    def compare(self, op: str, a: Any, b: Any) -> bool:
        """
        Safely compare two values based on the specified operator.
        """
        if op == "$eq":
            return a == b
        if op == "$lt":
            return a < b
        if op == "$gt":
            return a > b
        if op == "$gte":
            return a >= b
        if op == "$lte":
            return a <= b
        return False

    def evaluate_condition(
        self,
        condition: Union[SimpleCondition, Dict[str, Any]],
        transaction: Any,
    ) -> bool:
        """
        Evaluate a single condition against a transaction and its history.
        """
        if isinstance(condition, dict):
            if "$and" in condition:
                return all(
                    self.evaluate_condition(sub, transaction)
                    for sub in condition["$and"]
                )
            if "$or" in condition:
                return any(
                    self.evaluate_condition(sub, transaction)
                    for sub in condition["$or"]
                )
            condition = SimpleCondition(**condition)

        if condition.transform:
            func = self.special_functions.get(condition.transform)
            if not func:
                return False
            if condition.transform == "!count":
                pass  # necessário histórico
                # result = func(history, condition.field, condition.params or {})
            else:
                pass  # necessário histórico
            # return self.compare(condition.op, result, condition.value)
            return None

        if hasattr(transaction, condition.field):
            field_value = getattr(transaction, condition.field)

            if isinstance(field_value, ChannelEnum):
                condition.value = ChannelEnum[condition.value].value
                field_value = field_value.real

            if isinstance(field_value, datetime) and isinstance(condition.value, time):
                field_value = field_value.time()
            return self.compare(condition.op, field_value, condition.value)

        return False

    def evaluate_conditions(
        self, filter_condition: Dict[str, Any], transaction: Any
    ) -> bool:
        """
        Evaluate all filter conditions against a transaction.
        """
        return self.evaluate_condition(filter_condition, transaction)

    def calculate_risk(
        self,
        transaction: Transaction,
        rules: Dict[str, List[Dict]],
    ) -> bool:
        """
        Main entry point for evaluating risk against a rule set.
        """
        for rule_blocks in rules.values():
            for block in rule_blocks:
                filter_dict = block.get("filter")
                if filter_dict and self.evaluate_conditions(filter_dict, transaction):
                    return True
        return False
