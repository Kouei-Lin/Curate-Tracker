from decouple import config
import requests
import csv

# Fetch configuration values from the .env file
XDAI_GTCR_SUBGRAPH_URL = config("XDAI_GTCR_SUBGRAPH_URL")
XDAI_REGISTRY_ADDRESS_TAGS = config("XDAI_REGISTRY_ADDRESS_TAGS")
XDAI_REGISTRY_TOKENS = config("XDAI_REGISTRY_TOKENS")
XDAI_REGISTRY_DOMAINS = config("XDAI_REGISTRY_DOMAINS")

def fetch_tags_batch_by_registry(period, subgraph_endpoint, registry):
    start = int(period["start"].timestamp())
    end = int(period["end"].timestamp())

    subgraph_query = {
        "query": """
            {
                litems(where: {
                    registryAddress: "%s",
                    status_in: [Registered, ClearingRequested],
                    latestRequestResolutionTime_gte: %s,
                    latestRequestResolutionTime_lt: %s
                }, first: 1000) {
                    id
                    props {
                        value
                    }
                    latestRequestResolutionTime
                    requests {
                        requester
                        requestType
                        resolutionTime
                    }
                    key0
                    key1
                    key2
                    key3
                }
            }
        """ % (registry, start, end)
    }

    response = requests.post(subgraph_endpoint, json=subgraph_query)

    if response.status_code == 200:
        data = response.json()
        tags = data.get("data", {}).get("litems", [])
        return tags
    else:
        print(f"Failed to fetch data from {subgraph_endpoint}")
        return []

def parse_caip(caip):
    try:
        _, chain, address = caip.split(":")
        return {"chain": int(chain), "address": address}
    except ValueError:
        # Handle the case where the value cannot be converted to an integer
        return {"chain": None, "address": caip}

def item_to_tag(item, registry_type):
    caip_info = parse_caip(item.get("key0", ""))
    tag = {
        "id": item.get("id", ""),
        "registry": registry_type,
        "chain": caip_info["chain"],
        "latestRequestResolutionTime": int(item.get("latestRequestResolutionTime", 0)),
        "submitter": item.get("requests[0].requester", ""),
        "tagAddress": caip_info["address"],
    }
    return tag

def fetch_tags(period):
    address_tags_items = fetch_tags_batch_by_registry(
        period, XDAI_GTCR_SUBGRAPH_URL, XDAI_REGISTRY_ADDRESS_TAGS
    )
    address_tags = [item_to_tag(item, "addressTags") for item in address_tags_items]

    tokens_items = fetch_tags_batch_by_registry(
        period, XDAI_GTCR_SUBGRAPH_URL, XDAI_REGISTRY_TOKENS
    )
    tokens = [item_to_tag(item, "tokens") for item in tokens_items]

    domains_items = fetch_tags_batch_by_registry(
        period, XDAI_GTCR_SUBGRAPH_URL, XDAI_REGISTRY_DOMAINS
    )
    domains = [item_to_tag(item, "domains") for item in domains_items]

    # Combine all the tags
    all_tags = address_tags + tokens + domains

    return all_tags

# Example usage
if __name__ == "__main__":
    from datetime import datetime

    # Define the period for fetching data
    start_date = datetime(2023, 10, 1)
    end_date = datetime(2023, 10, 22)
    period = {"start": start_date, "end": end_date}

    # Fetch and print the tags
    tags = fetch_tags(period)


# Define the path where you want to save the CSV file
csv_file_path = "fetch_registry.csv"

# Store the results in a CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = tags[0].keys() if tags else []
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for tag in tags:
        writer.writerow(tag)

print(f"Tags have been saved to {csv_file_path}")
