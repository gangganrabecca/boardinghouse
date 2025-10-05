import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnector:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.driver = None
        
    def connect(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            print("Successfully connected to Neo4j Aura")
            return True
        except Exception as e:
            print(f"Error connecting to Neo4j: {e}")
            return False
    
    def close(self):
        if self.driver:
            self.driver.close()
    
    def get_session(self):
        if not self.driver:
            self.connect()
        return self.driver.session()

# Global instance
neo4j_connector = Neo4jConnector()