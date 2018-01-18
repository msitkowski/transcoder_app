# -*- encoding: utf-8 -*-

from enum import Enum


class Presets(Enum):
    """
    Video resolution presets used in transcored.

    Attributes
    ----------
    SD480p16x9 : str
        SD quality 480p 16:9.

    """

    HD1080p = "1351620000001-000001"
    HD720p = "1351620000001-000010"
    SD480p16x9 = "1351620000001-000020"
    SD480p4x3 = "1351620000001-000030"
    SD320p16x9 = "1351620000001-000040"
    SD320p4x3 = "1351620000001-000050"
