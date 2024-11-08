from repository.database import check_database_connection
import bcrypt


async def on_startup():
    await check_database_connection()
    print("Application startup: Database connection checked.")

async def on_shutdown():
    print("Application shutdown: Cleaning up resources.")


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed_password

