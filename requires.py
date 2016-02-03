from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes
import telnetlib


class MemcachedRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:memcache}-relation-{joined,changed}')
    def changed(self):
        if self.memcache_hosts():
            self.set_state('{relation_name}.available')

    @hook('{requires:memcache}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.available')

    def memcache_hosts(self):
        """
        Return a list of services requesting databases.
        Example usage::

            @when('memcache.available')
            def render_config(memcache):
                render_template('django.conf', context={
                    'memcache_hosts': memcache.memcache_hosts(),
                })
        """
        for conv in self.conversations():
            priv_addy = conv.get_remote('private-address')
            priv_port =  conv.get_remote('port')
            if priv_addy and priv_port:
                yield (priv_addy, priv_port)
