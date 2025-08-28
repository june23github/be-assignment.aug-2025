from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import User, Organization
from schemas.user import UserCreate
from core.hash import hash_password


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        # existing_username = db.query(User).filter(User.username == user_data.username).first()
        # if existing_username:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="Username already taken"
        #     )
        
        organization = db.query(Organization).filter(Organization.id == user_data.organization_id).first()
        if not organization:
            raise HTTPException(
                status_code=400,
                detail="Organization not found"
            )
        
        hashed_password = hash_password(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            role=user_data.role,
            organization_id=user_data.organization_id
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user


    