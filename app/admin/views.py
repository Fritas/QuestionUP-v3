"""
    Controller da aplicacao de administracao
"""

from flask import current_app, abort, request
from . import admin

@admin.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Desligando servidor...'