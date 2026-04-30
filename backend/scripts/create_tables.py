import asyncio
from core.database import engine
from models import Base

async def create_tables():
    try:
        async with engine.begin() as connect_db:
            await connect_db.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Error when creating tables: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())