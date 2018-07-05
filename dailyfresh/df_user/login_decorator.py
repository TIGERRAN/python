# coding=utf-8

from django.http import HttpResponse, HttpResponseRedirect


def verify_login(func):
    def wrapper(request, *args, **kwargs):
        if request.session.has_key('user_name'):
            return func(request, *args, **kwargs)
        else:
            response = HttpResponseRedirect('/user/login/')
            request_path = request.get_full_path()
            request.session['request_path'] = request_path
            # response.set_cookie('request_path', request_path)

            return response

    return wrapper