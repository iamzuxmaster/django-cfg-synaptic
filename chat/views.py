from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from control.models import Account, Message, Room
import json
# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

import os

from django.http import HttpResponse
import socketio
sio = socketio.Server(async_mode=async_mode)
thread = None


def control_chat_all_messages(request:HttpRequest):
    data = json.loads(request.body)

    try: 
        account_a_id = data["req_id"]
    except Exception as e:
        answer = {
            "code": 403
        }
        return JsonResponse(answer, safe=False)

    try: 
        account_b_id = data["acc_id"]
    except:
        answer = {
            "code": 403
        }
        return JsonResponse(answer, safe=False)

    account_a = Account.objects.get(id=account_a_id)
    account_b = Account.objects.get(id=account_b_id)

    try:
        try:         
            room = Room.objects.get(account_a=account_a, account_b=account_b)
        except:
            room= Room.objects.get(account_a=account_b, account_b=account_a)
    except:
            room= Room.objects.create(account_a=account_a, account_b=account_b) 

    answer = {
        "code": 200,
        "chat": {"id": room.uuid},
        "messages": list(map(lambda message: {"message": {"account": {"id": message.sender.id}, "message": message.message}}, room.message_set.all()))
    }
    return JsonResponse(answer, safe=False)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')


@sio.event
def my_connect(sid, message):
    account = Account.objects.get(id=message["req_id"])
    account.online = True
    account.save()

    sio.emit('my_connect_response', {'data': 200}, room=sid)


@sio.event
def my_broadcast_event(sid, message):
    sio.emit('my_response', {'data': message['data']})


@sio.event
def join(sid, message):
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)


@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)


@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])


@sio.event
def my_room_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=message['room'])

@sio.event
def join_room(sid, message):
    sio.enter_room(sid, message["room_id"])
    sio.emit('joined_room', {'message': 200})


@sio.event
def sendmessage(sid, message):
    account = Account.objects.get(id=message["account_id"])
    room = Room.objects.get(uuid=message["room_id"])
    message = Message.objects.create(room=room, sender=account, message=message["message"])

    sio.emit('addmessage', {'message': {"account" : {"id": account.id}, "message":message.message }})



@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')
