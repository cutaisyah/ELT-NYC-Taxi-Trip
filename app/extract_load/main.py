from .extract_nyc_taxi_trip import ExtractLoadNYCTaxiTrip

def main():
    extractor_yellow = ExtractLoadNYCTaxiTrip(taxi_type='yellow')
    extractor_yellow.extract_load_data()
    extractor_green = ExtractLoadNYCTaxiTrip(taxi_type='green')
    extractor_green.extract_load_data()