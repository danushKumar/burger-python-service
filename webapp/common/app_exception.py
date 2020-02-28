class AppException(Exception):

    # code = 123
    # cause = 'app exception'
    def __init__(self, error_codes, cause=None):
        super().__init__()
        self.codes = error_codes
        self.cause = cause

    