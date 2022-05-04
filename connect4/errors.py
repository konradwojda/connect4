class InvalidNameError(Exception):
    pass


class InvalidPlayerCount(Exception):
    pass


class InvalidColumnError(Exception):
    pass


class InvalidDataError(Exception):
    pass


class DatabasePathNotFound(FileNotFoundError):
    pass


class DatabasePermissionError(PermissionError):
    pass


class DatabasePathIsDirectory(IsADirectoryError):
    pass


class FileIsEmptyError(Exception):
    pass


class ColumnIsFullError(Exception):
    pass


class ColumnOutOfRangeError(Exception):
    pass
