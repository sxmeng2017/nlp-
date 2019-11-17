"""
werkzeug中Rule类，其中不少方法的实现要涉及map，但self.map初始
为None。经过查找，才明白。在Map类中的bind会调用MapAdapter类。而MapAdapter
类中会遍历每个Rule。其中MapAdapter的初始化参数有map。在这里，Rule对象能发现一个map
并传入，
"""

def bind(self, map, rebind=False):
    """Bind the url to a map and create a regular expression based on
    the information from the rule itself and the defaults from the map.

    :internal:
    """
    if self.map is not None and not rebind:
        raise RuntimeError("url rule %r already bound to map %r" % (self, self.map))
    self.map = map # 在这里将MapAdapter中map参数传给了rule
    if self.strict_slashes is None:
        self.strict_slashes = map.strict_slashes
    if self.subdomain is None:
        self.subdomain = map.default_subdomain
    self.compile()

class MapAdapter(object):

    """Returned by :meth:`Map.bind` or :meth:`Map.bind_to_environ` and does
    the URL matching and building based on runtime information.
    """

    def __init__(
        self,
        map,
        server_name,
        script_name,
        subdomain,
        url_scheme,
        path_info,
        default_method,
        query_args=None,
    ):
        self.map = map
        self.server_name = to_unicode(server_name)
        script_name = to_unicode(script_name)
        if not script_name.endswith(u"/"):
            script_name += u"/"
        self.script_name = script_name
        self.subdomain = to_unicode(subdomain)
        self.url_scheme = to_unicode(url_scheme)
        self.path_info = to_unicode(path_info)
        self.default_method = to_unicode(default_method)
        self.query_args = query_args