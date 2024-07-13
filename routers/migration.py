from fastapi import APIRouter, Depends
from db.database_engine import get_async_session

from sqlalchemy.ext.asyncio import AsyncSession

from error_handler.route_error import throw_db_general_error
from services.migration import get_table_overview_service, put_migrate_all_prepare_file, truncate_all_table
from common import log_manager

logger = log_manager.initLogger()
logger.info('API is starting up')
router = APIRouter(
    prefix="/migrate",
    tags=["Migration"],
    responses={503: {"message": "Service unavailable"}}
)


@router.delete("/truncate/all")
async def delete_by_truncate_all(db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: truncate all table")
    try:
        return await truncate_all_table(db_session)
    except Exception as error:
        throw_db_general_error(error)


@router.get("/tables/overview/{table}")
async def get_table_overview(table: str, db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: get overview information of {table}")
    try:
        return await get_table_overview_service(table, db_session)
    except Exception as error:
        throw_db_general_error(error)


@router.put("/prepare-file/all")
async def put_prepare_table(db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"Route: PUT migrate prepare file")
    try:
        return await put_migrate_all_prepare_file(db_session)
    except Exception as error:
        throw_db_general_error(error)
