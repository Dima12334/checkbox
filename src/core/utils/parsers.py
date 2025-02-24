from typing import List

from pydantic import ValidationError


def parse_pydantic_validation_error(exception: ValidationError) -> List[str]:
    errors = []
    for error in exception.errors():
        field = ".".join([str(el) for el in error["loc"]])
        message = error["msg"]
        errors.append(f"{field}: {message}")

    return errors
