class DuplicateRecordError(Exception):
    """for handling duplicate records in the database"""
    pass


class DataValidationError(Exception):
    """incomplete data before passing it into the database"""
    pass


