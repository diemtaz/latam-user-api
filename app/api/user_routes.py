

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter(tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserRepository.create(db, user)


@router.get(
    "/",
    response_model=list[UserResponse]
)
def list_users(db: Session = Depends(get_db)):
    return UserService.get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(user_id: str, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(db, user_id)

@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: str,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    return UserService.update_user(db, user_id, user)

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    UserService.delete_user(db, user_id)
    return

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def replace_user(
    user_id: str,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return UserService.replace_user(db, user_id, user)

