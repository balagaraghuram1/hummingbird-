from src.config.security import create_access_token, get_password_hash, verify_password


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return get_password_hash(password)

    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        return verify_password(password, hashed)

    @staticmethod
    def issue_token(user_id: str) -> str:
        return create_access_token(subject=user_id)


auth_service = AuthService()

