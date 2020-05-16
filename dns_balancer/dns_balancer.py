from time import time
from dns.resolver import NoNameservers
from errors.external_domain_not_found_exception import ExternalDomainNotFoundException


def swap(ix_1, ix_2, array):
    tmp = array[ix_2]
    array[ix_2] = array[ix_1]
    array[ix_1] = tmp
    return array


class DNSBalancer:
    def __init__(self, resolver, storage):
        self.storage = storage
        self.resolver = resolver
        self.cached = {}

    def all(self, query='', custom=None):
        if custom is True:
            return self.storage.filter_by(query)

        if custom is False:
            raise NotImplementedError()

        raise NotImplementedError()

    def save(self, new_custom_domain):
        return self.storage.save(new_custom_domain)

    def resolve(self, domain_name):
        if self.storage.has(domain_name):
            return self.storage[domain_name]

        if self.__cached(domain_name):
            return self.__get_from_cache(domain_name)

        try:
            result = self.__get_external(domain_name)
        except NoNameservers:
            raise ExternalDomainNotFoundException(f"domain '{domain_name}' not found")

        return result

    def update(self, domain_name, update_domain):
        return self.storage.update(domain_name, update_domain)

    def __cached(self, domain_name):
        if domain_name not in self.cached:
            return False

        if time() < self.cached[domain_name]['expiration']:
            return True

        self.cached[domain_name]['expiration'] = 0  # Invalidate cache
        return False

    def __get_from_cache(self, domain_name):
        cached_domain = self.cached[domain_name]
        ip_index = cached_domain['times_requested'] % len(cached_domain['ips'])
        cached_domain['last_ip_used'] = cached_domain['ips'][ip_index]
        cached_domain['times_requested'] += 1
        return self.__format(domain_name, cached_domain['ips'][ip_index])

    def __get_external(self, domain_name):
        raw_result = self.resolver.query(domain_name).response.answer.pop()
        ttl = raw_result.ttl
        ip_addresses = list(map(lambda ip_result: ip_result.address, raw_result.items))
        is_cached = domain_name in self.cached

        # Caso borde: cuando el ttl se vence y el IP primero en la lista devuelta por el servicio resulta ser
        #               el mismo que devolvi la ultima vez, por ende no quiero devolverlo nuevamente.
        if is_cached and self.cached[domain_name]['last_ip_used'] == ip_addresses[0] and len(ip_addresses) > 1:
            ip_addresses = swap(0, len(ip_addresses) - 1, ip_addresses)

        self.cached[domain_name] = {'ips': ip_addresses,
                                    'custom': False,
                                    'expiration': time() + ttl,
                                    'times_requested': 0,
                                    'last_ip_used': None}

        return self.__get_from_cache(domain_name)

    @staticmethod
    def __format(domain_name, ip):
        return {'domain': domain_name, 'ip': ip, 'custom': False}

