from flask import request
from flask import abort, make_response
from dns_balancer import DNS
from errors.custom_domain_already_exists_exception import CustomDomainAlreadyExistsException
from errors.custom_domain_payload_invalid_exception import CustomDomainPayloadInvalid
from errors.missing_parameter_exception import MissingParameterException
from errors.custom_domain_not_found_exception import CustomDomainNotFoundException

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

def actualizar(**kwargs):
    """
            Esta funcion maneja el request PUT /api/custom-domains/<domain>
             :param body:  dominio a actualizar en la lista de dominios
            :return:        200 dominio actualizado, 400 body mal formado, 404 dominio no encontrado.
            """

    domain_name = kwargs['domain_name']
    update_domain = kwargs['body']

    try:
        result = DNS.update(domain_name, update_domain)
    except (MissingParameterException, CustomDomainPayloadInvalid) as e:
        return abort(400, str(e))
    except CustomDomainNotFoundException as e:
        return abort(404, str(e))

    return make_response(result, 200)
