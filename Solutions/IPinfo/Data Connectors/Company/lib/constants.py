import os

# Enviornment Virables
RESOURCE_ID = os.environ["RESOURCE_ID"]
IPINFO_TOKEN = os.environ["IPINFO_TOKEN"]
TENANT_ID = os.environ["TENANT_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
SCHEDULE = os.environ["SCHEDULE"]
LOCATION = os.environ["LOCATION"]

parts = RESOURCE_ID.split("/")
SUBCRIPTION_ID = parts[2]
RESOURCE_GROUP_NAME = parts[4]
WORKSPACE_NAME = parts[8]

if SCHEDULE == "daily":
    CRON = "0 1 1 * * *"
    RETENTION_IN_DAYS = 4
    TOTAL_RETENTION_IN_DAYS = 4
elif SCHEDULE == "weekly":
    CRON = "0 1 1 * * 1"
    RETENTION_IN_DAYS = 14
    TOTAL_RETENTION_IN_DAYS = 21
else:
    CRON = "0 1 1 1 * *"
    RETENTION_IN_DAYS = 60
    TOTAL_RETENTION_IN_DAYS = 90

DATA_COLLECTION_ENDPOINT_NAME = "ipinfo-logs-ingestion"
COMPANY_DCR_NAME = "ipinfo_rule_for_company_table"
COMPANY_TABLE_NAME = "Ipinfo_Company_CL"
COMPANY_STREAM_DECLARATION = "Custom-Ipinfo_Company_CL"

AZURE_SCOPE = "https://management.azure.com/.default"
AZURE_BASE_URL = f"https://management.azure.com/subscriptions/{SUBCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP_NAME}/providers/Microsoft."
IPINFO_BASE_URL = "https://ipinfo.io/data"
MMDB_NAME = "standard_company.mmdb"

COMPANY_TABLE_SCHEMA = {
    "properties": {
        "totalRetentionInDays": TOTAL_RETENTION_IN_DAYS,
        "archiveRetentionInDays": 0,
        "plan": "Analytics",
        "retentionInDaysAsDefault": True,
        "totalRetentionInDaysAsDefault": True,
        "schema": {
            "tableSubType": "DataCollectionRuleBased",
            "name": COMPANY_TABLE_NAME,
            "tableType": "CustomLog",
            "description": "Range based table",
            "columns": [
                {"name": "as_domain", "type": "string", "isDefaultDisplay": False, "isHidden": False},
                {"name": "as_name", "type": "string", "isDefaultDisplay": False, "isHidden": False},
                {"name": "as_type", "type": "string", "isDefaultDisplay": False, "isHidden": False},
                {"name": "asn", "type": "string", "isDefaultDisplay": False, "isHidden": False},
                {"name": "country", "type": "string", "isDefaultDisplay": False, "isHidden": False},
                {"name": "company_domain", "type": "string", "isDefaultDisplay": False, "isHidden": False},
                {"name": "company_name", "type": "string", "isDefaultDisplay": False, "isHidden": False},
                {"name": "company_type", "type": "string", "isDefaultDisplay": False, "isHidden": False},
                {"name": "ip_range", "type": "string", "isDefaultDisplay": False, "isHidden": False},
                {"name": "TimeGenerated", "type": "datetime", "isDefaultDisplay": False, "isHidden": False},
            ],
            "standardColumns": [{"name": "TenantId", "type": "guid", "isDefaultDisplay": False, "isHidden": False}],
            "solutions": ["LogManagement"],
            "isTroubleshootingAllowed": True,
        },
        "provisioningState": "Succeeded",
        "retentionInDays": RETENTION_IN_DAYS,
    },
    "id": f"/subscriptions/{SUBCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP_NAME}/providers/Microsoft.OperationalInsights/workspaces/{WORKSPACE_NAME}/tables/{COMPANY_TABLE_NAME}",
    "name": COMPANY_TABLE_NAME,
}

COMPANY_TABLE_COLUMNS = {
    "columns": [
        {"name": "TimeGenerated", "type": "datetime"},
        {"name": "as_domain", "type": "string"},
        {"name": "as_name", "type": "string"},
        {"name": "as_type", "type": "string"},
        {"name": "asn", "type": "string"},
        {"name": "country", "type": "string"},
        {"name": "company_domain", "type": "string"},
        {"name": "company_name", "type": "string"},
        {"name": "company_type", "type": "string"},
        {"name": "range", "type": "string"},
    ]
}
