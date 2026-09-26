from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_db():
    return driver.session()

def check_connection() -> bool:
    driver.verify_connectivity()
    return True

def close_driver() -> None:
    driver.close()
