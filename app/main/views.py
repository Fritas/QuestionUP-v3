"""
    Controller da aplicacao principal
"""

from . import main

@main.route('/')
def index():
    return 'Index da aplicacao principal'