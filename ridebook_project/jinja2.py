from jinja2 import Environment, FileSystemLoader
from django.templatetags.static import static
from django.urls import reverse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'

def format_booking_id(id_val):
    if not id_val:
        return "N/A"
    return f"RB-BK-{int(id_val):05d}"

def format_alert_id(id_val):
    if not id_val:
        return "N/A"
    return f"RB-SOS-{int(id_val):04d}"

def environment(**options):
    if 'loader' not in options:
        options['loader'] = FileSystemLoader(str(TEMPLATES_DIR))
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'len': len,
        'str': str,
        'int': int,
        'float': float,
        'list': list,
        'dict': dict,
        'set': set,
        'min': min,
        'max': max,
        'round': round,
        'range': range,
        'enumerate': enumerate,
        'zip': zip,
        'format_booking_id': format_booking_id,
        'format_alert_id': format_alert_id,
    })
    return env
