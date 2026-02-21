from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import HTTPException, status
import os
from dotenv import load_dotenv

from auth_models import AdminUser

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # Increased to 2 hours

class AuthService:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    
    def verify_password(self, plain_password: str, password: str) -> bool:
        """Simple password verification (for demo only)"""
        return plain_password == password
    
    def get_password_hash(self, password: str) -> str:
        """Simple password hashing (for demo only)"""
        return password  # In production, use proper hashing
    
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[AdminUser]:
        """Authenticate a user"""
        user = db.query(AdminUser).filter(AdminUser.username == username).first()
        if not user:
            return None
        if not user.is_active:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
            return payload
        except JWTError:
            return None
    
    def get_current_user(self, db: Session, token: str) -> Optional[AdminUser]:
        """Get current user from token"""
        payload = self.verify_token(token)
        if payload is None:
            return None
        
        username = payload.get("sub")
        user = db.query(AdminUser).filter(AdminUser.username == username).first()
        if user is None:
            return None
        if not user.is_active:
            return None
        
        return user
    
    def login_user(self, db: Session, username: str, password: str) -> Tuple[str, AdminUser]:
        """Login user and return token"""
        user = self.authenticate_user(db, username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": user.username, "role": user.role, "full_name": user.full_name},
            expires_delta=access_token_expires
        )
        
        return access_token, user

# Global auth service instance
auth_service = AuthService()
