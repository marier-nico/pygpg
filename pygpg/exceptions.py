"""Exceptions for pygpg."""


class PyGPGError(Exception):
    """Base error for all pygpg related problems."""

    def __init__(self, msg=None):
        if msg is None:
            msg = "An unexpected error occurred"

        super().__init__(msg)


class KeyEditError(PyGPGError):
    """Error for errors that occur when editing keys."""

    def __init__(self, key_id: str, msg=None):
        if msg is None:
            msg = f"There was an error editing the GPG key with ID: {key_id}"

        super().__init__(msg)
        self.key_id = key_id
