# connections.py
from contextlib import contextmanager
from django.conf import settings
import oracledb

@contextmanager
def oracle_connection():
    db_config = settings.DATABASES['peoplesoft']
    
    dsn = oracledb.makedsn(
        db_config['HOST'], 
        db_config['PORT'], 
        service_name=db_config['NAME']
    )

    conn = None
    try:
        conn = oracledb.connect(
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            dsn=dsn
        )
        yield conn
    finally:
        if conn:
            conn.close()