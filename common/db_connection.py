import pymysql
import psycopg2
from psycopg2.extras import DictCursor
from .db_config_loader import load_db_config


_connection_cache ={}



def _is_connection_open(conn):
    if hasattr(conn, 'open'):  # pymysql
        return conn.open
    elif hasattr(conn, 'closed'):  # psycopg2
        return conn.closed == 0
    elif hasattr(conn, 'closed'):  # pyodbc
        try:
            conn.cursor()  # 간단 쿼리로 체크 가능
            return True
        except:
            return False
    return False

def _connect_mysql(cfg):
    return pymysql.connect(
        host=cfg['host'],
        port=int(cfg.get('port', 3306)),
        user=cfg['user'],
        password=cfg['password'],
        database=cfg['database'],
        cursorclass=pymysql.cursors.Cursor
    )

def _connect_postgres(cfg):
    return psycopg2.connect(
        host=cfg['host'],
        port=int(cfg.get('port', 5432)),
        user=cfg['user'],
        password=cfg['password'],
        dbname=cfg['database'],
        cursor_factory=DictCursor
    )

def _connect_tibero(cfg):
    if not cfg.get('odbc_driver'):
        raise ValueError("Tibero ODBC driver name ('odbc_driver') must be specified in config.")
    conn_str = (
        f"DRIVER={{{cfg['odbc_driver']}}};"
        f"SERVER={cfg['host']};"
        f"PORT={cfg['port']};"
        f"UID={cfg['user']};"
        f"PWD={cfg['password']};"
        f"DATABASE={cfg['database']};"
    )
    return pyodbc.connect(conn_str)

DB_DRIVERS = {
    'mysql': _connect_mysql,
    'postgres': _connect_postgres,
    'postgresql': _connect_postgres,
    'tibero': _connect_tibero,
}

def get_connection(section):
    if section in _connection_cache:
        conn = _connection_cache[section]
        if _is_connection_open(conn):
            return conn

    db_config = load_db_config(section)
    db_type = db_config.get('type', 'mysql').lower()

    if db_type not in DB_DRIVERS:
        raise ValueError(f"Unsupported DB type: {db_type}")

    conn = DB_DRIVERS[db_type](db_config)
    _connection_cache[section] = conn
    return conn

def close_connections():
    for conn in _connection_cache.values():
        try:
            if _is_connection_open(conn):
                conn.close()
        except:
            pass
    _connection_cache.clear()