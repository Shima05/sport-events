class ServiceError(Exception):
    """Service errors."""


class ValidationError(ServiceError):
    """Validation error."""
