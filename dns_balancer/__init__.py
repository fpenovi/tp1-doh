import dns.resolver
from storage.domains import CustomDomainRepository
from dns_balancer.dns_balancer import DNSBalancer

DNS = DNSBalancer(dns.resolver, CustomDomainRepository())
