from common.db_connection import get_connection, close_connections
from common.module import insert_db, insert_csv_to_db


def main():
    print('test')

    elect_query = """
    
    """

    insert_query = """
    insert into member (member_no,member_nm,mobile,company_no) values (%s,%s,%s,%s)
    """

    try:
          # select 대상db
        #select_conn = get_connection('TT')
          # insert 대상db
        insert_conn = get_connection('postgresql')

          # *************1, 2둘중 하나만 수행해서 주석처리로 사용해야함*************
          # 1번은 csv파일을 열어서 '열'만큼 insert문에 추가하여 수행해야함 (select 문 사용안함, data.csv파일 사용)
          # 2번은 select, insert query 사용함

          # 1. CSV → INSERT (헤더 스킵)
        insert_csv_to_db('data.csv', insert_query, insert_conn)

          # 2. DB INSERT
          # insert_db(select_conn, insert_conn, select_query, insert_query)

    except Exception as e:
        print(f"\033[91mX 예외 발생\033[0m", e)

          # CSV EXPORT
          # (select_conn, insert_conn, select_query, insert_query)

    finally:
        close_connections()

if __name__ == '__main__':
    main()