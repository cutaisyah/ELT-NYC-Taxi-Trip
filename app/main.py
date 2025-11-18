from app.extract_load import extract_load_main
import logging
logging.basicConfig(level=logging.INFO)

def main():
    try:
        logging.info("=== Starting NYC Taxi Data Extraction and Load... ===")
        extract_load_main()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        logging.info("=== Finished ===")
        
if __name__ == "__main__":
    main()
