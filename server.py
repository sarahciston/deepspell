#!/usr/bin/env python
# -*- coding: utf-8 -*-
# server.py

from deepspell import dspell
from flask import Flask, Response
app = Flask(__name__)


FILE_URL = 'https://cdn.glitch.com/155d0693-823a-4ff9-a75d-d5b22fccb7c1%2Fcjsjvu0x105xc0160slv1nzp2.wav'

@app.route('/goSpell')
def goSpell():
    FILE_URL = 'https://cdn.glitch.com/155d0693-823a-4ff9-a75d-d5b22fccb7c1%2Fcjsjvu0x105xc0160slv1nzp2.wav' #gqlDB() #this used to be the query route
    # spellText = ''
    return Response("<h1>Url is: /%s</h1>" % (FILE_URL), mimetype="text/html")


@app.route('/cloud')
def cloud(FILE_URL):
  text = fSpell(FILE_URL)
  return Response("/%s" % text)

# @app.route("/")# def hello():
#   return "Hello World!"
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response("<h1>Flask on Docker Config</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")

if __name__ == "__main__":
  app.run()
