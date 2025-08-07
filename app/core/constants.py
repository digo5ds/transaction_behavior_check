"""Constants used in the application."""

import enum


class ChannelEnum(enum.Enum):
    """
    Enumeration representing the various channels through which a transaction can be performed.

    Attributes:
        ATM (str): Transactions performed via Automated Teller Machines.
        TELLER (str): Transactions performed at a bank teller.
        INTERNET_BANKING (str): Transactions performed through internet banking platforms.
        MOBILE_BANKING (str): Transactions performed through mobile banking applications.
    """

    ATM = 0
    TELLER = 1
    INTERNET_BANKING = 2
    MOBILE_BANKING = 3


class TransactionType(enum.Enum):
    """
    Enumeration representing the available payment methods.

    Attributes:
        CREDIT: Represents payment made using a credit method.
        DEBIT: Represents payment made using a debit method.
    """

    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
