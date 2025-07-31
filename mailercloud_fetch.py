import requests
import datetime
# import json #greyed out because it's not being used 
import csv
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from environment variable
API_KEY = os.getenv("MAILERCLOUD_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found. Make sure MAILERCLOUD_API_KEY is set in your .env file.")

# Fallback date range (1st to last of current month)
today = datetime.date.today()
first_day = datetime.date(today.year, today.month, 1)
last_day = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1) if today.month < 12 else datetime.date(today.year, 12, 31)

from_date = first_day.strftime("2024-01-01")
to_date = last_day.strftime("2025-05-31")

url = "https://cloudapi.mailercloud.com/v1/campaign/list"

all_data = []

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

payload = {
    "date_from": from_date,
    "date_to": to_date,
    "limit": 100,
    "page": 1,
    "search": "",
    "sender_email": "",
    "sort_field": "name",
    "sort_order": "asc",
    "status": ""
}

try:
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()

        for campaign in result["data"]:
            try:
                row = {
                    "Campaign Name": campaign.get("name", ""),
                    "Domain": campaign.get("sender", {}).get("sender_email", "").split("@")[1].split(".")[0] if "sender_email" in campaign.get("sender", {}) and "@" in campaign["sender"]["sender_email"] else "",
                    "Total Lists": campaign.get("recepiant", {}).get("total_lists", ""),
                    "Lists": campaign.get("recepiant", {}).get("lists", ""),
                    "Contact Count": campaign.get("recepiant", {}).get("lists_contact_count", ""),
                    "Scheduled Date": campaign.get("scheduled_date", {}).get("date", ""),
                    "Sender Email": campaign.get("sender", {}).get("sender_email", ""),
                    "Reply Email": campaign.get("reply_email", ""),
                    "Status": campaign.get("status", ""),
                    "Type": campaign.get("type", ""),
                    "Abuse": campaign.get("report_summary", {}).get("abuse", ""),
                    "Abuse %": campaign.get("report_summary", {}).get("abuse_percentage", ""),
                    "Clicks": campaign.get("report_summary", {}).get("clicks", ""),
                    "Click %": round((campaign.get("report_summary", {}).get("clicks", 0) / campaign.get("report_summary", {}).get("sent", 1)) * 100, 2) if campaign.get("report_summary", {}).get("sent") else 0,
                    "Conversions": campaign.get("report_summary", {}).get("conversions", ""),
                    "Conversions %": campaign.get("report_summary", {}).get("conversions_percentage", ""),
                    "Delivered": campaign.get("report_summary", {}).get("delivered", ""),
                    "Delivered %": campaign.get("report_summary", {}).get("delivered_percentage", ""),
                    "Hard Bounce": campaign.get("report_summary", {}).get("hard_bounce", ""),
                    "Hard Bounce %": round((campaign.get("report_summary", {}).get("hard_bounce", 0) / campaign.get("report_summary", {}).get("sent", 1)) * 100, 2) if campaign.get("report_summary", {}).get("sent") else 0,
                    "Opens": campaign.get("report_summary", {}).get("opens", ""),
                    "Open %": campaign.get("report_summary", {}).get("open_percentage", ""),
                    "Queue": campaign.get("report_summary", {}).get("queue", ""),
                    "Queue %": campaign.get("report_summary", {}).get("queue_percentage", ""),
                    "Queued Total": campaign.get("report_summary", {}).get("queued_total", ""),
                    "Sent": campaign.get("report_summary", {}).get("sent", ""),
                    "Sent %": campaign.get("report_summary", {}).get("sent_percentage", ""),
                    "Soft Bounce": campaign.get("report_summary", {}).get("soft_bounce", ""),
                    "Soft Bounce %": round((campaign.get("report_summary", {}).get("soft_bounce", 0) / campaign.get("report_summary", {}).get("sent", 1)) * 100, 2) if campaign.get("report_summary", {}).get("sent") else 0,
                    "Spam Complaints": campaign.get("report_summary", {}).get("spam_complaints_count", ""),
                    "Spam Complaints %": campaign.get("report_summary", {}).get("spam_complaints_percentage", ""),
                    "Unsubscribes": campaign.get("report_summary", {}).get("unsubscribe", ""),
                    "Unsubscribe %": round((campaign.get("report_summary", {}).get("unsubscribe", 0) / campaign.get("report_summary", {}).get("sent", 1)) * 100, 2) if campaign.get("report_summary", {}).get("sent") else 0,
                    "Campaign ID": campaign.get("id", "")
                }
                all_data.append(row)

            except Exception as row_error:
                print(f"[!] Error parsing campaign data: {row_error}")

    else:
        print(f"[!] API Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"[!] Request Error: {e}")

# --- Write to CSV ---
if all_data:
    with open("mailercloud_campaigns.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_data[0].keys())
        writer.writeheader()
        writer.writerows(all_data)
    print("[✓] Data saved to mailercloud_campaigns.csv")
else:
    print("[!] No campaign data was retrieved. CSV file not written.")