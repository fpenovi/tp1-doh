import copy
from errors.missing_parameter_exception import MissingParameterException
from errors.custom_domain_already_exists_exception import CustomDomainAlreadyExistsException

__DOMAINS = {
    'custom1.fi.uba.ar': {
        'domain': 'custom1.fi.uba.ar',
        'ip': '1.1.1.1',
        'custom': True
    },
    'custom2.fi.uba.ar': {
        'domain': 'custom2.fi.uba.ar',
        'ip': '2.2.2.2',
        'custom': True
    },
    'www.yahoo.com': {
        'domain': 'www.yahoo.com',
        'ip': '160.49.91.10',
        'custom': False
    }
}

class __DomainCollection:
    DOMAIN_KEY = 'domain'
    IP_KEY = 'ip'
    CUSTOM_KEY = 'custom'

    def __init__(self, domains={}):
        self.domains = copy.deepcopy(domains)
        self.__validate([self.DOMAIN_KEY, self.IP_KEY, self.CUSTOM_KEY])

    def __validate(self, req_keyset=(DOMAIN_KEY, IP_KEY, CUSTOM_KEY)):
        for domain in self.domains.values():
            self.__validate_one(domain, req_keyset)

    def __validate_one(self, domain, req_keyset=(DOMAIN_KEY, IP_KEY)):
        for key in req_keyset:
            if key not in domain.keys():
                raise MissingParameterException(f'missing parameter: {key}')

    def custom(self):
        return list(filter(lambda d: d[self.CUSTOM_KEY], self.domains.values()))

    def filter_custom_by(self, search):
        custom_domains = self.custom()
        results = filter(lambda d: search in d[self.DOMAIN_KEY], custom_domains)
        return list(results)

    def save(self, new_domain):
        self.__validate_one(new_domain)
        new_domain_name = new_domain[self.DOMAIN_KEY]

        if new_domain_name in self.domains:
            raise CustomDomainAlreadyExistsException('custom domain already exists')

        new_domain[self.CUSTOM_KEY] = True
        self.domains[new_domain_name] = new_domain
        return new_domain


Domains = __DomainCollection(__DOMAINS)
