"""Standalone script to initialize the database tables."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db


async def main():
    print("Creating database tables...")
    await init_db()
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
