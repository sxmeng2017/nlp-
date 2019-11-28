class Headers:

    def __init__(self, defaults=None, _list=None):
        if _list is None:
            _list = []
        self._list = _list
        if defaults is not None:
            self.extend(defaults)


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

