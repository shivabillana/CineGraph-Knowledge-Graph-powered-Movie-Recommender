from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
load_dotenv()

uri = os.getenv("uri")
username = os.getenv("username_neo")
password = os.getenv("password")

driver = GraphDatabase.driver(uri, auth=(username,password))

def get_driver():
    return driver

# Optional but recommended
if __name__ == "__main__":
    try:
        driver.verify_connectivity()
        print("✅ Connected to Neo4j successfully")
    except Exception as e:
        print(f"❌ Connection failed: {e}")