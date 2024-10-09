from posthog.warehouse.s3 import get_s3_client
from django.conf import settings
from dlt.common.normalizers.naming.snake_case import NamingConvention


def prepare_s3_files_for_querying(folder_path: str, table_name: str, file_uris: list[str]):
    s3 = get_s3_client()

    normalized_table_name = NamingConvention().normalize_identifier(table_name)

    s3_folder_for_job = f"{settings.BUCKET_URL}/{folder_path}"
    s3_folder_for_schema = f"{s3_folder_for_job}/{normalized_table_name}"
    s3_folder_for_querying = f"{s3_folder_for_job}/{normalized_table_name}__query"

    if s3.exists(s3_folder_for_querying):
        s3.delete(s3_folder_for_querying, recursive=True)

    for file in file_uris:
        file_name = file.replace(f"{s3_folder_for_schema}/", "")
        s3.copy(file, f"{s3_folder_for_querying}/{file_name}")