from fastapi import APIRouter, Depends, HTTPException

from db.database_engine import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from error_handler.route_error import throw_db_general_error
from models.request.feature.create_feature import CreateFeature
from models.request.feature.update_feature import UpdateFeature
from services import feature
from common import log_manager

logger = log_manager.initLogger()
logger.info('API is starting up')
router = APIRouter(
    prefix="/feature",
    tags=["Feature"],
    responses={503: {"message": "Service unavailable"}}
)


@router.get("/list/all")
async def get_all_feature(db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: get all feature information")
    try:
        return await feature.get_all_feature(db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.get("/{feature_id}")
async def get_feature_by_id(feature_id: int,
                            db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: get feature info by id %s", feature_id)
    try:
        return await feature.get_feature_by_id(feature_id, db_session)
    except Exception as error:
        throw_db_general_error(error)


@router.patch("/{feature_id}")
async def patch_feature_by_id_route(feature_id: int,
                                    patch_body: UpdateFeature,
                                    db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: patch feature info by id %s", feature_id)
    try:
        return await feature.patch_feature_by_id(feature_id, patch_body, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.post("")
async def post_feature(post_body: CreateFeature,
                       db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: post new feature info")
    try:
        return await feature.post_feature(post_body, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)


@router.delete("/{feature_id}")
async def delete_feature(feature_id: int, db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: delete feature info by id %s", feature_id)
    try:
        return await feature.delete_feature(feature_id, db_session)
    except HTTPException as httpError:
        raise httpError
    except Exception as error:
        throw_db_general_error(error)
