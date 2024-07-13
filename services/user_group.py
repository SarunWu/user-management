from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common import log_manager
from db.executors import user_group
from models.request.user_group.create_user_group import CreateUserGroup
from models.request.user_group.update_user_group import UpdateUserGroup

logger = log_manager.initLogger()


async def get_all_user_group(mode: str, db_session: AsyncSession):
    logger.info(f"Service: get all user group information with %s mode", mode)
    match mode:
        case "full":
            return await user_group.get_full_detail_user_group(db_session)
        case "brief":
            return await user_group.get_brief_detail_user_group(db_session)
        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request mode {mode}, please specify only 'full' or 'brief'"
            )


async def get_user_group_by_id(user_group_id: int, mode: str, db_session: AsyncSession):
    logger.info(f"Service: get user group information by id %s", user_group_id)
    match mode:
        case "full":
            return await user_group.get_full_user_group_by_id(user_group_id, db_session)
        case "brief":
            return await user_group.get_brief_user_group_by_id(user_group_id, db_session)
        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request mode {mode}, please specify only 'full' or 'brief'"
            )


async def get_allow_feature_by_group_id(user_group_id: int, db_session: AsyncSession):
    logger.info(f"Service: get allow feature by user group id %s", user_group_id)
    return await user_group.query_allow_feature_by_group_id(user_group_id, db_session)


async def patch_user_group_by_id(user_group_id: int, update_user_group: UpdateUserGroup, db_session: AsyncSession):
    logger.info(f"Service: update user group information by id %s", user_group_id)
    result = await user_group.update_user_group_by_id(user_group_id, update_user_group, db_session)
    if result is True:
        return {"result": "User group information has been changed"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot update user group information please contact admin"
        )


async def post_user_group(create_user_group: CreateUserGroup, db_session: AsyncSession):
    logger.info(f"Service: create new user group information")

    result = await user_group.insert_user_group(create_user_group, db_session)
    if result is True:
        return {"result": "User group information has been inserted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot insert user group information please contact admin"
        )


async def delete_user_group(user_group_id: int, db_session: AsyncSession):
    logger.info(f"Service: delete user group information %s", user_group_id)

    result = await user_group.delete_user_group(user_group_id, db_session)
    if result is True:
        return {"result": "User group information has been deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot delete user group information please contact admin"
        )
