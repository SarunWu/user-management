from common import log_manager
from sqlalchemy import select, func, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.alembic.tables.feature import Feature
from db.executors.custom import truncate_table
from models.request.feature.create_feature import CreateFeature
from models.request.feature.update_feature import UpdateFeature
from models.response.table_summary import TableSummary

logger = log_manager.initLogger()


async def summarize(db_session: AsyncSession) -> TableSummary:
    query = select(func.count()).select_from(Feature)
    result = await db_session.execute(query)
    count_row = result.scalar_one_or_none()

    return TableSummary(
        name="Feature",
        description="The table contains functionality and modality and required level",
        total_records=count_row if count_row is not None else 0
    )


async def get_feature_by_id(feature_id: int, db_session: AsyncSession):
    query = select(Feature).where(Feature.id == feature_id)
    query_output = await db_session.execute(query)
    result = query_output.scalars().unique().one()
    return result


async def get_all_features(db_session: AsyncSession):
    query = select(Feature)
    query_output = await db_session.execute(query)
    result = query_output.scalars().unique().all()
    return result


def map_update_values(update_info: UpdateFeature):
    update_values = {}
    if update_info.name is not None:
        update_values['name'] = update_info.name

    if update_info.level is not None:
        update_values['level'] = update_info.level

    return update_values


async def update_feature_by_id(feature_id: int, update_info: UpdateFeature, db_session: AsyncSession):
    try:
        query = update(Feature).values(map_update_values(update_info)).where(Feature.id == feature_id)
        result = await db_session.execute(query)
        await db_session.flush()
        await db_session.commit()
        logger.info("update result: %s", result.rowcount)
        return result.rowcount is 1
    except Exception as error:
        logger.error("cannot insert to feature table", error.__traceback__)
        return False


async def insert_feature(insert_info: CreateFeature, db_session: AsyncSession):
    try:
        query = insert(Feature).values(name=insert_info.name,
                                       level=insert_info.level)

        result = await db_session.execute(query)
        await db_session.flush()
        await db_session.commit()
        logger.info("insert result: %s", result.rowcount)
        return result.rowcount is 1
    except Exception as error:
        logger.error("cannot insert to feature table", error.__traceback__)
        return False


async def delete_feature(feature_id: int, db_session: AsyncSession):
    try:
        query = delete(Feature).where(Feature.id == feature_id)
        result = await db_session.execute(query)
        await db_session.flush()
        await db_session.commit()
        logger.info("delete result: %s", result.rowcount)
        return result.rowcount is 1
    except Exception as error:
        logger.error("cannot delete to feature table", error.__traceback__)
        return False


async def batch_insert(feature_list: list[Feature], db_session: AsyncSession) -> bool:
    try:
        db_session.add_all(feature_list)
        await db_session.flush()
        await db_session.commit()
        return True
    except Exception as error:
        logger.error("cannot insert to feature table", error.__traceback__)
        return False


async def truncate(db_session: AsyncSession):
    return await truncate_table("feature", db_session)
