from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_password(passwd: str) -> str:
    return password_context.hash(passwd)


def verify_password(passwd: str, hashed_passwd: str) -> bool:
    return password_context.verify(passwd, hashed_passwd)
