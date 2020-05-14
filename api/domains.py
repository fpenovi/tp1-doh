from flask import abort, make_response
from dns_balancer import DNS
from errors.external_domain_not_found_exception import ExternalDomainNotFoundException

def obtener_uno(domain_name):
    """
        Esta funcion maneja el request GET /api/domains/{domain_name}

         :domain_name body:  nombre del dominio que se quiere obtener
        :return:        200 dominio, 404 dominio no encontrado
        """
    try:
        domain = DNS.resolve(domain_name)
    except ExternalDomainNotFoundException as e:
        return abort(404, str(e))

    return make_response(domain, 200)
