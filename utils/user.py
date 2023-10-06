import hashlib
import secrets


def verificar_usuario(password: str, bd_password: str) -> bool:

    form_pass = hash_password(password)
    current_password_bytes = form_pass.encode("utf8")
    correct_password_bytes = bd_password.encode("utf8")

    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )

    return is_correct_password


def hash_password(password: str) -> hashlib:
    """Función que cifra la contraseña en un hash determinado.

    Args:
        password: Contraseña a cifrar.

    Returns:
        Password cifrada.

    """
    h = hashlib.sha256()
    h.update(password.encode('utf-8'))

    return h.hexdigest()
