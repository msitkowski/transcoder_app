# -*- encoding: utf-8 -*-

"""
Module enable operations on AWS S3 Bucket.

"""

import boto3 as _boto3

from core.acl import ACL as _ACL
from core.location import Location as _Location

__version__ = ""
__author__ = "Mateusz Sitkowski"


class Bucket:
    """
    Class representing AWS S3 bucket.

    """

    def __init__(self, name: str, acl: _ACL.PRIVATE,
                 location: _Location.IRELAND) -> None:
        """
        Bucket object initialization.

        Parameters
        ----------
        name : str
            Bucket name.

        """
        self.__client = _boto3.client("s3")
        self.name = name
        self.acl = acl.value
        self.location = location.value

    def get_existing_bucket(self, name: str) -> bool:
        """
        Check if bucket exists.

        Returns
        -------
        bool
            True if exists otherwise false.

        """
        for b in self.list_buckets():
            if b and b.get('Name', "") == name:
                return True
        return False

    def create(self) -> None:
        """
        Create new bucket in AWS S3.

        """
        try:
            response = self.__client.create_bucket(
                ACL=self.acl, Bucket=self.name,
                CreateBucketConfiguration={
                    "LocationConstraint": self.location
                }
            )
            print(f"Bucket {self.name} has been created. "
                  f"Access link: {response.get('Location')}")
        except Exception as exc:
            print(exc)

    def delete(self) -> None:
        """
        Deletes the bucket from AWS S3. Bucket must be empty.

        """
        try:
            self.__client.delete_bucket(Bucket=self.name)
            print(f"Bucket {self.name} has been deleted.")
        except Exception as exc:
            print(exc)

    def download(self, key: str, filename: str) -> None:
        """
        Download a file from AWS S3 bucket.

        Parameters
        ----------
        key : str
        filename : str

        """
        try:
            s3 = _boto3.resource("s3")
            s3.Bucket(self.name).download_file(key, filename)
            print(f"File {key} downloaded from bucket {self.name}."
                  f"File saved as {filename}")
        except Exception as exc:
            print(exc)

    def upload(self, key: str, filename: str) -> None:
        """
        Upload a file to an AWS S3 bucket.

        Parameters
        ----------
        key : str
        filename : str

        """
        try:
            self.__client.upload_file(filename, self.name, key)
        except Exception as exc:
            print(exc)

    def list_files(self) -> list:
        """
        Returns some or all (up to 1000) of the objects in a bucket.

        Returns
        -------
        list
            Files stored in bucket.

        """
        return self.__client.list_objects(Bucket=self.name).get("Contents", [])

    @classmethod
    def list_buckets(cls):
        buckets = [bucket for bucket in _boto3.client(
            "s3").list_buckets().get('Buckets', [])]
        return buckets
