# # app/auth/utils/password.py
# import bcrypt

# def hash_password(password: str) -> str:
#     """Hash a password using bcrypt"""
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password.decode('utf-8')

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a password against its hash"""
#     return bcrypt.checkpw(
#         plain_password.encode('utf-8'),
#         hashed_password.encode('utf-8')
#     )

import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hased_password:str) -> bool:
    """verify plain password with hashed password"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hased_password.encode('utf-8'))
