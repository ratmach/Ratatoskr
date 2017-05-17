# In consumers.py
import json

from channels import Group
from channels.sessions import channel_session

# Connected to websocket.connect
from Ratatoskr.apps import RatatoskrGenerator
from Ratatoskr.model_god import ModelGod


@channel_session
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip("/")
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("chat-%s" % room).add(message.reply_channel)


# Connected to websocket.receive
@channel_session
def ws_message(message):
    text_ = message['text']
    loads = json.loads(text_)
    split = loads["model"].split('.')
    appName = split[0]
    modelName = split[1]
    data = loads['data']
    method = loads['method']
    response = ModelGod.getHandleFunction(app_name=appName, model_name=modelName, data=data, method=method)
    Group("chat-%s" % message.channel_session['room']).send({
        "text": response,
    })


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
