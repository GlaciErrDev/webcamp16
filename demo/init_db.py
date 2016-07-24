import term
import sqlalchemy as sa

from demo import settings
from demo.db import metadata


def init_db():
    dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(
        user=settings.DB_USER,
        database=settings.DATABASE,
        host=settings.DB_HOST,
        password=settings.DB_PASSWORD
    )
    term.writeLine('Creating all tables on {dsn}'.format(dsn=dsn), term.bold)
    engine = sa.create_engine(dsn)

    metadata.create_all(engine)
    term.writeLine('{count} tables are successfully '
                   'created!'.format(count=len(metadata.tables)),
                   term.green)


if __name__ == '__main__':
    init_db()
