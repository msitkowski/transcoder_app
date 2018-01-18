# -*- encoding: utf-8 -*-

from enum import Enum


class ACL(Enum):
    """
    Enum with Access control list permissions.

    Attributes
    ----------
    ACL.PRIVATE : str
        Private access.
    ACL.PUBLIC_READ : str
        Read access for public users.
    ACL.PUBLIC_READ_WRITE : str
        Read and write access for public users.
    ACL.AUTHENTICATED_READ : str
        Read access for authenticated users.

    """

    PRIVATE: str = "private"
    PUBLIC_READ: str = "public-read"
    PUBLIC_READ_WRITE: str = "public-read-write"
    AUTHENTICATED_READ: str = "authenticated-read"
