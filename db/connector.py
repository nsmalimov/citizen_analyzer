import asyncpg

async def connect_to_db(host):
    conn = await asyncpg.connect(user='postgres', password='ghsgdh12',
                                 database='citizen_analyzer', host=host)
    
    return conn
