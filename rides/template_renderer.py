import os
import re
from pathlib import Path
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
from .flask_bridge import _storage

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'

STANDALONE_TEMPLATES = {
    'admin_sos.html',
    'auth_loader.html',
    'e_ticket.html',
    'forgot_password.html',
    'login.html',
    'login_admin.html',
    'login_driver.html',
    'login_rider.html',
    'register.html',
    'register_driver.html',
    'sos_track.html',
    'verify.html',
    'base.html'
}

def render_app_template(template_name, **context):
    req = getattr(_storage, 'django_request', None)
    req_proxy = getattr(_storage, 'request_proxy', None)
    sess_proxy = getattr(_storage, 'session_proxy', None)
    
    ctx = dict(context)
    ctx['context'] = ctx
    if req_proxy is not None:
        ctx['request'] = req_proxy
    if sess_proxy is not None:
        ctx['session'] = sess_proxy

    # Inject content_template into context so Jinja can resolve any reference
    ctx['content_template'] = template_name

    # Check if this template should be wrapped in base.html
    is_standalone = context.get('standalone', False) or (template_name in STANDALONE_TEMPLATES)
    
    from ridebook_project.jinja2 import environment
    env = environment()

    if is_standalone:
        tmpl = env.get_template(template_name)
        content = tmpl.render(ctx)
        return HttpResponse(content)

    base_path = TEMPLATES_DIR / 'base.html'
    target_path = TEMPLATES_DIR / template_name
    
    if not target_path.exists():
        return HttpResponse(f"Template {template_name} not found", status=404)
        
    base_content = base_path.read_text(encoding='utf-8')
    target_content = target_path.read_text(encoding='utf-8')

    # Replace all content_template includes with actual target template code
    merged = re.sub(r'{%\s*include\s+content_template\s*%}', lambda m: target_content, base_content)
    
    tmpl = env.from_string(merged)
    content = tmpl.render(ctx)
    return HttpResponse(content)
