class ExchangeError(Exception):
    """Errors from the crypto exchange"""
    pass

class InvalidSymbolError(Exception):
    """Symbol does not exist on the exchange"""
    pass

class FetchError(Exception):
    """General fetch failure"""
    pass
