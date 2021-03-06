#!/usr/bin/env python
import requests
import sys
import os
from kubemq.queue.message_queue import MessageQueue
from kubemq.queue.message import Message
token = os.getenv("NOTION_TOKEN")

headers = {
  'Notion-Version': '2021-05-13',
  'Authorization': f'Bearer {token}'
}

if __name__ == "__main__":
  channel = "queues.single"
  queue = MessageQueue(channel, "audio-notion-url-receiver", "localhost:50000", 2, 1)
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
            page_id = message.Body.url[-32:]
            url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
            response = requests.get(url, headers=headers)
            full_text = []
            for result in response.json()["results"]:
              if "paragraph" in result:
                  for text in result["paragraph"]["text"]:
                      full_text.append(text["plain_text"])

            full_text = '\n'.join(map(str, full_text))
  except Exception as err:
      print(
          "'error sending:'%s'" % (
              err
          )
      )

  # Send item to AWS Polly Queue
  queue = MessageQueue(channel, "polly-queue-client", "localhost:50000")
  message = Message()
  message.metadata = meta
  message.body = full_text.encode('UTF-8')
  message.attributes = None
  try:
      sent = queue.send_queue_message(message)
      if sent.error:
          print('message enqueue error, error:' + sent.error)
      else:
          print('Send to Queue  at: %d' % (
              sent.sent_at
          ))
  except Exception as err:
      print('message enqueue error, error:%s' % (
          err
      ))
