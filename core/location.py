# -*- encoding: utf-8 -*-

from enum import Enum


class Location(Enum):
    """
    Enum class with server locations.

    Attributes
    ----------
    Location.IRELAND : str
        Server located in Ireland.

    """

    IRELAND: str = "eu-west-1"
