from __future__ import annotations


class AppError(Exception):
    status_code = 500
    code = "app_error"

    def __init__(self, detail: str, *, code: str | None = None, status_code: int | None = None) -> None:
        super().__init__(detail)
        self.detail = detail
        if code is not None:
            self.code = code
        if status_code is not None:
            self.status_code = status_code


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"


class AuthError(AppError):
    status_code = 401
    code = "auth_error"


class ConflictError(AppError):
    status_code = 409
    code = "conflict"
