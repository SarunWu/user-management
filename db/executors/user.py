from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload

from common import log_manager

from sqlalchemy import select, func, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.alembic.tables.feature import Feature
from db.alembic.tables.user import User
from models.request.user.create_user import CreateUser
from models.request.user.update_user import UpdateUser
from models.response.table_summary import TableSummary
from db.executors.custom import truncate_table

logger = log_manager.initLogger()


async def summarize(db_session: AsyncSession) -> TableSummary:
    query = select(func.count()).select_from(User)
    result = await db_session.execute(query)
    count_row = result.scalar_one_or_none()

    return TableSummary(
        name="User",
        total_records=count_row if count_row is not None else 0,
        description="The table contains basic information of user",
    )


async def get_user_by_id(user_id: int, db_session: AsyncSession):
    query = select(User).where(User.id == user_id).options(joinedload(User.access_group))
    query_output = await db_session.execute(query)
    result = query_output.scalars().unique().one()
    return result


async def get_all_users(db_session: AsyncSession):
    query = select(User).options(joinedload(User.access_group))
    query_output = await db_session.execute(query)
    result = query_output.scalars().unique().all()
    return result


async def query_allow_feature_by_user_id(user_id: int, db_session: AsyncSession):
    query = select(User).where(User.id == user_id).options(joinedload(User.access_group))
    query_output = await db_session.execute(query)
    result = query_output.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User id not found: {user_id}")

    group_level = result.access_group.level
    query_feature = select(Feature.id, Feature.name, Feature.level).where(Feature.level <= group_level)
    query_feature_output = await db_session.execute(query_feature)
    allow_features = [{"id": f.id, "name": f.name, "level": f.level} for f in query_feature_output.all()]
    return allow_features


def map_update_values(update_info: UpdateUser):
    update_values = {}
    if update_info.first_name is not None:
        update_values['first_name'] = update_info.first_name

    if update_info.last_name is not None:
        update_values['last_name'] = update_info.last_name

    if update_info.tel_no is not None:
        update_values['tel_no'] = update_info.tel_no

    if update_info.date_of_birth is not None:
        update_values['date_of_birth'] = update_info.date_of_birth

    if update_info.district is not None:
        update_values['district'] = update_info.district

    if update_info.city is not None:
        update_values['city'] = update_info.city

    if update_info.province is not None:
        update_values['province'] = update_info.province

    if update_info.zip_code is not None:
        update_values['zip_code'] = update_info.zip_code

    if update_info.access_group_id is not None:
        update_values['access_group_id'] = update_info.access_group_id

    return update_values


async def update_user_by_id(user_id: int, update_info: UpdateUser, db_session: AsyncSession):
    try:
        query = update(User).values(map_update_values(update_info)).where(User.id == user_id)
        result = await db_session.execute(query)
        await db_session.flush()
        await db_session.commit()
        logger.info("update result: %s", result.rowcount)
        return result.rowcount is 1
    except Exception as error:
        logger.error("cannot insert to user table", error.__traceback__)
        return False


async def insert_user(insert_info: CreateUser, db_session: AsyncSession):
    try:
        query = insert(User).values(first_name=insert_info.first_name,
                                    last_name=insert_info.last_name,
                                    tel_no=insert_info.tel_no,
                                    date_of_birth=insert_info.date_of_birth,
                                    district=insert_info.district,
                                    city=insert_info.city,
                                    province=insert_info.province,
                                    zip_code=insert_info.zip_code,
                                    access_group_id=insert_info.access_group_id)

        result = await db_session.execute(query)
        await db_session.flush()
        await db_session.commit()
        logger.info("insert result: %s", result.rowcount)
        return result.rowcount is 1
    except Exception as error:
        logger.error("cannot insert to user table", error.__traceback__)
        return False


async def delete_user(user_id: int, db_session: AsyncSession):
    try:
        query = delete(User).where(User.id == user_id)
        result = await db_session.execute(query)
        await db_session.flush()
        await db_session.commit()
        logger.info("delete result: %s", result.rowcount)
        return result.rowcount is 1
    except Exception as error:
        logger.error("cannot delete to user table", error.__traceback__)
        return False


async def batch_insert(user_list: list[User], db_session: AsyncSession) -> bool:
    try:
        db_session.add_all(user_list)
        await db_session.commit()
        return True
    except Exception as error:
        logger.error("cannot insert to user table", error.__traceback__)
        return False


async def truncate(db_session: AsyncSession):
    return await truncate_table("user", db_session)
