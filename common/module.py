from .db_config_loader import get_batch_size
import xml.etree.ElementTree as ET
import csv
import pandas as pd


def insert_xlsx_to_db(xlsx_path, insert_query, db_conn):
    batch_size = get_batch_size()
    total = 0

    df = pd.read_excel(xlsx_path)

    # null 처리
    def nullify_empty(value):
        return value if pd.notnull(value) and str(value).strip() != '' else None

    # float -> text로 바꾸는 로직
    def normalize_id(val):
        if val is None:
            return None
        try:
            f = float(val)
            i = int(f)
            return str(i)
        except (ValueError, TypeError):
            return str(val).strip()

    # 헤더 스킵, 각 row에 대해 null/normalize 처리
    rows = [
        tuple(nullify_empty(normalize_id(col)) for col in row)
        for row in df.values
    ]

    with db_conn.cursor() as cursor:
        try:
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                cursor.executemany(insert_query, batch)
                total += len(batch)
                print(f"✅ {total} rows inserted from XLSX.")
            db_conn.commit()
        except Exception as e:
            db_conn.rollback()
            print(f"\033[91mX 예외 발생 Rollback \033[0m ", e)

# CSV → DB INSERT (헤더 제외)

def insert_csv_to_db(csv_path, insert_query, db_conn):

  batch_size = get_batch_size()
  total = 0

  with open(csv_path, newline='', encoding='cp949', errors='replace') as csvfile:
    reader = csv.reader(csvfile)

    next(reader) # 헤더 스킵

    # null 처리
    def nullify_empty(value):
      return value if value.strip() != '' else None

    # float -> text로 바꾸는 로직 (엑셀에서 89+E 이런형태로 들어와서 한건데 엑셀에서 text로 copy해야함. 의미없음.)
    def normalize_id(val):
      if val is None:
        return None
      try:
        f=float(val)
        i = int(f)
        return str(i)
      except (ValueError,TypeError):
        return val.strip() if isinstance(val,str) else val

    rows = [tuple(nullify_empty(normalize_id(col)) for col in row) for row in reader]


    with db_conn.cursor() as cursor:
      try:
        for i in range(0, len(rows), batch_size):
          batch = rows[i:i + batch_size]
          cursor.executemany(insert_query, batch)
          total += len(batch)
          print(f"✅ {total} rows inserted from CSV.")
        db_conn.commit()
      except Exception as e:
        db_conn.rollback()
        print(f"\033[91mX 예외 발생 Rollback \033[0m ",e)


def read_query_from_xml(file_path):
  tree = ET.parse(file_path)

  root = tree.getroot()

  return root.find('query').text.strip()


def insert(insert_query, batch, db2_conn):
  with db2_conn.cursor() as cursor:
    cursor.executemany(insert_query, batch)


def insert_db(select_conn, insert_conn, select_query, insert_query):
  batch_size = get_batch_size()

  # select -> INSERT 문
  with select_conn.cursor() as cursor1:
    cursor1.execute(select_query)
    total = 0

    try:
      while True:

        batch = cursor1.fetchmany(batch_size)
        if not batch:
          break

        insert(insert_query, batch, insert_conn)
        total += len(batch)
        print(f"Inserted {total} rows so far...")

      insert_conn.commit()
      print(f"✅ Done! Total {total} rows inserted.")
    except Exception as e:
      insert_conn.rollback()
      print(f"\033[91mX 예외 발생 Rollback \033[0m ",e)



