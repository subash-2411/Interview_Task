import json
from functools import wraps
from asgiref.local import Local
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

_storage = Local()

class FlaskRequestProxy:
    def __init__(self, django_request):
        self._req = django_request
        self.method = django_request.method
        self.path = django_request.path
        self.args = dict(django_request.GET.items())
        
        form_data = dict(django_request.POST.items())
        self.form = form_data
        
        self.headers = {k: v for k, v in django_request.headers.items()}
        self._json = None
        if django_request.content_type == 'application/json' or 'application/json' in django_request.META.get('CONTENT_TYPE', ''):
            try:
                self._json = json.loads(django_request.body.decode('utf-8'))
            except Exception:
                self._json = None
        else:
            try:
                self._json = json.loads(django_request.body.decode('utf-8'))
            except Exception:
                self._json = None

    def get_json(self, silent=True):
        return self._json

    @property
    def json(self):
        return self._json or {}

    @property
    def is_json(self):
        return self._json is not None

    @property
    def remote_addr(self):
        return self._req.META.get('REMOTE_ADDR', '127.0.0.1')

    def __getattr__(self, name):
        return getattr(self._req, name)


class FlaskSessionProxy:
    def __init__(self, django_session):
        self._session = django_session

    def get(self, key, default=None):
        return self._session.get(key, default)

    def __getitem__(self, key):
        return self._session[key]

    def __setitem__(self, key, value):
        self._session[key] = value
        self._session.modified = True

    def __delitem__(self, key):
        if key in self._session:
            del self._session[key]
            self._session.modified = True

    def __contains__(self, key):
        return key in self._session

    def pop(self, key, default=None):
        val = self._session.pop(key, default)
        self._session.modified = True
        return val

    def clear(self):
        self._session.clear()
        self._session.modified = True


class RequestLocalProxy:
    def __getattr__(self, name):
        req = getattr(_storage, 'request_proxy', None)
        if req is None:
            raise RuntimeError("Working outside of request context")
        return getattr(req, name)

    def __getitem__(self, item):
        req = getattr(_storage, 'request_proxy', None)
        if req is None:
            raise RuntimeError("Working outside of request context")
        return req[item]


class SessionLocalProxy:
    def __getattr__(self, name):
        sess = getattr(_storage, 'session_proxy', None)
        if sess is None:
            raise RuntimeError("Working outside of session context")
        return getattr(sess, name)

    def __getitem__(self, item):
        sess = getattr(_storage, 'session_proxy', None)
        if sess is None:
            raise RuntimeError("Working outside of session context")
        return sess[item]

    def __setitem__(self, item, value):
        sess = getattr(_storage, 'session_proxy', None)
        if sess is None:
            raise RuntimeError("Working outside of session context")
        sess[item] = value

    def __delitem__(self, item):
        sess = getattr(_storage, 'session_proxy', None)
        if sess is None:
            raise RuntimeError("Working outside of session context")
        del sess[item]

    def __contains__(self, item):
        sess = getattr(_storage, 'session_proxy', None)
        if sess is None:
            return False
        return item in sess

    def get(self, key, default=None):
        sess = getattr(_storage, 'session_proxy', None)
        if sess is None:
            return default
        return sess.get(key, default)

    def pop(self, key, default=None):
        sess = getattr(_storage, 'session_proxy', None)
        if sess is None:
            return default
        return sess.pop(key, default)

    def clear(self):
        sess = getattr(_storage, 'session_proxy', None)
        if sess is not None:
            sess.clear()


request = RequestLocalProxy()
session = SessionLocalProxy()


def jsonify(*args, **kwargs):
    if args and not kwargs:
        if len(args) == 1:
            return JsonResponse(args[0], safe=False)
        return JsonResponse(list(args), safe=False)
    return JsonResponse(kwargs, safe=False)


def render_template(template_name, **context):
    from .template_renderer import render_app_template
    return render_app_template(template_name, **context)


def redirect(location, code=302):
    return HttpResponseRedirect(location)


def Response(content=b'', status=200, mimetype=None, content_type=None, headers=None, **kwargs):
    ct = content_type or mimetype or 'text/plain'
    resp = HttpResponse(content, status=status, content_type=ct)
    if headers:
        for k, v in headers.items():
            resp[k] = v
    return resp


def bridge_view(func):
    @wraps(func)
    @csrf_exempt
    def wrapper(django_req, *args, **kwargs):
        _storage.django_request = django_req
        _storage.request_proxy = FlaskRequestProxy(django_req)
        _storage.session_proxy = FlaskSessionProxy(django_req.session)
        try:
            result = func(django_req, *args, **kwargs)
            if isinstance(result, tuple):
                body = result[0]
                status_code = result[1] if len(result) > 1 else 200
                headers = result[2] if len(result) > 2 else {}
                if isinstance(body, (HttpResponse, JsonResponse, HttpResponseRedirect)):
                    body.status_code = status_code
                    for k, v in headers.items():
                        body[k] = v
                    return body
                elif isinstance(body, (dict, list)):
                    resp = JsonResponse(body, status=status_code, safe=not isinstance(body, list))
                    for k, v in headers.items():
                        resp[k] = v
                    return resp
                else:
                    resp = HttpResponse(str(body), status=status_code)
                    for k, v in headers.items():
                        resp[k] = v
                    return resp
            elif isinstance(result, (HttpResponse, JsonResponse, HttpResponseRedirect)):
                return result
            elif isinstance(result, (dict, list)):
                return JsonResponse(result, safe=not isinstance(result, list))
            elif isinstance(result, str):
                return HttpResponse(result)
            return result
        finally:
            _storage.django_request = None
            _storage.request_proxy = None
            _storage.session_proxy = None
    return wrapper
