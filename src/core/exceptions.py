from fastapi import HTTPException, status


class ExpiredTokenException(HTTPException):
    def __init__(self, message: str = "Token has expired."):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message
        super().__init__(self.status_code, self.message)


class InvalidTokenException(HTTPException):
    def __init__(self, message: str = "Invalid token."):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message
        super().__init__(self.status_code, self.message)


class InvalidUsernameOrPasswordException(HTTPException):
    def __init__(self, message: str = "Invalid email or password."):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message
        super().__init__(self.status_code, self.message)


class ObjectAlreadyExistsException(HTTPException):
    def __init__(self, message: str = "Object already exists."):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message
        super().__init__(self.status_code, self.message)
