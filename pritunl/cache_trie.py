from constants import *
from cache import cache_db

class CacheTrie(object):
    __slots__ = ('name', 'key')

    def __init__(self, name, key=''):
        self.name = name
        self.key = key

    def get_cache_key(self, suffix=None):
        key = '%s_%s' % (self.name, self.key)
        if suffix is not None:
            key += '_' + suffix
        return key

    def get_nodes(self):
        return cache_db.set_elements(self.get_cache_key())

    def add_value(self, value):
        cache_db.set_add(self.get_cache_key('values'), value)

    def get_values(self):
        return cache_db.set_elements(self.get_cache_key('values'))

    def add_key(self, key, value):
        name = self.name + '_'
        cur_key = self.key
        new_key = cur_key
        for char in key:
            new_key += char
            cache_db.set_add(name + cur_key, new_key)
            cur_key = new_key
        cache_db.set_add(name + cur_key + '_values', value)

    def remove_key(self, key, value):
        name = self.name + '_'
        cur_key = self.key
        new_key = cur_key
        for char in key:
            new_key += char
            cache_db.set_remove(name + cur_key, new_key)
            cur_key = new_key
        cache_db.set_remove(name + cur_key + '_values', value)

    def chain(self, values):
        name = self.name
        for node_key in self.get_nodes():
            CacheTrie(name, node_key).chain(values)
        node_values = self.get_values()
        if node_values:
            values.update(node_values)
        return values

    def get_prefix(self, prefix):
        return CacheTrie(self.name, prefix).chain(set())

    def iter_prefix(self, prefix):
        for value in CacheTrie(self.name, prefix).chain(set()):
            yield value
