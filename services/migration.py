import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common import log_manager, file_reader
from constants import file_path, file_status
from db.executors import user, migrate_status, user_group, feature

logger = log_manager.initLogger()


async def truncate_all_table(db_session: AsyncSession):
    logger.info(f"Service: truncate all table")
    result = {"user_group": await user_group.truncate(db_session),
              "user": await user.truncate(db_session),
              "feature": await feature.truncate(db_session),
              "migrate_status": await migrate_status.truncate(db_session)}
    return result


async def get_table_overview_service(table: str, db_session: AsyncSession):
    logger.info(f"Service: get overview information of {table}")
    match str.lower(table):
        case "user":
            return await user.summarize(db_session)
        case "user_group":
            return await user_group.summarize(db_session)
        case "feature":
            return await feature.summarize(db_session)
        case "migrate":
            return await migrate_status.summarize(db_session)
        case "all":
            user_info = await user.summarize(db_session)
            user_group_info = await user_group.summarize(db_session)
            feature_info = await feature.summarize(db_session)
            migrate_info = await user.summarize(db_session)

            return [user_info, user_group_info, feature_info, migrate_info]

        case _:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No table found: {table}"
            )


async def put_migrate_all_prepare_file(db_session: AsyncSession):
    logger.info(f"Service: put migrate prepare all file for database")

    migrate_results = [
        await migrate_generic("user_group", file_path.USER_GROUP_PREPARE_FILE, db_session,
                              file_reader.read_prepare_user_group_group, user_group.batch_insert),
        await migrate_generic("user", file_path.USER_PREPARE_FILE, db_session,
                              file_reader.read_prepare_user_record, user.batch_insert),
        await migrate_generic("feature", file_path.FEATURE_PREPARE_FILE, db_session,
                              file_reader.read_prepare_feature, feature.batch_insert)
    ]

    return migrate_results


async def migrate_generic(table_name: str, prepare_file_path: str, db_session: AsyncSession,
                          read_prepare_function,
                          batch_insert_function):
    migrate_status_result = await migrate_status.check_file_is_migrated(prepare_file_path,
                                                                        db_session)
    migrate_status_result.table = table_name
    migrate_status_result.file_path = prepare_file_path
    logger.info("%s_file_migrate_result: %s", table_name, migrate_status_result)

    if migrate_status_result.get_status() is True:
        logger.info("%s has been migrated with file %s", table_name, prepare_file_path)
        return migrate_status_result
    else:
        logger.info("%s hasn't been migrated with file %s", table_name, prepare_file_path)
        logger.info("%s starts migrating with file %s", table_name, prepare_file_path)
        insert_migrate_file_path_result = await migrate_status.insert_prepare_file_path(table_name,
                                                                                        prepare_file_path,
                                                                                        db_session)
        if insert_migrate_file_path_result.get_status() is False:
            logger.info("insert filepath to migrate status is uncompleted")
            migrate_status_result.status = False
            migrate_status_result.description = file_status.FILEPATH_UPLOAD_INCOMPLETE
            return migrate_status_result

        logger.info("insert filepath to migrate status is completed")
        prepare_objects = read_prepare_function(prepare_file_path)
        insert_object_result = await batch_insert_function(prepare_objects, db_session)
        if insert_object_result is True:
            logger.info("insert prepared data to %s is completed", table_name)
            migrate_status_result.status = True
            migrate_status_result.description = file_status.MIGRATION_COMPLETED
            migrate_status_result.create_date = datetime.datetime.now()
            return migrate_status_result
        else:
            logger.info("insert prepared data to %s is uncompleted", table_name)
            migrate_status_result.status = False
            migrate_status_result.description = file_status.MIGRATION_UNCOMPLETED
            return migrate_status_result

