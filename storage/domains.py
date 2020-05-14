import copy
from errors.missing_parameter_exception import MissingParameterException
from errors.custom_domain_already_exists_exception import CustomDomainAlreadyExistsException

class CustomDomainRepository:
    DOMAIN_KEY = 'domain'
    IP_KEY = 'ip'
    CUSTOM_KEY = 'custom'

    def __init__(self, domains={}):
        self.domains = copy.deepcopy(domains)
        self.__validate([self.DOMAIN_KEY, self.IP_KEY, self.CUSTOM_KEY])

    def __getitem__(self, domain_name):
        return self.domains[domain_name]

    def __validate(self, req_keyset=(DOMAIN_KEY, IP_KEY, CUSTOM_KEY)):
        for domain in self.domains.values():
            self.__validate_one(domain, req_keyset)

    def __validate_one(self, domain, req_keyset=(DOMAIN_KEY, IP_KEY)):
        for key in req_keyset:
            if key not in domain.keys():
                raise MissingParameterException(f'missing parameter: {key}')

    def filter_by(self, search):
        results = filter(lambda d: search in d[self.DOMAIN_KEY], self.domains.values())
        return list(results)

    def save(self, new_domain):
        self.__validate_one(new_domain)
        new_domain_name = new_domain[self.DOMAIN_KEY]

        if new_domain_name in self.domains:
            raise CustomDomainAlreadyExistsException('custom domain already exists')

        new_domain[self.CUSTOM_KEY] = True
        self.domains[new_domain_name] = new_domain
        return new_domain

    def has(self, domain_name):
        return domain_name in self.domains
