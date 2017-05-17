def handleRequest(method=None):
    registry = {}

    def registrar(func):
        registry["s"] = func
        func.__ratamethod__ = method
        return func

    registrar.all = registry
    return registrar


handler = handleRequest