# Before refactor
# async def migrate_user_group(user_group_file_path: str, db_session: AsyncSession):
#     user_group_file_migrate_result = await migrate_status.check_file_is_migrated(user_group_file_path,
#                                                                                  db_session)
#     logger.info("user_group_file_migrate_result:", user_group_file_migrate_result)
#     user_group_file_migrate_result.table = "user_group"
#     user_group_file_migrate_result.file_path = user_group_file_path
#
#     if user_group_file_migrate_result.get_status() is True:
#         logger.info("user_group_file_migrate_result is true")
#         return user_group_file_migrate_result
#     else:
#         logger.info("user_group_file_migrate_result is false")
#         insert_file_path_result = await migrate_status.insert_prepare_file_path("user_group",
#                                                                                 user_group_file_path,
#                                                                                 db_session)
#         if insert_file_path_result.get_status() is True:
#             logger.info("insert filepath to migrate status is true")
#             user_group_list = file_reader.read_prepare_user_group_group(user_group_file_path)
#             insert_user_group_object_result = await user_group.batch_insert(user_group_list, db_session)
#             if insert_user_group_object_result is True:
#                 user_group_file_migrate_result.status = True
#                 user_group_file_migrate_result.description = file_status.FILE_INSERT_COMPLETE
#                 user_group_file_migrate_result.create_date = insert_file_path_result.create_date
#                 return user_group_file_migrate_result
#             else:
#                 user_group_file_migrate_result.status = False
#                 user_group_file_migrate_result.description = file_status.FILE_INSERT_INCOMPLETE
#                 return user_group_file_migrate_result
#         else:
#             logger.info("insert filepath to migrate status is false")
#             user_group_file_migrate_result.status = False
#             user_group_file_migrate_result.description = file_status.FILEPATH_UPLOAD_INCOMPLETE
#             return user_group_file_migrate_result
#
#
# async def migrate_user(user_file_path: str, db_session: AsyncSession):
#     user_file_migrate_result = await migrate_status.check_file_is_migrated(user_file_path,
#                                                                            db_session)
#     user_file_migrate_result.table = "user"
#     user_file_migrate_result.file_path = user_file_path
#
#     if user_file_migrate_result.get_status() is True:
#         return user_file_migrate_result
#     else:
#         insert_file_path_result = await migrate_status.insert_prepare_file_path("user",
#                                                                                 user_file_path,
#                                                                                 db_session)
#         if insert_file_path_result.get_status() is True:
#             user_list = file_reader.read_prepare_user_record(user_file_path)
#             insert_user_object_result = await user.batch_insert(user_list, db_session)
#             if insert_user_object_result is True:
#                 user_file_migrate_result.status = True
#                 user_file_migrate_result.description = file_status.FILE_INSERT_COMPLETE
#                 user_file_migrate_result.create_date = insert_file_path_result.create_date
#                 return user_file_migrate_result
#             else:
#                 user_file_migrate_result.status = False
#                 user_file_migrate_result.description = file_status.FILE_INSERT_INCOMPLETE
#                 return user_file_migrate_result
#         else:
#             user_file_migrate_result.status = False
#             user_file_migrate_result.description = file_status.FILEPATH_UPLOAD_INCOMPLETE
#             return user_file_migrate_result
#
#
# async def migrate_feature(feature_file_path: str, db_session: AsyncSession):
#     feature_file_migrate_result = await migrate_status.check_file_is_migrated(feature_file_path,
#                                                                               db_session)
#     feature_file_migrate_result.table = "feature"
#     feature_file_migrate_result.file_path = feature_file_path
#
#     if feature_file_migrate_result.get_status() is True:
#         return feature_file_migrate_result
#     else:
#         insert_file_path_result = await migrate_status.insert_prepare_file_path("user",
#                                                                                 feature_file_path,
#                                                                                 db_session)
#         if insert_file_path_result.get_status() is True:
#             feature_list = file_reader.read_prepare_feature(feature_file_path)
#             insert_feature_object_result = await feature.batch_insert(feature_list, db_session)
#             if insert_feature_object_result is True:
#                 feature_file_migrate_result.status = True
#                 feature_file_migrate_result.description = file_status.FILE_INSERT_COMPLETE
#                 feature_file_migrate_result.create_date = insert_file_path_result.create_date
#                 return feature_file_migrate_result
#             else:
#                 feature_file_migrate_result.status = False
#                 feature_file_migrate_result.description = file_status.FILE_INSERT_INCOMPLETE
#                 return feature_file_migrate_result
#         else:
#             feature_file_migrate_result.status = False
#             feature_file_migrate_result.description = file_status.FILEPATH_UPLOAD_INCOMPLETE
#             return feature_file_migrate_result
