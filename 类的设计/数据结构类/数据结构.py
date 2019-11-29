class Headers:

    KeyError = None
    def __init__(self, defaults=None, _list=None):
        if _list is None:
            _list = []
        self._list = _list
        if defaults is not None:
            self.extend(defaults)

    @classmethod
    def linked(cls, headerlist):
        return cls(_list=headerlist)

    def __getitem__(self, key, _index_operation=True):
        if _index_operation:
            if isinstance(key, (int)):
                return self._list[key]
            elif isinstance(key, slice):
                return self.__class__(self._list[key])
        ikey = key.lower()
        for k, v in self._list:
            if k.lower() == ikey:
                return v
        raise self.KeyError(key)

    def __eq__(self, other):
        return other.__class__ is self.__class__ and \
                set(other._list) == set(self._list)

    def __ne__(self, other):
        return not self.__eq__(other)

    def get(self, key, default=None, type=None):
        try:
            rv = self.__getitem__(key, _index_operation=False)
        except KeyError:
            return default
        if type is None:
            return rv
        try:
            return type(rv)
        except ValueError:
            return default

    def getlist(self, key, type=None):
        ikey = key.lower()
        result = []
        for k, v in self:
            if k.lower() == ikey:
                if type is not None:
                    try:
                        v = type(v)
                    except ValueError:
                        continue
                result.append(v)
        return result

    def get_all(self, name):
        return self.getlist(name)

    def iteritems(self, lower=False):
        for key, value in self:
            if lower:
                key = key.lower()
            yield key, value

    def iterkeys(self, lower=False):
        for key, _ in self:
            if lower:
                key = key.lower()
            yield key

    def itervalues(self):
        for _, value in self:
            yield value

    def keys(self, lower=False):
        return list(self.iterkeys(lower))

    def values(self):
        return list(self.itervalues())

    def items(self, lower=False):
        return list(self.iteritems(lower))

    def extend(self, iterable):
        if isinstance(iterable, dict):
            for key, value in iterable.iteritems():
                if isinstance(value, (tuple, list)):
                    for v in value:
                        self.add(key, v)

                else:
                    self.add(key, v)
        else:
            for key, value in iterable:
                self.add(key, value)

    def __delitem__(self, key, _index_operation=True):
        """
        用于删除特定键值
        :param key:
        :param _index_operation:
        :return:
        """
        if _index_operation and isinstance(key, (int, long, slice)):
            del self._list[key]
            return
        key = key.lower()
        new = []
        for k, v in self._list:
            if k.lower() != key:
                new.append((k, v))
        self._list[:] = new

    def remove(self, key):
        """Remove a key.
        :param key: The key to be removed.
        """
        return self.__delitem__(key, _index_operation=False)

    def pop(self, key=None, default=_missing):

        if key is None:
            return self._list.pop()
        if isinstance(key, (int, long)):
            return self._list.pop(key)
        try:
            rv = self[key]
            self.remove(key)
        except KeyError:
            if default is not _missing:
                return default
            raise
        return rv

    def __contains__(self, item):
        try:
            self.__getitem__(item, _index_operation=False)
        except KeyError:
            return False
        return True

    has_key = __contains__

    def __iter__(self):
        """Yield ``(key, value)`` tuples."""
        return iter(self._list)

    def __len__(self):
        return len(self._list)

    def popitem(self):
        return self.pop()

    def add(self, _key, _value, **kwargs):
        if kwargs:
            _value = dump_options_header(_value, dict((k.replace('_', '-'), v)
                                                      for k, v in kwargs.items()))
        self._append((_key, _value))

    def add_header(self, _key, _value, **kwargs):
        self.add(_key, _value, **kwargs)

    def clear(self):
        del self._list[:]

    def set(self, key, value):
        lc_key = key.lower()
        for idx, (old_key, old_value) in enumerate(self._list):
            if old_key.lower() == lc_key:
                self._list[idx] = (key, value)
                break
        else:
            return self.add(key, value)
        self._list[idx + 1:] = [(k, v) for k, v in self._list[idx + 1:]
                                if k.lower() != lc_key]

    def setdefault(self, key, value):
        if key in self:
            return self[key]
        self.set(key, value)
        return value

    def __setitem__(self, key, value):
        if isinstance(key, (slice, key, value)):
            self._list[key] = value
        else:
            self.set(key, value)

    def to_list(self, charset='utf-8'):
        """Convert the headers into a list and converts the unicode header
        items to the specified charset.
        :return: list
        """
        result = []
        for k, v in self:
            if isinstance(v, unicode):
                v = v.encode(charset)
            else:
                v = str(v)
            result.append((k, v))
        return result

    def copy(self):
        return self.__class__(self._list)

    def __copy__(self):
        return self.copy()

    def __str__(self, charset='utf-8'):
        strs = []
        for key, value in self.to_list(charset):
            strs.append('%s: %s' % (key, value))
        strs.append('\r\n')
        return '\r\n'.join(strs)

    def __repr__(self):
        return '%s(%r)' % (
            self.__class__.__name__,
            list(self)
        )