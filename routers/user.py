from fastapi import APIRouter, Depends, HTTPException

from db.database_engine import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from error_handler.route_error import throw_db_general_error
from models.request.user.create_user import CreateUser
from models.request.user.update_user import UpdateUser
from services import user
from common import log_manager

logger = log_manager.initLogger()
logger.info('API is starting up')
router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={503: {"message": "Service unavailable"}}
)


@router.get("/list/all")
async def get_all_user(db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: get all user information")
    try:
        return await user.get_all_user(db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.get("/{user_id}/allow-features")
async def get_allow_feature_by_user_id(user_id: int, db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: get all feature by user_group_id %s", user_id)
    try:
        return await user.get_allow_feature_by_user_id(user_id, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.get("/{user_id}")
async def get_user_by_id(user_id: int,
                         db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: get user info by id %s", user_id)
    try:
        return await user.get_user_by_id(user_id, db_session)
    except Exception as error:
        throw_db_general_error(error)


@router.patch("/{user_id}")
async def patch_user_by_id_route(user_id: int,
                                 patch_body: UpdateUser,
                                 db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: patch user info by id %s", user_id)
    try:
        return await user.patch_user_by_id(user_id, patch_body, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.post("")
async def post_user(post_body: CreateUser,
                    db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: post new user info")
    try:
        return await user.post_user(post_body, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: delete user info by id %s", user_id)
    try:
        return await user.delete_user(user_id, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)
