"""Constants used in the application."""

import enum


class ChannelEnum(enum.IntEnum):
    """
    Enumeration representing the various channels through which a transaction can be performed.

    Integer values assigned to each channel:
        ATM = 0 (Automated Teller Machine)
        TELLER = 1 (Bank teller counter)
        INTERNET_BANKING = 2 (Internet banking platform)
        MOBILE_BANKING = 3 (Mobile banking application)
    """

    ATM = 0
    TELLER = 1

    INTERNET_BANKING = 2
    IBK = 2

    MOBILE_BANKING = 3
    MBK = 3


INITIAL_RULES = {
    "high_value_dawn": [
        {
            "filter": {
                "and": [
                    {
                        "field": "created_at",
                        "transform": "!time",
                        "op": "gte",
                        "value": {"hour": 0, "minute": 0, "second": 0},
                    },
                    {
                        "field": "created_at",
                        "transform": "!time",
                        "op": "lte",
                        "value": {"hour": 5, "minute": 0, "second": 0},
                    },
                    {
                        "field": "channel",
                        "op": "eq",
                        "value": "ATM",
                    },
                    {
                        "field": "amount",
                        "op": "gte",
                        "value": 10000,
                    },
                ]
            },
            "suspect": True,
        }
    ],
    "trx_teller_bef_10__or_aft_16": [
        {
            "filter": {
                "or": [
                    {
                        "and": [
                            {
                                "field": "created_at",
                                "transform": "!time",
                                "op": "lt",
                                "value": {"hour": 10, "minute": 0, "second": 0},
                            },
                            {
                                "field": "channel",
                                "op": "eq",
                                "value": "TELLER",
                            },
                        ]
                    },
                    {
                        "and": [
                            {
                                "field": "created_at",
                                "transform": "!time",
                                "op": "gt",
                                "value": {"hour": 16, "minute": 0, "second": 0},
                            },
                            {
                                "field": "channel",
                                "op": "eq",
                                "value": "TELLER",
                            },
                        ]
                    },
                ]
            },
            "suspect": True,
        },
    ],
    "same_trx_in_last_in_period": [
        {
            "filter": {
                "and": [
                    {
                        "field": "",
                        "transform": "!count_same_trx_by_channel_user_in_last_in_period",
                        "params": {
                            "channel": ["IBK", "MBK", "TELLER", "ATM"],
                            "interval_minutes": 10,
                            "sensibility_variation_percentage": 0.2,
                        },
                        "op": "gte",
                        "value": 3,
                    }
                ]
            },
        },
    ],
    "high_value_account_destination_not_frequent": [
        {
            "filter": {
                "and": [
                    {
                        "field": "",
                        "transform": "!destination_account_frequency",
                        "op": "lte",
                        "value": 2,
                    },
                    {
                        "field": "amount",
                        "op": "gte",
                        "value": 10000,
                    },
                ]
            },
        },
    ],
    "high_value_older_age_diginal": [
        {
            "filter": {
                "and": [
                    {
                        "field": "origin_account_rel.customer_rel.age",
                        "op": "gte",
                        "value": 60,
                    },
                    {
                        "field": "amount",
                        "op": "gte",
                        "value": 500,
                    },
                    {
                        "field": "channel",
                        "op": "in",
                        "value": ["IBK", "MBK"],
                    },
                    {
                        "field": "",
                        "transform": "!count_same_trx_by_channel_user_in_last_in_period",
                        "params": {
                            "channel": ["IBK", "MBK"],
                            "interval_minutes": 43200,
                        },
                        "op": "lte",
                        "value": 5,
                    },
                ]
            },
        },
    ],
    "multiples_txr_by_IBK_or_MBK": [
        {
            "filter": {
                "$and": [
                    {
                        "transform": "!count_same_trx_by_channel_user_in_last_in_period",
                        "params": {"channel": ["IBK", "MBK"]},
                        "op": "lte",
                        "value": 5,
                    },
                    {
                        "field": "created_at",
                        "transform": "!time",
                        "op": "$gt",
                        "value": {"hour": 16, "minute": 0, "second": 0},
                    },
                ],
            },
            "suspect": True,
        }
    ],
}
