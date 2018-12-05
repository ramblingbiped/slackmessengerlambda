#!/usr/bin/python3

import boto3
import argparse
import logging
import sys
import json
from botocore.exceptions import ClientError

arg_parser= argparse.ArgumentParser(description='Simple script for publishing a message to an SQS Queue for Slack Notifications')
arg_parser.add_argument("-a", "--application", type=str, required=True, help="Specifies the application associated with the build")
arg_parser.add_argument("-r", "--release", type=str, required=True, help="The release version/identifier associated with the artifiact being built")
arg_parser.add_argument("-s", "--status", type=str, required=True, help="The status of the build relative to a specific stage of the build process")
arg_parser.add_argument("-w", "--webhook", type=str, required=True, help="The Slack webhook to publish the message to")
arg_parser.add_argument("-q", "--queue", type=str, required=True, help="The SQS queue URL")
args = arg_parser.parse_args()

PROFILE = "rbiped"
REGION = "us-west-2"


boto3.setup_default_session(profile_name=PROFILE, region_name=REGION)
client = boto3.client('sqs')

application_name = args.application
release_version = args.release
build_status = args.status
webhook_url = args.webhook
queue_url = args.queue


def publish_message():
    logger = log_init()
    message_src = {
        "application": application_name,
        "release": release_version,
        "stage": build_status,
        "webhook_url": webhook_url
    }

    message = json.dumps(message_src)
    logger.debug(message)
    try:
        response = client.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )
        logger.info("Message Published: {}".format(response))
    except ClientError as e:
        logger.debug(e)
        logger.error(e['Error']['Message'])

def log_init():
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)
    h = logging.StreamHandler(sys.stdout)
    FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
    h.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    return logger

publish_message()