from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class MemcachedRequires(RelationBase):
    scope = scopes.UNIT
    auto_accessors = ['private-address']

    @hook('{requires:memcache}-relation-{joined,changed}')
    def changed(self):
        if self.memcache_hosts():
            self.set_state('{relation_name}.available')

    @hook('{requires:memcache}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.available')


    def get_remote_all(self, key, default=None):
        '''Return a list of all values presented by remote units for key'''
        values = []
        for conversation in self.conversations():
            for relation_id in conversation.relation_ids:
                for unit in hookenv.related_units(relation_id):
                    value = hookenv.relation_get(key,
                                                 unit,
                                                 relation_id) or default
                    if value:
                        values.append(value)
        return list(set(values))

    def memcache_hosts(self):
        return self.get_remote_all('private-address')
