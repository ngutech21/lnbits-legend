from loguru import logger


async def m001_initial(db):
    logger.info("migrate db")
    print("aaaaaaaaacjkjjkjkjkjkjkjkjkjkjk")
    await db.execute(
        f"""
       CREATE TABLE scheduler.job_config (
           id TEXT PRIMARY KEY,
           user_name TEXT NOT NULL,
           wallet TEXT NOT NULL,
           lnurl TEXT NOT NULL,
           description TEXT,
           timer_minute int NOT NULL
       );
   """
    )
