from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common import log_manager
from db.executors import user
from models.request.user.update_user import UpdateUser
from models.request.user.create_user import CreateUser

logger = log_manager.initLogger()


async def get_all_user(db_session: AsyncSession):
    logger.info(f"Service: get all user information")
    return await user.get_all_users(db_session)


async def get_allow_feature_by_user_id(user_id: int, db_session: AsyncSession):
    logger.info(f"Service: get allow feature by user id %s", user_id)
    return await user.query_allow_feature_by_user_id(user_id, db_session)


async def get_user_by_id(user_id: int, db_session: AsyncSession):
    logger.info(f"Service: get user information by id %s", user_id)
    return await user.get_user_by_id(user_id, db_session)


async def patch_user_by_id(user_id: int, update_user: UpdateUser, db_session: AsyncSession):
    logger.info(f"Service: update user information by id %s", user_id)
    result = await user.update_user_by_id(user_id, update_user, db_session)
    if result is True:
        return {"result": "user information has been changed"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot update user information please contact admin"
        )


async def post_user(create_user: CreateUser, db_session: AsyncSession):
    logger.info(f"Service: create new user information")

    result = await user.insert_user(create_user, db_session)
    if result is True:
        return {"result": "user information has been inserted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot insert user information please contact admin"
        )


async def delete_user(user_id: int, db_session: AsyncSession):
    logger.info(f"Service: delete user information %s", user_id)

    result = await user.delete_user(user_id, db_session)
    if result is True:
        return {"result": "user information has been deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot delete user information please contact admin"
        )
