from fastapi import APIRouter, Depends, HTTPException

from db.database_engine import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from error_handler.route_error import throw_db_general_error
from models.request.user_group.create_user_group import CreateUserGroup
from models.request.user_group.update_user_group import UpdateUserGroup
from services import user_group
from common import log_manager

logger = log_manager.initLogger()
logger.info('API is starting up')
router = APIRouter(
    prefix="/user-group",
    tags=["User Group"],
    responses={503: {"message": "Service unavailable"}}
)


@router.get("/{user_group_id}/allow-features")
async def get_all_feature_by_user_group_id(user_group_id: int, db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: get all feature by user_group_id %s", user_group_id)
    try:
        return await user_group.get_allow_feature_by_group_id(user_group_id, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.get("/list/all/{mode}")
async def get_all_user_group(mode: str, db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: get all user group information")
    try:
        return await user_group.get_all_user_group(mode, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.get("/{user_group_id}/{mode}")
async def get_user_group_by_id(user_group_id: int, mode: str,
                               db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: get user group info by id %s with mode %s", user_group_id, mode)
    try:
        return await user_group.get_user_group_by_id(user_group_id, mode, db_session)
    except Exception as error:
        throw_db_general_error(error)


@router.patch("/{user_group_id}")
async def patch_user_group_by_id(user_group_id: int,
                                 patch_body: UpdateUserGroup,
                                 db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: patch user group info by id %s", user_group_id)
    try:
        return await user_group.patch_user_group_by_id(user_group_id, patch_body, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.post("")
async def post_user_group(post_body: CreateUserGroup,
                          db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: post new user group info")
    try:
        return await user_group.post_user_group(post_body, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.delete("/{user_group_id}")
async def delete_user_group(user_group_id: int, db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: delete user group info by id %s", user_group_id)
    try:
        return await user_group.delete_user_group(user_group_id, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)
