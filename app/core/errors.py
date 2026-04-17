class AppError(Exception):
    status_code = 400
    error_code = "APP_ERROR"
    message = "Ошибка приложения"

    def __init__(self, *, message: str | None = None,
                 meta: dict | None = None):
        self.meta = meta or {}
        if message is not None:
            self.message = message
        super().__init__(self.message)


class UserAlreadyExistsError(AppError):
    status_code = 409
    error_code = "CONFLICT"

    def __init__(self, field: str):
        self.message = "{0} уже существует".format(field)


class UnauthorizedError(AppError):
    status_code = 401
    error_code = "UNAUTHORIZED"
    message = "Неверный пароль"


class ForbiddenError(AppError):
    status_code = 403
    error_code = "FORBIDDEN"
    message = "Действие запрещено"


class NotFoundError(AppError):
    status_code = 404
    error_code = "NOT_FOUND"

    def __init__(self, obj_name: str):
        self.message = "Объект {0} не найден в базе".format(obj_name)


class BadGatewayError(AppError):
    status_code = 502
    error_code = "BAD_GATEWAY"
    message = "Ошибка в шлюзе"


class ServiceUnavailableError(AppError):
    status_code = 503
    error_code = "SERVICE_UNAVAILABLE"
    message = "Сервис недоступен"


class GatewayTimeoutError(AppError):
    status_code = 504
    error_code = "GATEWAY_TIMEOUT"
    message = "Шлюз не отвечает"
