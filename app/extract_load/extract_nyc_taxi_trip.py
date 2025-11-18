import os
import re
import logging
from dotenv import load_dotenv
from datetime import datetime
from ..utils import HttpClient
from .web_scrapper import WebScrapper
from .processing_file import ProcessFile

load_dotenv()
logging.basicConfig(level=logging.INFO)

class ExtractLoadNYCTaxiTrip:

    def __init__(self, taxi_type: str):
        self.http_client = HttpClient()
        self.taxi_type = taxi_type

    def __fetch_nyc_urls(self):
        response = self.http_client.get(os.getenv("NYC_TAXI_DATA_URL", ""))
        if response.status_code != 200 or not response.text:
            raise ConnectionError("Failed to fetch NYC Taxi Data page.")
        
        scrapper = WebScrapper(response.text)
        # Filter for all months in 2025
        urls = scrapper.find_urls(self.taxi_type, '2025') 
        if not urls:
            raise ValueError(f"No URLs found for taxi type '{self.taxi_type}' in 2025.")
        return urls

    def __parse_url_date(self, url: str) -> datetime:
        match = re.search(r"(\d{4}-\d{2})\.parquet$", url)
        if not match:
            raise ValueError(f"Cannot extract date from URL: {url}")
        date_str = match.group(1) + "-01"
        return datetime.strptime(date_str, "%Y-%m-%d")

    def __log_extraction(self, idx: int, url: str):
        date_obj = self.__parse_url_date(url)
        formatted_date = date_obj.strftime('%d %b %Y')
        logging.info(f"{idx+1}: Extracted data for {formatted_date}")

    def __extract_data(self):
        urls = self.__fetch_nyc_urls()
        # urls = urls[:1] # limit to first month in case it takes forever to run it in shell. You can remove this line to extract all available months.
        processor = ProcessFile(urls)
        df = processor.read_parquet()

        pickup_col = "tpep_pickup_datetime" if self.taxi_type == "yellow" else "lpep_pickup_datetime"
        df_filtered = processor.filter_first_day_each_month(df, pickup_col)

        for idx, url in enumerate(urls):
            self.__log_extraction(idx, url)

        return df_filtered

    def extract_load_data(self):
        try:
            df = self.__extract_data()
            logging.info(f"Data extraction and processing for '{self.taxi_type}' taxi completed successfully.")
        except (ConnectionError, ValueError) as e:
            raise RuntimeError(f"Data extraction failed: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error during extraction: {e}") from e
