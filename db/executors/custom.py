from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
import logging

logger = logging.getLogger(__name__)


async def truncate_table(table_name: str, db_session: AsyncSession):
    try:
        # Construct the raw SQL for truncating the table
        truncate_query = text(f"TRUNCATE TABLE public.{table_name} RESTART IDENTITY CASCADE")

        # Execute the raw SQL
        await db_session.execute(truncate_query)
        await db_session.commit()

        logger.info(f"Table {table_name} truncated successfully.")
        return True
    except Exception as e:
        logger.error(f"An error occurred while truncating the table {table_name}: {e}")
        await db_session.rollback()
        return False
