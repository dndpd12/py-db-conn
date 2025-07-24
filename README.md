1. 온라인 환경에서 패키지 다운로드
다음 명령으로 requirements.txt에 명시된 패키지를 whl 또는 tar.gz 파일로 미리 다운로드할 수 있습니다:

bash
복사
편집
pip download -r requirements.txt -d ./packages
./packages 폴더에 모든 의존성 포함 패키지 파일이 저장됩니다.

2. 폐쇄망 환경에서 설치
위에서 다운로드한 packages 폴더를 폐쇄망 서버에 옮긴 후:

bash
복사
편집
pip install --no-index --find-links=./packages -r requirements.txt
--no-index: PyPI 같은 온라인 저장소를 사용하지 않고 로컬 패키지만 사용.

--find-links=./packages: 지정한 폴더에서 패키지를 찾음.

3. 주의할 점
pip download는 requirements.txt에 버전이 명시된 패키지와 의존성 패키지까지 모두 가져옵니다.

Python 버전이 폐쇄망 환경과 동일해야 합니다. (예: 3.12 환경이면 3.12에 맞는 wheel을 다운로드해야 합니다.)

OS 환경도 동일해야 합니다. (Windows용 패키지는 Linux에서 설치 불가)

4. 예시 워크플로우
bash
복사
편집
# 온라인 환경
pip freeze > requirements.txt
pip download -r requirements.txt -d ./packages

# packages + requirements.txt를 폐쇄망 서버에 복사

# 폐쇄망 환경
pip install --no-index --find-links=./packages -r requirements.txt


alias python=python3 ~/.zshrc   
alias pip=pip3 ~/.zshrc   

shiftt + commnad +p

python -m pip install pymysql
python3 -m pip install psycopg2-binary

pip3 install pandas openpyxl



— 지금 현재 library 형태로 requirements 파일 만들기
python -m pip freeze > requirements.txt



uvicorn server:app --reload --host 0.0.0.0 --port 8000
