import os
import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.oauth2 import service_account

websites = [
    {
        "division": "Door Division",
        "domain": "www.samuraidoors.com",
        "property_id": "450920964",
        "creds": "creds/samuraidoors.json"
    },
    {
        "division": "Oil and Gas Division",
        "domain": "www.citycatoilpartssupply.com",
        "property_id": "422321881",
        "creds": "creds/citycat.json"
    },
    {
        "division": "Oil and Gas Division",
        "domain": "www.oilandgasindustrialequipmentsupply.com",
        "property_id": "451760390",
        "creds": "creds/citycat.json"
    },
    {
        "division": "Oil and Gas Division",
        "domain": "www.oilpipepigging.com",
        "property_id": "422204071",
        "creds": "creds/citycat.json"
    },
    {
        "division": "Oil and Gas Division",
        "domain": "www.piggingspacerguidesealdisc.com",
        "property_id": "428851202",
        "creds": "creds/citycat.json"
    },
    {
        "division": "Lab Division",
        "domain": "www.citycatlabequipments.com",
        "property_id": "451729204",
        "creds": "creds/citycat.json"
    },
    {
        "division": "Gypsum Division",
        "domain": "www.whitepanthergypsum.com",
        "property_id": "451750702",
        "creds": "creds/citycat.json"
    },
    {
        "division": "Furniture Division",
        "domain": "www.spaceinteriormanagementandsolution.com",
        "property_id": "422450982",
        "creds": "creds/citycat.json"
    },
    {
        "division": "Electrical Division",
        "domain": "www.spaceageelectrical.com",
        "property_id": "471770099",
        "creds": "creds/citycat.json"
    }
]

def fetch_countries(property_id, creds_relative_path):
  
    script_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(script_dir, creds_relative_path)

    credentials = service_account.Credentials.from_service_account_file(creds_path)
    client = BetaAnalyticsDataClient(credentials=credentials)

    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=yesterday, end_date=yesterday)],
    )

    response = client.run_report(request)
    countries = [row.dimension_values[0].value for row in response.rows] if response.rows else []
    return countries

divisions_output = {}

for site in websites:
    countries = fetch_countries(site["property_id"], site["creds"])
    if site["division"] not in divisions_output:
        divisions_output[site["division"]] = []

    if countries:
        divisions_output[site["division"]].append(f"1. {site['domain']} – {', '.join(countries)}")
    else:
        divisions_output[site["division"]].append(f"1. {site['domain']} – No Visit")

# ✅ Print the final grouped output
for division, lines in divisions_output.items():
    print(f"{division}\nWebsites visit:")
    for line in lines:
        print(line)
    print("")
