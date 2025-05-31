
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time

app = Flask(__name__)

room_data = [
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

def get_reserved_dates(room_id):
    url = f"https://www.airbnb.co.kr/rooms/{room_id}#availability-calendar"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=ko-KR')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    reserved_tags = soup.find_all(attrs={"data-is-day-blocked": "true"})

    today = datetime.today()
    reserved_dates = []

    for tag in reserved_tags:
        test_id = tag.get("data-testid", "")
        if test_id.startswith("calendar-day-"):
            date_str = test_id.replace("calendar-day-", "").strip(".")
            try:
                date_obj = datetime.strptime(date_str, "%Y.%m.%d")
                if date_obj > today:
                    reserved_dates.append(date_str)
            except:
                continue

    return sorted(set(reserved_dates))

@app.route("/", methods=["GET", "POST"])
def index():
    selected = request.form.get("room_id")
    results = []

    if selected == "all":
        targets = room_data
    elif selected:
        targets = [r for r in room_data if r[0] == selected]
    else:
        targets = []

    for room_id, rtype, rname in targets:
        try:
            dates = get_reserved_dates(room_id)
        except Exception as e:
            dates = [f"❌ 오류 발생: {e}"]
        results.append((rtype, rname, dates, len(dates)))

    return render_template("index.html", room_data=room_data, results=results)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
