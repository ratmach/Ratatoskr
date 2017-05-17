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
    try:
        response_string = handle_request(message)
    except Exception as e :
        response_string  ="{\"exception\" : \""+str(e) +"\" }"
    Group("chat-%s" % message.channel_session['room']).send({
        "text": str(response_string),
    })


def handle_request(message):
    text_ = message['text']
    request = json.loads(text_)
    split = request["model"].split('.')
    app_name = split[0]
    model_name = split[1]
    data = request['data']
    method = request['method']
    model = ModelGod.get_model(app_name, model_name)
    handler = ModelGod.getHandleFunction(model, data=data, method=method)
    response = {}
    data = request['data']
    if handler is not None:
        response = handler(None, data)
    else:
        if method == "CREATE":
            created = model.objects.create(**data)
            response = created
        elif method == "GET":
            got = model.objects.get(id=data['id'])
            response = got
        elif method == "UPDATE":
            old = model.objects.get(id=data['id'])
            for attr in data:
                setattr(old, attr, data[attr])
            old.save()
            response = old
        elif method == "DELETE":
            model.objects.get(id=data['id']).delete()
            response = "deleted"
    response_string = json_from_data(response)
    return response_string


def json_from_data(object):
    if type(object) is str:
        return object
    elif type(object) is dict:
        return json.dumps(object)
    json_data = {}
    for field in object._meta.fields:
        json_data[field.name] = getattr(object, field.name)
    return json.dumps(json_data)


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
