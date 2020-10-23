import hydra
from src.factory import *


log = Logger(__name__).instance


def conduct(cfg: dictconfig):
    dataset = Dataset(cfg)

    files = dataset.get_files()
    [dataset.exploratory_data_analysis(file) for file in files]
    log.info(f"Ending process: {datetime.now().strftime('%H:%M:%S')}\n")
    log.info("  ---------------------------------------------------------------  \n")


@hydra.main(config_path="conf/config.yaml")
def job_export(cfg: dictconfig):
    log.info(f"{cfg.dataset.name.upper()} - starting time: {datetime.now().strftime('%H:%M:%S')}")
    conduct(cfg)


if __name__ == '__main__':
    job_export()
