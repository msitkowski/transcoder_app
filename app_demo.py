# -*- encoding: utf-8 -*-

"""
App demo.

"""

from time import sleep
from json import loads

from core.acl import ACL
from core.location import Location
from core.bucket.bucket import Bucket
from core.notification.topic import SNSTopic
from core.notification.queue import SQSQueue
from core.transcoder.presets import Presets
from core.transcoder.job_status import JobStatus
from core.transcoder.elastic_transcoder import ElasticTranscoder

# create SNS Topic
sns_topic = SNSTopic(name="test-demo-app-topic")

if not sns_topic.get_existing_topic(sns_topic.name):
    sns_topic.create()

# create SQS Queue
sqs_queue = SQSQueue(name="test-demo-app-queue")

if not sqs_queue.get_existing_queue(sqs_queue.name):
    sqs_queue.create()

# subscribe SQS Queue for SNS Topic
# sns_topic.subscribe(sqs=sqs_queue)

# create bucket for input data
input_bucket = Bucket(
    name="test-demo-app-input-bucket",
    acl=ACL.PRIVATE, location=Location.IRELAND)

if not input_bucket.get_existing_bucket(input_bucket.name):
    input_bucket.create()

# upload data to input bucket
input_bucket.upload(
    key="test-demo-app-movie.mp4",
    filename="res/funny_cat_movie.mp4")

not_uploaded = True

while not_uploaded:
    sleep(2)
    for f in input_bucket.list_files():
        if f and f.get("Key", "") == "test-demo-app-movie.mp4":
            not_uploaded = False
            break

# create output bucket
output_bucket = Bucket(
    name="test-demo-app-output-bucket",
    acl=ACL.PRIVATE, location=Location.IRELAND)

if not output_bucket.get_existing_bucket(output_bucket.name):
    output_bucket.create()

# create Elastic Transcoder object
elastic_transcoder = ElasticTranscoder(Location.IRELAND)

# create pipeline
if not elastic_transcoder.get_existing_pipeline("test-demo-app-pipeline"):
    elastic_transcoder.create_pipeline(
        name="test-demo-app-pipeline",
        input_bucket=input_bucket,
        output_bucket=output_bucket,
        sns_topic=sns_topic
    )

# create job and wait for notification about it
job = elastic_transcoder.create_job(
    input_key="test-demo-app-movie.mp4",
    output_key="transcoded-test-demo-app-movie.mp4",
    preset=Presets.HD720p, output_prefix='720p/'
)

# listing jobs
elastic_transcoder.list_jobs_by_pipeline()

# waiting for job complete notification
sleep(2)
notifications = sqs_queue.receive_message()

while notifications:
    for n in notifications:
        notification = loads(loads(n.get("Body")).get("Message"))
        print("State:", notification.get("state"),
              "Job id:", notification.get("jobId"))
        sqs_queue.delete_message(n.get("ReceiptHandle"))
    sleep(2)
    notifications = sqs_queue.receive_message()
