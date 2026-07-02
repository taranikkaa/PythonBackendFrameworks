from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Bcrypt introduces an intentional work-factor delay making brute-force
    # attacks computationally expensive unlike legacy algorithms like MD5/SHA-1 (Step 89)
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)