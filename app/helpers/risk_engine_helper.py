"""Helper class for evaluating behavioral transaction risk."""

import statistics
from datetime import datetime, time, timedelta
from typing import Any, Callable, Dict, List, Union

from app.core.constants import ChannelEnum
from app.core.logger import logger
from app.helpers.mongo_helper import MongoHelper
from app.helpers.transaction_helper import TransactionHelper
from app.models.collections.rules_model import Rule
from app.models.collections.user_cache_model import KnowlegedDestinations
from app.models.tables.transaction_model import Transaction
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
        self.mongo_helper = MongoHelper()
        self.transaction_helper = TransactionHelper()

    def count_transactions(
        self, transactions: List[dict], field: str, params: dict
    ) -> int:
        """
        Count transactions that match given parameters.
        """
        return 0  # Not yet implemented

    def same_transaction(
        self,
        interval_minutes,
        channels: List[str],
        origin_account_id,
        destination_account_id,
        params,
    ) -> int:

        variation = params.get("sensibility_variation_percentage")
        channels = [ChannelEnum[channel].value for channel in params["channel"]]
        result = self.transaction_helper.count_transaction_by_user_channel(
            channel=channels,
            lookback=datetime.now() - timedelta(minutes=interval_minutes),
            origin_account_id=origin_account_id,
            destination_account_id=destination_account_id,
        )
        transaction_values = [item[4] for item in result if item[0] in channels]
        if variation:
            median = statistics.median(transaction_values)
            lower_bound = median * (1 - variation)
            upper_bound = median * (1 + variation)
            return sum(v for v in transaction_values if lower_bound <= v <= upper_bound)
        return sum(transaction_values)

    def __count_same_trx_by_channel_user_in_last_in_period(
        self,
        interval_minutes: int,
        origin_account_id: int,
        destination_account_id: int,
        params: dict,
    ) -> int:
        """
        Counts transactions that match given parameters and sums their amounts.

        Args:
            interval_minutes (int): The number of minutes to look back.
            origin_account_id (int): The originating account of the transactions.
            destination_account_id (int): The destination account of the transactions.
            params (Dict[str, Any]): Additional parameters for the transform.

        Returns:
            int: The sum of the amounts of the transactions.
        """
        variation = params.get("sensibility_variation_percentage")
        channels = [ChannelEnum[channel].value for channel in params["channel"]]
        result = self.transaction_helper.count_transaction_by_user_channel(
            channel=channels,
            lookback=datetime.now() - timedelta(minutes=interval_minutes),
            origin_account_id=origin_account_id,
            destination_account_id=destination_account_id,
        )
        transaction_values = [
            [float(item[1]), item[4]] for item in result if item[0] in channels
        ] or []
        transaction_values = [
            value for value, count in transaction_values for _ in range(count)
        ]
        if not transaction_values:
            return 0
        if variation:
            median = statistics.median(transaction_values)
            lower_bound = median * (1 - variation)
            upper_bound = median * (1 + variation)
            return len(
                [v for v in transaction_values if lower_bound <= v <= upper_bound]
            )

        return len(transaction_values)

    def __destination_account_frequency(
        self, origin_account_id: int, destination_account_id: int
    ) -> int:
        """
        Counts how many times a given destination account has been used by a given
        origin account.

        Args:
            origin_account_id (int): The originating account.
            destination_account_id (int): The destination account.

        Returns:
            int: The number of occurrences of the destination account.
        """
        occurrences = [
            item.destination_user
            for item in self.mongo_helper.find_documents(
                KnowlegedDestinations, {"origin_user": origin_account_id}
            )
        ].count(destination_account_id)
        return occurrences

    def process_transform(
        self, transform: str, transaction_field, transform_field, params
    ) -> Any:
        """
        Convert a value based on the specified transform.

        Supported transforms:

        * -- ``!time``: parse the value as a time
        * --``!last_minutes``: calculate the datetime that
        * -- ``!count_same_trx_by_channel_user_in_last_in_period``:
            count transactions that match given parameters
        * -- ``!destination_account_frequency``:
            count how many times a given destination account has been used by a given origin account

        Args:
            transform (str): The transform to apply.
            transaction_field (Any): The value to transform.
            transform_field (Any): The value to transform.
            params (Dict[str, Any]): Additional parameters for the transform.

        Returns:
            Any: The transformed value. If the transform is not supported,
            is the given value (in minutes) ago from now
        """
        if transform == "!time":
            return datetime.now().replace(**transform_field)

        if (
            transform == "!count_same_trx_by_channel_user_in_last_in_period"
            and params.get("channel")
            and params.get("interval_minutes")
        ):
            result = self.__count_same_trx_by_channel_user_in_last_in_period(
                interval_minutes=params["interval_minutes"],
                origin_account_id=transaction_field.origin_account_rel.id,
                destination_account_id=transaction_field.destination_account_rel.id,
                params=params,
            )
            return result

        if transform == "!destination_account_frequency":
            return self.__destination_account_frequency(
                origin_account_id=transaction_field.origin_account_rel.id,
                destination_account_id=transaction_field.destination_account_rel.id,
            )

        return transform_field

    def compare(
        self,
        op: str,
        transaction_field_value: Any,
        condition_value: Any,
    ) -> bool:
        """
        Safely compare two values based on the specified operator.
        """

        # self.compare(condition.op, field_value, condition.value)
        if op == "eq":
            return transaction_field_value == condition_value
        if op == "lt":
            return transaction_field_value < condition_value
        if op == "gt":
            return transaction_field_value > condition_value
        if op == "gte":
            return transaction_field_value >= condition_value
        if op == "lte":
            return transaction_field_value <= condition_value
        if op == "in":
            return transaction_field_value in condition_value
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
            if "and" in condition:
                return all(
                    self.evaluate_condition(sub, transaction)
                    for sub in condition["and"]
                )
            if "or" in condition:
                return any(
                    self.evaluate_condition(sub, transaction) for sub in condition["or"]
                )
            condition = SimpleCondition(**condition)

        if hasattr(transaction, condition.field):
            field_value = getattr(transaction, condition.field)

            if isinstance(field_value, ChannelEnum):
                if isinstance(condition.value, list):
                    condition.value = [
                        ChannelEnum[item].value for item in condition.value
                    ]
                else:
                    condition.value = ChannelEnum[condition.value].value
                field_value = field_value.value

            if isinstance(field_value, datetime) and isinstance(condition.value, time):
                field_value = field_value.time()

        if condition.transform:

            if condition.transform in ("!time"):
                # cast: convert the field_value to the same type as condition.value
                condition_value = self.process_transform(
                    condition.transform, transaction, condition.value, condition.params
                )
                transaction_value = field_value
            else:
                # dynamic_funcs: execute the function and return the result like transaction_value
                transaction_value = self.process_transform(
                    condition.transform, transaction, condition.value, condition.params
                )
                condition_value = condition.value
            if not condition.op:
                return False
            return self.compare(condition.op, transaction_value, condition_value)

        if "." in condition.field:
            parts = condition.field.split(".")
            field_value = transaction
            for part in parts:
                field_value = getattr(field_value, part)
            return self.compare(condition.op, field_value, condition.value)
        if field_value is not None:
            return self.compare(condition.op, field_value, condition.value)
        return False

    def calculate_risk(self, transaction: Transaction) -> bool:
        """
        Main entry point for evaluating risk against a rule set.
        """
        mongo_helper = MongoHelper()
        rules = [item["conditions"] for item in mongo_helper.find_documents(Rule)]
        for rule_blocks in rules:
            for block in rule_blocks:
                filter_dict = block.get("filter")
                if filter_dict and self.evaluate_condition(filter_dict, transaction):
                    logger.info(
                        "Transaction matched rule, this trahsaction is suspect: rule: %s",
                        filter_dict,
                    )

                    return True
        return False
