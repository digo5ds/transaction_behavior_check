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
    MOBILE_BANKING = 3
    MBK = 3
