from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

# ✅ 객실 ID와 이름 매핑
rooms = [
    ("1310456538491337564", "B/E", "#1 파인릴렉스(수퍼킹)"),
    ("1313524133477209346", "B/E", "#2 파인릴렉스(수퍼킹)"),
    ("1313527463157595989", "B/E", "#3 파인릴렉스(수퍼킹)"),
    ("1313530122933363235", "B/E", "#4 파인릴렉스(수퍼킹)"),
    ("1314988728421012929", "B/E", "#5 파인릴렉스(수퍼킹)"),
    ("1315050464965138670", "B/E", "#6 파인릴렉스(수퍼킹)"),
    ("1315085270385143745", "B/E", "#7 파인릴렉스(수퍼킹)"),
    ("1315090916311198024", "B/E", "#8 파인릴렉스(수퍼킹)"),
    ("1315100666031756011", "B/E", "#9 파인릴렉스(수퍼킹)"),
    ("1315119626981800855", "B/E", "#1 파인앤힐링 (퀸사이즈)"),
    ("1315121890814440800", "B/E", "#2 파인앤힐링 (퀸사이즈)"),
    ("1315122560894066658", "B/E", "#3 파인앤힐링 (퀸사이즈)"),
    ("1315124087245158911", "B/E", "#4 파인앤힐링 (퀸사이즈)"),
    ("1315124458774130134", "B/E", "#5 파인앤힐링 (퀸사이즈)"),
    ("1315126692230541668", "B/E", "#6 파인앤힐링 (퀸사이즈)"),
    ("1315127408216081001", "B/E", "#7 파인앤힐링 (퀸사이즈)"),
    ("1315129879545505910", "B/E", "#8 파인앤힐링 (퀸사이즈)"),
    ("1315130062282810106", "B/E", "#9 파인앤힐링 (퀸사이즈)"),
    ("1315132686200650033", "C", "#1 파인패밀리"),
    ("1315132693295511775", "C", "#2 파인패밀리"),
    ("1315136615926663390", "C", "#3 파인패밀리"),
    ("1315136620826211866", "C", "#4 파인패밀리 (1311 문성원)"),
    ("1315141993953024841", "C", "#5 파인패밀리"),
    ("1315142001959187224", "C", "#6 파인패밀리"),
    ("1315149647391684632", "A/F", "#1 파인오션트레블 (투룸)"),
    ("1315149653921555055", "A/F", "#2 파인오션트레블 (투룸)"),
    ("1315152008888032544", "A/F", "#3 파인오션트레블 (투룸)"),
    ("1315152016148616664", "A/F", "#4 파인오션트레블 (투룸)"),
    ("1315154299070283522", "A/F", "#5 파인오션트레블 (투룸) (1310 김송)"),
    ("1315154305924436167", "A/F", "#6 파인오션트레블 (투룸)")
]

# ✅ 예약 날짜 크롤링 함수
def get_reserved_dates(room_id):
    url = f"https://www.airbnb.co.kr/rooms/{room_id}#availability-calendar"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0.4430.212"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        today = datetime.today()
        reserved_dates = []

        for tag in soup.find_all(attrs={"data-is-day-blocked": "true"}):
            test_id = tag.get("data-testid", "")
            if test_id.startswith("calendar-day-"):
                date_str = test_id.replace("calendar-day-", "").strip(".")
                try:
                    date_obj = datetime.strptime(date_str, "%Y.%m.%d")
                    if date_obj > today:
                        reserved_dates.append(date_str)
                except:
                    continue

        return reserved_dates

    except Exception as e:
        return [f"❌ 오류: {e}"]

@app.route("/")
def index():
    return render_template("index.html", room_data=rooms, results=[])

@app.route("/check/<room_id>")
def check_room(room_id):
    reserved = get_reserved_dates(room_id)
    return jsonify({"room": rooms.get(room_id, room_id), "reserved": reserved, "count": len(reserved)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)