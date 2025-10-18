class DatabaseError(Exception):
    """Generic DB exception."""

    def __init__(self, *args) -> None:
        super().__init__(*args)


class DataBaseIntegrityError(DatabaseError):
    pass


class NotFoundError(DatabaseError):
    pass
