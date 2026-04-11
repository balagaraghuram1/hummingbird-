from src.services.auth_service import auth_service


def test_password_hash_and_verify() -> None:
    hashed = auth_service.hash_password("secret")
    assert auth_service.check_password("secret", hashed)

