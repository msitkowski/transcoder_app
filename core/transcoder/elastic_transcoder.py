# -*- encoding: utf-8 -*-

"""
Module enable operations on AWS Elastic transcoder
(handling pipelines and jobs).

"""

import boto3 as _boto3

from .presets import Presets as _Presets
from .job_status import JobStatus as _JobStatus
from core.location import Location as _Location
from core.bucket.bucket import Bucket as _Bucket
from core.notification.topic import SNSTopic as _SNSTopic

__version__ = ""
__author__ = "Mateusz Sitkowski"


class ElasticTranscoder:
    """
    Class representing AWS Elastic Transcoder.

    """

    def __init__(self, location: _Location) -> None:
        """
        Initialize ElasticTranscoder object for specific location.

        Parameters
        ----------
        location : Location
            Location of server providing service.

        """
        self.__client = _boto3.client("elastictranscoder")
        self.location = location.value
        self.pipeline_id = None

    def list_pipelines(self) -> list:
        """
        Get dictionary with available pipelines.

        Returns
        -------
        list
            Available pipelines.

        """
        try:
            return self.__client.list_pipelines().get("Pipelines", [])
        except Exception as exc:
            print(exc)

    def get_existing_pipeline(self, name: str) -> bool:
        """
        Check if pipeline exists.

        Returns
        -------
        bool
            True if exists otherwise false.

        """
        for p in self.list_pipelines():
            if p and p.get('Name', "") == name:
                self.pipeline_id = p.get("Id")
                return True
        return False

    def create_pipeline(self, name: str, input_bucket: _Bucket,
                        output_bucket: _Bucket, sns_topic: _SNSTopic) -> dict:
        """
        Create new pipeline for Elastic Transcoder.

        Returns
        -------
        dict
            Created pipeline specification.

        """
        try:
            arn = _boto3.resource('iam').Role(
                    'Elastic_Transcoder_Default_Role').arn
            response = self.__client.create_pipeline(
                Name=name,
                InputBucket=input_bucket.name,
                OutputBucket=output_bucket.name,
                Role=arn,
                Notifications={
                    "Progressing": sns_topic.arn,
                    "Completed": sns_topic.arn,
                    "Warning": sns_topic.arn,
                    "Error": sns_topic.arn
                })
            pipeline = response.get("Pipeline", {})
            if pipeline:
                self.pipeline_id = pipeline.get("Id", "")
                print(f"Created Pipeline {self.pipeline_id}",
                      f"")
                return pipeline
            else:
                raise Exception("Create pipeline error!")
        except Exception as exc:
            print(exc)

    def delete_pipeline(self) -> None:
        """
        Delete Elastic Transcoder pipeline.

        """
        try:
            self.__client.delete_pipeline(Id=self.pipeline_id)
            self.pipeline_id = None
        except Exception as exc:
            print(exc)

    def create_job(self, input_key: str, output_key: str,
                   preset: _Presets, output_prefix: str) -> str:
        """

        Parameters
        ----------
        input_key : str
        output_key : str
        preset : Presets
        output_prefix : str

        Returns
        -------
        str
            Created job id.

        """
        try:
            job_id = self.__client.create_job(
                PipelineId=self.pipeline_id,
                Input={
                    'Key': input_key,
                },
                OutputKeyPrefix=output_prefix,
                Output={
                    "Key": output_key,
                    "PresetId": preset.value,
                }
            ).get("Job", {}).get("Id", "")
            print(f"Created job {job_id}")
            return job_id
        except Exception as exc:
            print(exc)

    def cancel_job(self, job_id: str) -> None:
        try:
            self.__client.cancel_job(job_id)
            print(f"Job {job_id} canceled.")
        except Exception as exc:
            print(exc)

    def list_jobs_by_status(
            self, status: _JobStatus = _JobStatus.COMPLETE) -> list:
        return self.__client.list_jobs_by_status(
            Status=status.value).get("Jobs", [])

    def list_jobs_by_pipeline(self) -> list:
        return self.__client.list_jobs_by_pipeline(
            PipelineId=self.pipeline_id).get("Jobs", [])
