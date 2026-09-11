import logging

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from .schemas import UserCreate, UserUpdate


logger = logging.getLogger(__name__)


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str
):
    logger.info(
        "Authentication attempt",
        extra={
            "event": "authentication_attempt",
            "operation": "login"
        }
    )

    try:
        statement = select(models.User).where(
            models.User.email == email
        )

        result = await db.execute(statement)
        user = result.scalars().first()

        if not user:
            logger.warning(
                "Authentication failed",
                extra={
                    "event": "authentication_failed",
                    "operation": "login",
                    "reason": "user_not_found"
                }
            )
            return None

        password_correct = bcrypt.checkpw(
            password.encode("utf-8"),
            user.password_hash.encode("utf-8")
        )

        if not password_correct:
            logger.warning(
                "Authentication failed",
                extra={
                    "event": "authentication_failed",
                    "operation": "login",
                    "reason": "invalid_credentials"
                }
            )
            return None

        logger.info(
            "Authentication successful",
            extra={
                "event": "authentication_success",
                "operation": "login",
                "user_id": user.id
            }
        )

        return user

    except Exception as exc:
        logger.exception(
            "Authentication operation failed",
            extra={
                "event": "authentication_error",
                "operation": "login",
                "error_type": type(exc).__name__
            }
        )
        raise


async def create_user(
    db: AsyncSession,
    user_data: UserCreate
):
    logger.info(
        "Creating new user",
        extra={
            "event": "user_creation_started",
            "operation": "create_user"
        }
    )

    try:
        hashed_password = bcrypt.hashpw(
            user_data.password.encode("utf-8"),
            bcrypt.gensalt()
        )

        new_user = models.User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password.decode("utf-8")
        )

        db.add(new_user)

        await db.commit()
        await db.refresh(new_user)

        logger.info(
            "User created successfully",
            extra={
                "event": "user_created",
                "operation": "create_user",
                "user_id": new_user.id
            }
        )

        return new_user

    except Exception as exc:
        logger.exception(
            "User creation failed",
            extra={
                "event": "user_creation_error",
                "operation": "create_user",
                "error_type": type(exc).__name__
            }
        )
        raise


async def get_user(
    db: AsyncSession,
    user_id: int
):
    logger.info(
        "Fetching user",
        extra={
            "event": "user_fetch_started",
            "operation": "get_user",
            "user_id": user_id
        }
    )

    try:
        statement = select(models.User).where(
            models.User.id == user_id
        )

        result = await db.execute(statement)

        user = result.scalars().first()

        if user:
            logger.info(
                "User fetched successfully",
                extra={
                    "event": "user_fetched",
                    "operation": "get_user",
                    "user_id": user_id
                }
            )
        else:
            logger.warning(
                "User not found",
                extra={
                    "event": "user_not_found",
                    "operation": "get_user",
                    "user_id": user_id
                }
            )

        return user

    except Exception as exc:
        logger.exception(
            "Failed to fetch user",
            extra={
                "event": "user_fetch_error",
                "operation": "get_user",
                "user_id": user_id,
                "error_type": type(exc).__name__
            }
        )
        raise


async def get_users(
    db: AsyncSession,
    search: str | None,
    page: int,
    page_size: int
):
    logger.info(
        "Fetching users",
        extra={
            "event": "users_fetch_started",
            "operation": "get_users",
            "page": page,
            "page_size": page_size
        }
    )

    try:
        statement = select(models.User)

        if search:
            logger.info(
                "Applying user search filter",
                extra={
                    "event": "user_search_applied",
                    "operation": "get_users"
                }
            )

            statement = statement.where(
                models.User.name.ilike(f"%{search}%")
                |
                models.User.email.ilike(f"%{search}%")
            )

        offset = (page - 1) * page_size

        statement = (
            statement
            .order_by(models.User.id)
            .offset(offset)
            .limit(page_size)
        )

        result = await db.execute(statement)
        users = result.scalars().all()

        logger.info(
            "Users fetched successfully",
            extra={
                "event": "users_fetched",
                "operation": "get_users",
                "result_count": len(users),
                "page": page,
                "page_size": page_size
            }
        )

        return users

    except Exception as exc:
        logger.exception(
            "Failed to fetch users",
            extra={
                "event": "users_fetch_error",
                "operation": "get_users",
                "page": page,
                "page_size": page_size,
                "error_type": type(exc).__name__
            }
        )
        raise


async def update_user(
    db: AsyncSession,
    user: models.User,
    user_data: UserUpdate
):
    logger.info(
        "Updating user",
        extra={
            "event": "user_update_started",
            "operation": "update_user",
            "user_id": user.id
        }
    )
    try:
        user.name = user_data.name
        user.email = user_data.email

        await db.commit()
        await db.refresh(user)

        logger.info(
            "User updated successfully",
            extra={
                "event": "user_updated",
                "operation": "update_user",
                "user_id": user.id
            }
        )

        return user

    except Exception as exc:
        logger.exception(
            "User update failed",
            extra={
                "event": "user_update_error",
                "operation": "update_user",
                "user_id": user.id,
                "error_type": type(exc).__name__
            }
        )
        raise


async def delete_user(
    db: AsyncSession,
    user: models.User
):
    logger.info(
        "Deleting user",
        extra={
            "event": "user_deletion_started",
            "operation": "delete_user",
            "user_id": user.id
        }
    )

    try:
        await db.delete(user)
        await db.commit()

        logger.info(
            "User deleted successfully",
            extra={
                "event": "user_deleted",
                "operation": "delete_user",
                "user_id": user.id
            }
        )

    except Exception as exc:
        logger.exception(
            "User deletion failed",
            extra={
                "event": "user_deletion_error",
                "operation": "delete_user",
                "user_id": user.id,
                "error_type": type(exc).__name__
            }
        )
        raise