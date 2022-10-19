from flask_jwt_extended import get_jwt


def admin_group_required(func):
    """
    Decorator which requires admin jwt token permission for executing functions
    """
    def wrapper(*args, **kwargs):
        jwt = get_jwt()
        if "admin" not in jwt.get("groups", []):
            return {"message": "Forbidden"}, 403

        result = func(*args, **kwargs)
        return result
    wrapper.__name__ = func.__name__
    return wrapper