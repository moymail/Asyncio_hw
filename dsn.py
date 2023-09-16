from sqlalchemy.ext.asyncio import create_async_engine


dialect = 'postgresql+asyncpg'
username = 'asyncio'
password = "1234"
host = '127.0.0.1'
port = '5431'
database = 'asyncio'


DSN = f'{dialect}://{username}:{password}@{host}:{port}/{database}'

engine = create_async_engine(DSN)