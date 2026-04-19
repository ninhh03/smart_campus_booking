import asyncio
from core.database import engine
from models import Base

async def create_tables():
    print("Đang tạo bảng")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Đã tạo các bảng thành công!")
    except Exception as e:
        print(f"Lỗi trong quá trình tạo bảng: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())