import os
import zipfile
import subprocess
from Credit_Card_Fraud_Detection import logger
from Credit_Card_Fraud_Detection.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not self.config.local_data_file.exists():
            try:
                # Use gdown with --fuzzy for flexible link handling
                subprocess.run([
                    "gdown",
                    "--fuzzy",
                    self.config.source_URL,
                    "-O",
                    str(self.config.local_data_file)
                ], check=True)
                logger.info(f"Downloaded file to {self.config.local_data_file}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to download file: {e}")
        else:
            logger.info(f"File already exists at {self.config.local_data_file}, size: {get_size(self.config.local_data_file)}")



    def extract_zip_file(self):
        os.makedirs(self.config.unzip_dir, exist_ok=True)
        try:
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(self.config.unzip_dir)
            logger.info(f"Extracted ZIP file to {self.config.unzip_dir}")
        except zipfile.BadZipFile:
            logger.error("The downloaded file is not a valid ZIP file.")
        except FileNotFoundError:
            logger.error("ZIP file not found.")
  