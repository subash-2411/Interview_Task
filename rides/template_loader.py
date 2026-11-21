import os
from pathlib import Path
from jinja2 import Environment
from django.http import HttpResponse
from .django_adapter import _storage

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'

def get_full_template_string(template_name, standalone=False):
    target_path = TEMPLATES_DIR / template_name
    if not target_path.exists():
        raise FileNotFoundError(f"Template {template_name} not found")
        
    target_content = target_path.read_text(encoding='utf-8')
    if template_name == 'base.html' or standalone:
        return target_content
        
    base_path = TEMPLATES_DIR / 'base.html'
    if not base_path.exists():
        return target_content
        
    base_content = base_path.read_text(encoding='utf-8')
    # If child template defines blocks or doesn't use base include, check
    if '{% include content_template %}' in base_content:
        return base_content.replace('{% include content_template %}', target_content)
    return target_content
