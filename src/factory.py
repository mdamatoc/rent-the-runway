from src.core.logger import Logger
from abc import ABC
from omegaconf import dictconfig
from datetime import datetime, timedelta
from src.s3 import S3
import pandas as pd
from pandas.core import frame
from src.core.data_analysis import DataAnalysis


log = Logger(__name__).instance


class Dataset(ABC):
    def __init__(self, cfg: dictconfig):
        self.cfg = cfg

    def exploratory_data_analysis(self, file: str):
        data_frame = self.__read_file(file)

        log.info("Starting Data Analysis")
        data_analysis = DataAnalysis(data_frame)
        # print(data_frame)

        """
        1. Produza um grafico da distribuicao de peso (histograma) dos clientes (em Kg)
        """
        data_analysis.make_a_histogram_in_kgs(weight_column='weight')


    def get_files(self) -> list:
        log.info("Searching usable files")
        files = self.__list_files()
        downloaded_files = []
        for file in files:
            downloaded_files = []
            downloaded_file = self.__download_file(key=file)
            downloaded_files.append(downloaded_file)

        return downloaded_files

    def __list_files(self) -> list:
        # files = S3().list_files(bucket=self.cfg.dataset.bucket, folder=self.cfg.dataset.raw_file)

        files = ['renttherunway_final_data.json']
        return files

    def __download_file(self, key: str) -> str:
        # response = S3().download_file(bucket=self.cfg.dataset.bucket, key=key)
        # if not response:
        #     log.error(f"Can't download file {key}. Exiting...")
        #     exit(code=1)

        key = 'renttherunway_final_data.json'
        return key.split('/')[-1]

    def __read_file(self, file: str) -> pd.core.frame.DataFrame:
        if self.cfg.dataset.format == 'json':
            return self.__read_json(file)
        else:
            log.error("Trying to read a file with a not implemented method!")
            raise NotImplemented

    @staticmethod
    def __read_json(file: str) -> pd.core.frame.DataFrame:
        log.info("Reading json file")
        return pd.read_json(file, lines=True)
