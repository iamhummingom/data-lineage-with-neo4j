from neo4j import GraphDatabase
import logging
import os
import json
from pathlib import Path
from collections import OrderedDict
from distutils.util import strtobool

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
log = logging.getLogger()


def _setup_logging():
    if log.handlers:
        for handler in log.handlers:
            log.removeHandler(handler)

    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logging.getLogger("botocore").setLevel("ERROR")
    logging.getLogger("boto3").setLevel("ERROR")


def get_query(query_path) -> str:
    """
    used standard way of reading query files contents
    :param query_path: complete query path in str
    :return: content of the query file removing trailing empty strings
    """
    path = Path(query_path).read_text().rstrip()
    if path is None:
        log.error("Failed to read query")
    return path


def load_data():
    _setup_logging()
    driver = GraphDatabase.driver(uri="bolt://neo4j:7687", auth=("neo4j", os.getenv("NEO4J_PASSWORD")),
                                  encrypted=False)
    session = driver.session()
    with open("cypher/data_config.json") as input_file:
        data_config = json.loads(input_file.read(), object_pairs_hook=OrderedDict)
    if strtobool(os.getenv("RECREATE_SCHEMA", "False")) == 1:
        for script in data_config["recreate_schema"]:
            query = get_query(script)
            log.info(f'running script : {script}')
            session.run(query)
    for script in data_config["load"]:
        query = get_query(script)
        log.info(f'running script : {script}')
        session.run(query)
    log.info('Data loaded successfully')


if __name__ == "__main__":
    load_data()
