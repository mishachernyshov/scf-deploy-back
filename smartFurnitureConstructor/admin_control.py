import os
from django.http import HttpResponse
from django.shortcuts import redirect


def update_cartificate(request):
    os.system('mkcert -cert-file cert.pem -key-file key.pem 0.0.0.0 localhost 127.0.0.1 ::1')

    return redirect("/admin")


def restore_db(request):
    os.system('py manage.py dbbackup')

    return redirect("/admin")


def restore(request):
    os.system('yes.bat | restore.bat')

    return redirect("/admin")
