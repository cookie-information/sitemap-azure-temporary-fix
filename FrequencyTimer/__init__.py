import datetime
import logging

import azure.functions as func

# TODO
# 1. Scrape all links from page within XML
# 2. Convert links to proper HTML <a> tags
# 4. Run script 1x per month (cronjob)
# 5. Output a tags to page
# 6. Host site on Azure storage blob
# 7. Set up CI/CD to push changes to storage blob and updated based on crawler frequency

# Imports
import requests
from bs4 import BeautifulSoup

import os

from azure.storage.blob import BlobClient, ContentSettings


def write_to_blob_storage(loc):

    content_type = ContentSettings(content_type="text/html")

    conn_string = os.environ["AzureWebJobsStorage"]

    blob_client = BlobClient.from_connection_string(conn_string,
                                                    container_name="output-files", blob_name="linkoutput.html")

    blob_client.upload_blob(loc, overwrite=True, content_settings=content_type)


def get_all_loc():
    loc_list = []
    url = "https://example-site.com/sitemap" # Change this to the URL of your sitemap
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    loc_tags = soup.select('loc')
    for loc in loc_tags:
        loc_list.append(f"<a href={loc.text}>{loc.text}</a><br>")

    return loc_list


def main(mytimer: func.TimerRequest) -> None:
    logging.info("Starting timer trigger")
    loc = get_all_loc()
    loc.insert(0, "<html>") 
    loc.append("</html>")
    joined_output = "\n".join(loc).encode("UTF-8")
    write_to_blob_storage(joined_output)

    logging.info("Ending timer trigger")
