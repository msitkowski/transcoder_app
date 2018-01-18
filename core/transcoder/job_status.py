# -*- encoding: utf-8 -*-

from enum import Enum


class JobStatus(Enum):
    """
    Transcoder jobs status.

    Attributes
    ----------
    SUBMITTED : str
        Job submitted to processing.
    PROGRESSING : str
        Currently processing job.
    COMPLETE : str
        Completed job.
    CANCELED : str
        Cancelled job.
    ERROR : str
        Job where error occurred during processing.

    """

    SUBMITTED = "Submitted"
    PROGRESSING = "Progressing"
    COMPLETE = "Complete"
    CANCELED = "Canceled"
    ERROR = "Error"
