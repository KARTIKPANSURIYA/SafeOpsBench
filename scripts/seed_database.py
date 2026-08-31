from safeopsbench.db.seed import seed_session
from safeopsbench.db.session import create_database
engine,factory=create_database("sqlite+pysqlite:///safeopsbench.db");seed_session(factory());engine.dispose()
