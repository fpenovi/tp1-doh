from flask import request
from storage.domains import Domains
from flask import abort, make_response

def obtener_todos():
    """
        Esta funcion maneja el request GET /api/custom-domains?q=<string>

        :return:        200 lista de dominios custom registrados que contienen <string>
        """
    query = request.args.get('q') or ''
    return {'items': Domains.filter_custom_by(query)}

def crear(**kwargs):
    """
        Esta funcion maneja el request POST /api/custom-domains
         :param body:  dominio a crear en la lista de dominios
        :return:        201 dominio creado, 400 body mal formado o el dominio ya existe.
        """
    new_domain = kwargs['body']
    return make_response(Domains.save(new_domain), 201)

