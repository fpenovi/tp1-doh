from flask import request
from storage.domains import Domains

def obtener_todos():
    """
        Esta funcion maneja el request GET /api/custom-domains?q=<string>

        :return:        200 lista de dominios custom registrados que contienen <string>
        """
    query = request.args.get('q') or ''
    return {'items': Domains.filter_custom_by(query)}
