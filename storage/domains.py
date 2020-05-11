import copy

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
    CUSTOM_KEY = 'custom'
    DOMAIN_KEY = 'domain'
    IP_KEY = 'ip'

    def __init__(self, domains={}):
        self.domains = copy.deepcopy(domains)

    def custom(self):
        return list(filter(lambda d: d[self.CUSTOM_KEY], self.domains.values()))

    def filter_custom_by(self, search):
        custom_domains = self.custom()
        results = filter(lambda d: search in d[self.DOMAIN_KEY], custom_domains)
        return list(results)


Domains = __DomainCollection(__DOMAINS)
