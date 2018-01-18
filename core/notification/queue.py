# -*- encoding: utf-8 -*-

"""
Module enable operations on AWS SQS Queue.

"""

import boto3 as _boto3

__version__ = ""
__author__ = "Mateusz Sitkowski"


class SQSQueue:
    """
    AWS Simple Queue Service.

    """

    def __init__(self, name: str) -> None:
        """
        Initialize sqs queue object.

        Parameters
        ----------
        name : str
            Queue name.

        """
        self.name = name
        self.arn = None
        self.url = None
        self.__client = _boto3.client('sqs')
        self.__resource = _boto3.resource("sqs")

    def get_existing_queue(self, name: str) -> bool:
        """
        Check if queue exists.

        Returns
        -------
        bool
            True if exists otherwise false.

        """
        for q in self.list_queues():
            if q and q.endswith(name):
                self.url = q
                self.arn = self.__resource.Queue(
                    self.url).attributes.get("QueueArn", "")
                return True
        return False

    def list_queues(self) -> list:
        """
        Get available SQS queues.

        Returns
        -------
        list
            Available SQS Queues.

        """
        try:
            return self.__client.list_queues().get("QueueUrls", [])
        except Exception as exc:
            print(exc)

    def create(self, name: str = None) -> None:
        """
        Create new SQS Queue.

        Parameters
        ----------
        name : str, optional
            Queue name. If not given, current name will be used.

        """
        try:
            if name:
                self.name = name
            response = self.__client.create_queue(QueueName=self.name)
            self.url = response.get("QueueUrl", "")
            self.arn = self.__resource.Queue(
                self.url).attributes.get("QueueArn", "")
            print(f"SQS Queue {self.name} Created.")
        except Exception as exc:
            print(exc)

    def delete(self) -> None:
        """
        Delete existing SQS Queue.

        """
        try:
            self.__client.delete_queue(TopicArn=self.url)
            self.name = None
            self.arn = None
            self.url = None
            print(f"SQS Queue Deleted.")
        except Exception as exc:
            print(exc)

    def receive_message(self) -> list:
        """
        Read messages from queue.

        Returns
        -------
        list
            Received messages.

        """
        try:
            return self.__client.receive_message(
                QueueUrl=self.url).get("Messages", [])
        except Exception as exc:
            print(exc)

    def delete_message(self, handle: str) -> None:
        """
        Delete message from queue.

        """
        try:
            self.__client.delete_message(
                QueueUrl=self.url, ReceiptHandle=handle)
        except Exception as exc:
            print(exc)
