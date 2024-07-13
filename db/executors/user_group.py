from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

from common import log_manager
from sqlalchemy import select, func, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.alembic.tables.feature import Feature
from db.alembic.tables.user_group import UserGroup
from db.executors.custom import truncate_table
from models.request.user_group.create_user_group import CreateUserGroup
from models.request.user_group.update_user_group import UpdateUserGroup
from models.response.table_summary import TableSummary

logger = log_manager.initLogger()


async def summarize(db_session: AsyncSession) -> TableSummary:
    query = select(func.count()).select_from(UserGroup)
    result = await db_session.execute(query)
    count_row = result.scalar_one_or_none()

    return TableSummary(
        name="User Group",
        description="The table contains the group that describe access level of users",
        total_records=count_row if count_row is not None else 0
    )


async def get_full_user_group_by_id(user_group_id: int, db_session: AsyncSession):
    query = select(UserGroup).where(UserGroup.id == user_group_id).options(joinedload(UserGroup.users))
    query_output = await db_session.execute(query)
    result = query_output.scalars().unique().one()
    return result


async def get_brief_user_group_by_id(user_group_id: int, db_session: AsyncSession):
    query = select(UserGroup).where(UserGroup.id == user_group_id)
    query_output = await db_session.execute(query)
    result = query_output.scalars().unique().one()
    return result


async def get_full_detail_user_group(db_session: AsyncSession):
    query = select(UserGroup).options(joinedload(UserGroup.users))
    query_output = await db_session.execute(query)
    result = query_output.scalars().unique().all()
    return result


async def get_brief_detail_user_group(db_session: AsyncSession):
    query = select(UserGroup)
    query_output = await db_session.execute(query)
    result = query_output.scalars().all()
    return result


async def query_allow_feature_by_group_id(user_group_id: int, db_session: AsyncSession):
    query = select(UserGroup).where(UserGroup.id == user_group_id)
    query_output = await db_session.execute(query)
    result = query_output.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User group id not found: {user_group_id}")

    group_level = result.level
    query_feature = select(Feature.id, Feature.name, Feature.level).where(Feature.level <= group_level)
    query_feature_output = await db_session.execute(query_feature)
    allow_features = [{"id": f.id, "name": f.name, "level": f.level} for f in query_feature_output.all()]
    return allow_features


async def update_user_group_by_id(user_group_id: int, update_info: UpdateUserGroup, db_session: AsyncSession):
    try:
        condition = {}
        if update_info.name is not None:
            condition['name'] = update_info.name

        if update_info.level is not None:
            condition['level'] = update_info.level

        query = update(UserGroup).values(condition).where(UserGroup.id == user_group_id)
        result = await db_session.execute(query)
        await db_session.flush()
        await db_session.commit()
        logger.info("update result: %s", result.rowcount)
        return result.rowcount is 1
    except Exception as error:
        logger.error("cannot insert to user group table", error.__traceback__)
        return False


async def insert_user_group(insert_info: CreateUserGroup, db_session: AsyncSession):
    try:
        query = insert(UserGroup).values(id=insert_info.user_group_id, name=insert_info.name, level=insert_info.level)

        result = await db_session.execute(query)
        await db_session.flush()
        await db_session.commit()
        logger.info("insert result: %s", result.rowcount)
        return result.rowcount is 1
    except Exception as error:
        logger.error("cannot insert to user group table", error.__traceback__)
        return False


async def delete_user_group(user_group_id: int, db_session: AsyncSession):
    try:
        query = delete(UserGroup).where(UserGroup.id == user_group_id)
        result = await db_session.execute(query)
        await db_session.flush()
        await db_session.commit()
        logger.info("delete result: %s", result.rowcount)
        return result.rowcount is 1
    except Exception as error:
        logger.error("cannot delete to user group table", error.__traceback__)
        return False


async def batch_insert(user_group_list: list[UserGroup], db_session: AsyncSession) -> bool:
    try:
        db_session.add_all(user_group_list)
        await db_session.commit()
        return True
    except Exception as error:
        logger.error("cannot insert to user group table", error.__traceback__)
        return False


async def truncate(db_session: AsyncSession):
    return await truncate_table("user_group", db_session)
