from flask import request
from flask import abort, make_response
from dns_balancer import DNS
from errors.custom_domain_already_exists_exception import CustomDomainAlreadyExistsException
from errors.missing_parameter_exception import MissingParameterException

def obtener_todos():
    """
        Esta funcion maneja el request GET /api/custom-domains?q=<string>

        :return:        200 lista de dominios custom registrados que contienen <string>
        """
    query = request.args.get('q') or ''
    return {'items': DNS.all(query=query, custom=True)}

def crear(**kwargs):
    """
        Esta funcion maneja el request POST /api/custom-domains
         :param body:  dominio a crear en la lista de dominios
        :return:        201 dominio creado, 400 body mal formado o el dominio ya existe.
        """
    new_domain = kwargs['body']

    try:
        result = DNS.save(new_domain)
    except (CustomDomainAlreadyExistsException, MissingParameterException) as e:
        return abort(400, str(e))

    return make_response(result, 201)

