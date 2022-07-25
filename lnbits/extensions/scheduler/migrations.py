async def m001_initial(db):
   await db.execute(
       f"""
       CREATE TABLE scheduler.scheduled_payment (
           id TEXT PRIMARY KEY,
           wallet TEXT NOT NULL,
           lnurlpay TEXT NOT NULL
       );
   """
   )
