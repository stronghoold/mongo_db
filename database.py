import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL)

database = client.get_database(os.getenv("MONGO_DB_NAME"))



collection = database.get_collection("users")

async def test_connection():
    try:
        await client.admin.command('ping')
        print("Conexión exitosa a la base de datos MongoDB")
    except Exception as e:
        print(f"Error al conectar a la base de datos MongoDB: {e}")
        
if __name__ == "__main__":
    asyncio.run(test_connection())