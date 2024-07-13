from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common import log_manager
from db.executors import feature
from models.request.feature.update_feature import UpdateFeature
from models.request.feature.create_feature import CreateFeature

logger = log_manager.initLogger()


async def get_all_feature(db_session: AsyncSession):
    logger.info(f"Service: get all feature information")
    return await feature.get_all_features(db_session)


async def get_feature_by_id(feature_id: int, db_session: AsyncSession):
    logger.info(f"Service: get feature information by id %s", feature_id)
    return await feature.get_feature_by_id(feature_id, db_session)


async def patch_feature_by_id(feature_id: int, update_feature: UpdateFeature, db_session: AsyncSession):
    logger.info(f"Service: update feature information by id %s", feature_id)
    result = await feature.update_feature_by_id(feature_id, update_feature, db_session)
    if result is True:
        return {"result": "feature information has been changed"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot update feature information please contact admin"
        )


async def post_feature(create_feature: CreateFeature, db_session: AsyncSession):
    logger.info(f"Service: create new feature information")

    result = await feature.insert_feature(create_feature, db_session)
    if result is True:
        return {"result": "feature information has been inserted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot insert feature information please contact admin"
        )


async def delete_feature(feature_id: int, db_session: AsyncSession):
    logger.info(f"Service: delete feature information %s", feature_id)

    result = await feature.delete_feature(feature_id, db_session)
    if result is True:
        return {"result": "feature information has been deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cannot delete feature information please contact admin"
        )
