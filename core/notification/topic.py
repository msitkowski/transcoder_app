# -*- encoding: utf-8 -*-

"""
Module enable operations on AWS SNS Topic.

"""

import boto3 as _boto3

from .queue import SQSQueue as _SQSQueue


__version__ = ""
__author__ = "Mateusz Sitkowski"


class SNSTopic:
    """
    AWS Simple Notification Service topic.

    """

    def __init__(self, name: str) -> None:
        """
        Initialize SNSTopic object.

        Parameters
        ----------
        name : str
            Topic name.

        """
        self.name = name
        self.arn = None
        self.__client = _boto3.client('sns')

    def get_existing_topic(self, name: str) -> bool:
        """
        Check if pipeline exists.

        Returns
        -------
        bool
            True if exists otherwise false.

        """
        for t in self.list_topics():
            if t and name in t.get("TopicArn", ""):
                self.arn = t.get("TopicArn")
                return True
        return False

    def list_topics(self) -> list:
        """
        Get available SNS topics from AWS.

        Returns
        -------
        list
            Already created topics available to use.

        """
        try:
            return self.__client.list_topics().get("Topics", [])
        except Exception as exc:
            print(exc)

    def create(self, name: str = None) -> None:
        """
        Create new SNS Topic using given name or object name value.

        Parameters
        ----------
        name : str, optional
            Name of SNS topic to create instead of object name
            defined during object initialization.

        """
        try:
            if name:
                self.name = name
            response = self.__client.create_topic(Name=self.name)
            self.arn = response.get("TopicArn", "")
            print(f"SNS Topic {self.name} Created.")
        except Exception as exc:
            print(exc)

    def delete(self) -> None:
        """
        Delete existing SNS Topic.

        """
        try:
            self.__client.delete_topic(TopicArn=self.arn)
            self.name = None
            self.arn = None
            print("SNS Topic Deleted.")
        except Exception as exc:
            print(exc)

    def subscribe(self, sqs: _SQSQueue) -> None:
        """
        Subscribe given SQS queue to SNS Topic.

        Parameters
        ----------
        sqs : SQSQueue
            Queue for which topic will be subscribed.

        """
        try:
            _boto3.resource('sns').Topic(self.arn).subscribe(
                Protocol="sqs", Endpoint=sqs.arn)
            print(f"SQS Queue {sqs.name} subscribed to SNS Topic {self.name}.")
        except Exception as exc:
            print(exc)
