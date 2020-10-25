from datetime import datetime
from src.factory import *
import hydra


log = Logger(__name__).instance


def conduct(cfg: dictconfig) -> None:
    dataset = Dataset(cfg)

    files = dataset.get_files()
    [dataset.data_analysis(file) for file in files]
    log.info(f"Ending process: {datetime.now().strftime('%H:%M:%S')}\n")
    log.info("  ---------------------------------------------------------------  \n")


@hydra.main(config_path="conf/config.yaml")
def job(cfg: dictconfig) -> None:
    log.info(f"{cfg.dataset.name.upper()} - starting time: {datetime.now().strftime('%H:%M:%S')}")
    conduct(cfg)


if __name__ == '__main__':
    job()
