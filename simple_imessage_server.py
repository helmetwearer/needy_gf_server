#!/usr/bin/env python
# encoding: utf-8
import os
from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)
SCRIPT_CONTENT = '''
    on run {targetBuddyPhone, targetMessage}
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy targetBuddyPhone of targetService
            send targetMessage to targetBuddy
        end tell
    end run
'''
send_script_path = Path.home().joinpath('send.applescript')

@app.route('/message', methods=['POST']) 
def message():
    phone = request.form['phone']
    message = request.form['message']
    stream = os.popen('osascript %s %s "%s"' % (send_script_path, phone, message))
    output = stream.read()
    return '\"%s\" sent to %s' % (message, phone)


if __name__ == '__main__':
    f = open(send_script_path, "w")
    f.write(SCRIPT_CONTENT)
    f.close()
    app.run(host='0.0.0.0', port=1337)