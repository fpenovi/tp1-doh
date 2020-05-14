import dns.resolver
from storage.domains import CustomDomainRepository
from dns_balancer.dns_balancer import DNSBalancer

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
    }
}

DNS = DNSBalancer(dns.resolver, CustomDomainRepository(__DOMAINS))
