from datetime import datetime

import pandas as pd

from constants.date_format import DATE_OF_BIRTH_FORMAT
from constants.file_path import USER_GROUP_PREPARE_FILE
from db.alembic.tables.user import User
from db.alembic.tables.user_group import UserGroup
from db.alembic.tables.feature import Feature


def read_prepare_user_record(file_path) -> list[User]:
    user_csv = pd.read_csv(file_path)
    users: list[User] = []
    for index, row in user_csv.iterrows():
        converted_date_of_birth = datetime.strptime(str(row.date_of_birth), DATE_OF_BIRTH_FORMAT)
        users.append(
            User(
                first_name=row.first_name, last_name=row.last_name,
                tel_no=str(row.tel_no), date_of_birth=converted_date_of_birth,
                district=row.district, city=row.city,
                province=row.province, zip_code=str(row.zip_code),
                access_group_id=row.access_group_id
            )
        )
    return users


def read_prepare_user_group_group(file_path: str):
    user_group_csv = pd.read_csv(file_path)
    user_groups: list[UserGroup] = []
    for index, row in user_group_csv.iterrows():
        user_groups.append(UserGroup(id=row['id'], name=row['name'], level=row['level']))
    return user_groups


def read_prepare_feature(file_path: str):
    feature_csv = pd.read_csv(file_path)
    features: list[Feature] = []
    for index, row in feature_csv.iterrows():
        features.append(Feature(name=str(row['name']), level=row.level))
    return features


def main():
    read_prepare_user_group_group("../" + USER_GROUP_PREPARE_FILE)


if __name__ == "__main__":
    main()
