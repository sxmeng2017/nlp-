class LazyImport:

    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None

    def __getattr__(self, item):
        if self.module is None:
            self.module = __import__(self.module_name)
        return getattr(self.module, item)

string = LazyImport("numpy")
print(string.max([1,2,3,4]))