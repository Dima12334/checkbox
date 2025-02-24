from fastapi import HTTPException, status


class ExpiredTokenException(HTTPException):
    def __init__(self, message: str = "Token has expired."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)


class InvalidTokenException(HTTPException):
    def __init__(self, message: str = "Invalid token."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)


class InvalidUsernameOrPasswordException(HTTPException):
    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)


class ObjectAlreadyExistsException(HTTPException):
    def __init__(self, message: str = "Object already exists."):
        super().__init__(status.HTTP_409_CONFLICT, message)
