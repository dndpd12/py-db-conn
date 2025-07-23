import configparser

CONFIG_FILE = 'common/db_config.ini'


def load_db_config(section):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    if section not in config:
        raise ValueError(f"Section [{section}] not found in {CONFIG_FILE}")

    db_type = config[section].get('type', 'mysql').lower()

    supported_db_types = ('mysql', 'postgres', 'postgresql', 'tibero')
    if db_type not in supported_db_types:
        raise ValueError(f"Unsupported DB type: {db_type}")

    default_ports = {
        'mysql': 3306,
        'postgres': 5432,
        'postgresql': 5432,
        'tibero': 8629,
    }
    default_port = default_ports.get(db_type, 3306)

    return {
        'type': db_type,
        'host': config[section]['host'],
        'port': config.getint(section, 'port', fallback=default_port),
        'user': config[section]['user'],
        'password': config[section]['password'],
        'database': config[section]['database'],
        'odbc_driver': config[section].get('odbc_driver', ''),  # Tibero용 ODBC 드라이버명
    }

def get_batch_size(default=10000):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        return config.getint('options', 'batch_size', fallback=1000)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default