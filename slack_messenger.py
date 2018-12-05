import json
import requests
import logging
import sys

def handler(event, context):
    logger = log_init()
    logger.info(event)

    for record in event['Records']:
        logger.debug("Event: {}".format(record))

        message = json.loads(record['body'])
        app = message['application']
        release = message['release']
        status = message['stage']
        webhook_url = message['webhook_url']

    return send_message(app, release, status, webhook_url)

def send_message(app, release, status, webhook_url):
    logger = log_init()
    logger.debug("Application: {}\tRelease: {}\tStatus: {}".format(app, release, status))
    message = "{} of {} is currently in the {} stage".format(release, app, status)
    slack_message = json.dumps({ 'text': message, 'attachments': [
        {
            'title': '{} CodePipeline'.format(app),
            'title_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }
    ] })
    try:
        response = requests.post(
            webhook_url,
            data=slack_message,
            headers={'Content-Type': 'application/json'}
        )

        logger.debug(response)
        if response.status_code == 200:
            logger.info("message successfully submitted!")
        elif response.status_code != 200:
            logger.warn("message submission failed: {}\t{}".format(response.status_code, response.text))
    except requests.exceptions.RequestException as e:
        logger.error(e)

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