## Slack 자동화 툴

### 하는 일
1. 슬랙 채널의 메시지 / 덧글 / 리액션 긁어오기
2. 긁어온 슬랙 채널의 메시지 / 덧글 / 리액션을 별도의 구글 시트에 기록하기

### 사용 방법
1. 트래킹하고 싶은 슬랙 채널에 `sungle_bot` 슬랙 app 추가
    - 해당 채널에 `/invite @sungle_bot` 입력하면 봇이 추가됨
    - 2주차까지는 초대 작업 완료했습니다
2. `variables.txt`에서 트래킹하고 싶은 slack channel 이름 변경
    - 디폴트로는 테스트를 위해 `admin-트래킹자동화`로 되어 있음
    - 프라이빗 채널일 경우 `app.py`의 main() 함수에서 `private=True`로 설정
    - 퍼블릭 채널일 경우 `app.py`의 main() 함수에서 `private=False`로 설정
3. `pip install -r requirements.txt`
4. `python -m app.py`
5. 실행 과정에서 구글 로그인 화면이 뜬다면, 성글 어드민 계정으로 로그인
6. 성공적으로 작동했다면, "Data written to sheet successfully" 문구가 출력

### 글 트래킹 시트 작성 포맷
| 글_ID       | 글_작성시간               | 작성자_이름 | 작성자_ID | 글_내용                  | 글_리액션                                                                                                                                               |
|-------------|---------------------------|-------------|-----------|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| 61862b07-81 | 2023. 11. 24 오후 4:13:05 | sksoup      | U45N      | This is the test message | [{"name": "eyes", "users": ["DP02FG"], "count": 1, "user_name": ["someuser"]}, {"name": "bug", "users": ["405N"], "count": 1, "user_name": ["sksoup"]}] |

### 덧글 트래킹 시트 작성 포맷
| 글_ID       | 덧글_ID     | 덧글_작성시간             | 작성자_이름 | 작성자_ID | 덧글_내용              | 덧글_리액션                                                                                                                                             |
|-------------|-------------|---------------------------|-------------|-----------|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| 61862b07-81 | ev44g597-d2 | 2023. 11. 24 오후 4:13:16 | sksoup      | U45N      | This is the test reply | [{"name": "eyes", "users": ["DP02FG"], "count": 1, "user_name": ["someuser"]}, {"name": "bug", "users": ["405N"], "count": 1, "user_name": ["sksoup"]}] |
