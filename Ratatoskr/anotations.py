def handleRequest(method=None):
    def registrar(func):
        func.__ratamethod__ = method
        return func
    return registrar
handler = handleRequest
