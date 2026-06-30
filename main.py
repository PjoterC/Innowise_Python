import data_loader
from db_connector import DatabaseConnection, PostgresConnection


def load_data(connection) -> None:
    loader = data_loader.DataLoader(connection)
  
    roomcount = loader.load(data_loader.JsonFileDataSource("rooms.json"), data_loader.ROOMS)
    print(f"Loaded {roomcount} rooms")
    studentcount = loader.load(data_loader.JsonFileDataSource("students.json"), data_loader.STUDENTS)
    print(f"Loaded {studentcount} students")


def main(database: DatabaseConnection = None) -> None: # type: ignore
    database = database or PostgresConnection()
    try:
        connection = database.connect()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    print("✅ Connection successful")
    try:
        load_data(connection)
    finally:
        database.close()
        print("✅ Connection closed")


if __name__ == "__main__":
    main()
