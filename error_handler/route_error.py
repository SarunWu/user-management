from fastapi import HTTPException, status

from common import log_manager
from constants.error_message import DB_GENERAL_ERROR

logger = log_manager.initLogger()


def throw_db_general_error(error: Exception):
    logger.error(DB_GENERAL_ERROR, error.__traceback__)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=DB_GENERAL_ERROR
    )
