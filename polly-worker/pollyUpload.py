#!/usr/bin/env python
import requests
import sys
import os
from kubemq.queue.message_queue import MessageQueue
from kubemq.queue.message import Message
from boto3 import Session
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import logging
from tempfile import gettempdir
token = os.getenv("NOTION_TOKEN")

headers = {
  'Notion-Version': '2022-02-22',
  'Authorization': f'Bearer {token}'
}

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
  channel = "queues.single"
  queue = MessageQueue(channel, "audio-notion-polly-receiver", "localhost:50000", 2, 1)
  try:
    res = queue.receive_queue_messages()
    if res.error:
        print(
            "'Received:'%s'" % (
                res.error
            )
        )
    else:
        for message in res.messages:
            meta = message.metadata
            print(
                "'Received :%s ,Body: sending:'%s'" % (
                    message.MessageID,
                    message.Body
                )
            )
            
            # Create a client using the credentials and region defined in the [adminuser]
            # section of the AWS credentials file (~/.aws/credentials).
            session = Session(profile_name="adminuser")
            polly = session.client("polly")

            try:
                # Request speech synthesis
                response = polly.synthesize_speech(Text=message.Body, OutputFormat="mp3",
                                                    VoiceId="Joanna",Engine = 'neural')
            except (BotoCoreError, ClientError) as error:
                # The service returned an error, exit gracefully
                print(error)
                sys.exit(-1)

            # Access the audio stream from the response
            if "AudioStream" in response:
                # Note: Closing the stream is important because the service throttles on the
                # number of parallel connections. Here we are using contextlib.closing to
                # ensure the close method of the stream object will be called automatically
                # at the end of the with statement's scope.
                    with closing(response["AudioStream"]) as stream:
                        output = os.path.join(gettempdir(), "speech.mp3")

                    try:
                        # Open a file for writing the output as a binary stream
                        with open(output, "wb") as file:
                            file.write(stream.read())
                    except IOError as error:
                        # Could not write to file, exit gracefully
                        print(error)
                        sys.exit(-1)
                    upload_file(f"output-{meta}.mp3", "audio-notion-recordings")
            else:
                # The response didn't contain audio data, exit gracefully
                print("Could not stream audio")
                sys.exit(-1)
  except Exception as err:
      print(
          "'error sending:'%s'" % (
              err
          )
      )
