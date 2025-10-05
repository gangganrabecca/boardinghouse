from app.database.neo4j_connector import neo4j_connector

def initialize_database():
    session = neo4j_connector.get_session()
    
    # Create constraints for uniqueness
    constraints = [
        "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
        "CREATE CONSTRAINT user_username IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE",
        "CREATE CONSTRAINT room_id IF NOT EXISTS FOR (r:Room) REQUIRE r.id IS UNIQUE",
        "CREATE CONSTRAINT room_number IF NOT EXISTS FOR (r:Room) REQUIRE r.room_number IS UNIQUE",
        "CREATE CONSTRAINT tenant_id IF NOT EXISTS FOR (t:Tenant) REQUIRE t.id IS UNIQUE",
        "CREATE CONSTRAINT booking_id IF NOT EXISTS FOR (b:Booking) REQUIRE b.id IS UNIQUE"
    ]
    
    for constraint in constraints:
        try:
            session.run(constraint)
            print(f"Created constraint: {constraint}")
        except Exception as e:
            print(f"Error creating constraint: {e}")

if __name__ == "__main__":
    if neo4j_connector.connect():
        initialize_database()
        print("Database initialized successfully!")
    else:
        print("Failed to connect to database")