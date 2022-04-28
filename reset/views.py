from django.http import HttpRequest
from django.shortcuts import redirect, render
from control.tasks import send_email
from reset.models import UserPasswordReset
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from dateutil.relativedelta import relativedelta
from dateutil import parser
import datetime


def unix_stamp(date):
    now = datetime.datetime.now()
    return  now.hour >= int(date.strftime('%H'))+5

# Create your views here.
def index(request):
    try: 
        code = request.build_absolute_uri().split('?')[1]
    except: 
        code = None
    context = {
        "code": code
    }
    return render(request, "reset/index.html", context)

def reset_email(request: HttpRequest):
    if request.method == "POST": 
        send_email.send(request.POST["email"], host= request.build_absolute_uri().split("://")[0] + "://" + request.get_host())
    return redirect("/reset/?sended")

def reset_password(request: HttpRequest, hash):
    user_reset = UserPasswordReset.objects.get(hash=hash)

    if user_reset.complete == False and unix_stamp(user_reset.date_created): 
        context = {
            "secure_hash": hash
        }
        return render(request, "reset/reset_password.html", context)
    else:
        return redirect("/reset/?errror/")   

def reset_password_create(request: HttpRequest, hash):
    if request.method == "POST": 
        hash = request.POST["hash"]
        new_password = request.POST["new_password"]
        password_hash = PBKDF2PasswordHasher()
        user_reset = UserPasswordReset.objects.get(hash=hash)
        user_reset.user.password = password_hash.encode(password=new_password, salt="salt", iterations=50000)
        user_reset.user.save()
        user_reset.complete = True
        user_reset.save()
        return redirect("/reset/?edited")   