#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
import json
from threading import Thread

from replit.database import Database

repl_id = os.environ["REPL_ID"]
print(f"https://{repl_id}.id.repl.co")
db = Database(os.environ["REPLIT_DB_URL"])
print(db)

def main():

    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    @app.route('/', methods=['GET'])
    def home():
        return {}

    @app.route('/update', methods=['POST'])
    def updatedata():
        post_data = json.loads(request.data)
        d = list(post_data.keys())
        d.sort()
        if d == ['data', 'key']:
          key = post_data['key']
          
          t = {}
          t['__original__'] = post_data['data']
          db[key] = t
          return {'result': 'ok'}
        return {}

    @app.route('/get', methods=['GET'])
    @cross_origin()
    def getdata():
      try:
        keys = request.args.get('keys').lower()
        keys = keys.split('|')
        res = {}
        for _ in keys:
          if db.get(_):
            res[_] = json.loads(db.get_raw(_))

            if res[_].get('__original__'):
              res[_] = res[_].get('__original__')

        return {"result": res}
      except:
        return {}

    @app.route('/deleteall', methods=['GET'])
    @cross_origin()
    def deleteall():
      try:
        keys = db.keys()
        for _key in keys:
          del db[_key]

        return {"result": 'ok'}
      except:
        return {}

    def run():
        app.run(host='0.0.0.0')

    apiserver = Thread(target=run)
    apiserver.start()


if __name__ == '__main__':
    main()
