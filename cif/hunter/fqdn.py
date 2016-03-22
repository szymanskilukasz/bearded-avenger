import dns.resolver
import logging
import copy
from cif.utils import resolve_ns
from pprint import pprint


class Fqdn(object):

    def __init__(self, *args, **kv):
        self.logger = logging.getLogger(__name__)

    def _resolve_mx(self, data):
        r = resolve_ns(data, 'MX')
        return [rr.exchange for rr in r]

    def _resolve_ns(self, data):
        return resolve_ns(data, 'NS')

    def process(self, i, router):
        if i.itype == 'fqdn':
            r = self._resolve(i.indicator)
            for rr in r:
                ip = copy.deepcopy(i)
                ip.indicator = str(rr)
                ip.itype = 'ipv4'
                ip.confidence = (int(ip.confidence) / 2)
                x = router.submit(ip)
                self.logger.debug(x)

            r = self._resolve_ns(i.indicator)
            for rr in r:
                ip = copy.deepcopy(i)
                ip.indicator = str(rr)
                ip.itype = 'ipv4'
                ip.confidence = (int(ip.confidence) / 3)
                x = router.submit(ip)
                self.logger.debug(x)

            for rr in r:
                ip = copy.deepcopy(i)
                ip.indicator = str(rr)
                ip.itype = 'ipv4'
                ip.confidence = (int(ip.confidence) / 4)
                x = router.submit(ip)
                self.logger.debug(x)


Plugin = Fqdn