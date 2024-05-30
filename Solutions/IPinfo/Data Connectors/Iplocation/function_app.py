import logging
import time
import maxminddb
import azure.functions as func
from azure.identity import ClientSecretCredential
from azure.monitor.ingestion import LogsIngestionClient
from lib.constants import *
from lib.utils import download_mmdbs
from lib.utils import check_and_create_data_collection_endpoint
from lib.utils import check_and_create_table
from lib.utils import check_and_create_data_collection_rules
from lib.utils import get_table

app = func.FunctionApp()

@app.schedule(schedule=CRON, arg_name="myTimer", run_on_startup=True, use_monitor=False)
def ipinfo_iplocation_function(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Ipinfo Iplocation timer trigger function executed.")

    def upload_data_to_location_table(dce_endpoint, dcr_immutableid, stream_name):
        credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
        client = LogsIngestionClient(endpoint=dce_endpoint, credential=credential, logging_enable=True)
        mmdb_file_path = "/tmp/standard_location.mmdb"
        reader = maxminddb.open_database(mmdb_file_path)
        chunk_size = 10000
        data_chunk = []
        logging.info("Uploading Standard Location Data.\n")
        for ip, ip_data in reader:
            result = {}
            result["city"] = ip_data.get("city", "")
            result["country"] = ip_data.get("country", "")
            result["geoname_id"] = ip_data.get("geoname_id", "")
            result["lat"] = ip_data.get("lat", "")
            result["lng"] = ip_data.get("lng", "")
            result["postal_code"] = ip_data.get("postal_code", "")
            result["region"] = ip_data.get("region", "")
            result["region_code"] = ip_data.get("region_code", "")
            result["range"] = str(ip)
            data_chunk.append(result)
            if len(data_chunk) >= chunk_size:
                try:
                    client.upload(rule_id=dcr_immutableid, stream_name=stream_name, logs=data_chunk)
                except Exception as e:
                    logging.error(f"Upload failed: {e}")
                data_chunk = []
        if data_chunk:
            try:
                client.upload(rule_id=dcr_immutableid, stream_name=stream_name, logs=data_chunk)
            except Exception as e:
                logging.error(f"Upload failed: {e}")
        reader.close()
        logging.info("Standard Location Data uploading completed.")

    # Function flow starts here; above this line are function definitions
    credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    access_token = credential.get_token(AZURE_SCOPE).token
    if access_token:
        logging.info("\nAccess Token Retrieved\n")
        logging.info(access_token)
    else:
        logging.error("\nFailed to retrieve access token\n")

    download_mmdbs()
    dce_endpoint = check_and_create_data_collection_endpoint(DATA_COLLECTION_ENDPOINT_NAME, access_token)
    check_and_create_table(LOCATION_TABLE_NAME, LOCATION_TABLE_SCHEMA, access_token)
    retries = 3
    while retries > 0:
        if get_table(LOCATION_TABLE_NAME, access_token):
            location_dcr_immutableid, location_stream_name = check_and_create_data_collection_rules(
                access_token,
                LOCATION_DCR_NAME,
                LOCATION_STREAM_DECLARATION,
                LOCATION_TABLE_COLUMNS,
                DATA_COLLECTION_ENDPOINT_NAME,
            )
            upload_data_to_location_table(dce_endpoint, location_dcr_immutableid, location_stream_name)
            break
        else:
            logging.info("Table not created yet, retrying in 1 minute...")
            time.sleep(60)
            retries -= 1
    if retries == 0:
        logging.error("Table creation timed out after 3 retries. Data collection rules were not created.")
