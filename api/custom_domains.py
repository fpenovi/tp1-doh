from flask import abort, make_response

CUSTOM_DOMAINS = {
    'custom1.fi.uba.ar': {
        'domain': 'custom1.fi.uba.ar',
        'ip': '1.1.1.1',
        'custom': True
    }
}

def obtener_todos():
    """
        Esta funcion maneja el request GET /api/custom-domains?q=<string>

        :return:        200 lista de dominios custom registrados que contienen <string>
        """
    search_result = [CUSTOM_DOMAINS['custom1.fi.uba.ar']]
    return {'items': search_result}
