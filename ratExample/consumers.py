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
    app_name = split[0]
    model_name = split[1]
    data = loads['data']
    method = loads['method']

    model = ModelGod.get_model(app_name, model_name)
    handler = ModelGod.getHandleFunction(model, data=data, method=method)
    if handler is not None:
        handler(None, data)
    else:
        model.objects.create(**loads['data'])
    Group("chat-%s" % message.channel_session['room']).send({
        "text": text_,
    })


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
