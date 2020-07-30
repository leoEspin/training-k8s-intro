#!/usr/bin/python -u

import os
import json
import socket
import datetime
import web
import random

def load_jokes():
  global JOKES_LIST
  JOKES_LIST = json.load(open('jokes.json'))
  random.shuffle(JOKES_LIST)


# Endpoints
class health:
  def GET(self):
    return blahblah

class hello:
  def GET(self):
    return json.dumps({
      'msg': 'hello jello from ' + HOST, 
      'date': str(datetime.datetime.now())
    })

class joke:
  def GET(self):
    if not JOKES_LIST:
      load_jokes()
    joke = JOKES_LIST.pop()
    return json.dumps({
      'joke': joke,
      'host': HOST,
      'time': str(datetime.datetime.now())
    })
  def POST(self):
    return 'POST successful, but nothing useful has been implemented yet'

class goodbye:
  def GET(self):
    msg = json.dumps({
      'msg': 'goodbye cruel world, from ' + HOST,
      'date': str(datetime.datetime.now())
    })
    print(msg)
    return msg

if __name__ == '__main__':

  JOKES_LIST = []
  HOST = socket.gethostname()
  DEBUG = os.environ.get('DEBUG', False)

  ### map uris to classes
  urls = (
    '/health', 'health',
    '/hello', 'hello',
    '/', 'joke',
    '/goodbye', 'goodbye',
  )
  app = web.application(urls, globals())

  ### start http server
  web.httpserver.runsimple(app.wsgifunc(), ('0.0.0.0', 80))
