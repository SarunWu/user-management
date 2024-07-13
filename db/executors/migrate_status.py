import sys
import os

from db.executors.custom import truncate_table

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from common import log_manager
from constants import file_status
from models.response.file_migrate_result import FileMigrateResult
from sqlalchemy import select, func, insert
from sqlalchemy.ext.asyncio import AsyncSession
from db.alembic.tables.migrate_status import MigrateStatus
from models.response.table_summary import TableSummary

logger = log_manager.initLogger()


async def summarize(db_session: AsyncSession) -> TableSummary:
    query = select(func.count()).select_from(MigrateStatus)
    result = await db_session.execute(query)
    count_row = result.scalar_one_or_none()

    return TableSummary(
        name="Migrate Status",
        description="The table contains the information of the file that is used to insert as migrated data",
        total_records=count_row if count_row is not None else 0
    )


async def check_file_is_migrated(file_path: str, db_session: AsyncSession) -> FileMigrateResult:
    query = select(MigrateStatus.create_date).where(MigrateStatus.source_file_name == file_path)
    query_output = await db_session.execute(query)

    result = query_output.scalar_one_or_none()
    if result is None:
        return FileMigrateResult(status=False, description=file_status.FILE_NOT_EXIST)
    else:
        return FileMigrateResult(status=True, description=file_status.FILE_MIGRATED, create_date=result)


async def insert_prepare_file_path(target_table: str, file_path: str, db_session: AsyncSession) -> FileMigrateResult:
    logger.info(f"Start inserting filepath to {target_table} with {file_path}")

    try:
        query = insert(MigrateStatus).values(source_file_name=file_path, target_table=target_table).returning(
            MigrateStatus)
        query_output = await db_session.execute(query)
        insert_result = query_output.scalar_one_or_none()

        return FileMigrateResult(status=True,
                                 description=file_status.FILEPATH_UPLOAD_COMPLETE,
                                 create_date=insert_result.create_date)

    except Exception as error:
        logger.error("Fail to insert filepath", error.__traceback__)
        return FileMigrateResult(status=False, description=file_status.FILEPATH_UPLOAD_INCOMPLETE)


async def truncate(db_session: AsyncSession):
    return await truncate_table("migrate_status", db_session)
