from fastapi import FastAPI
from datetime import datetime

from database import get_session

app = FastAPI()


@app.post("/")
def root():
    return {"message": "FastAPI + Cassandra works"}

@app.post("/tags")
def create_tag_value(tag_name: str, value: float):

    now = datetime.now()

    day = now.strftime("%Y-%m-%d")

    get_session().execute("INSERT INTO tag_history_v2 (tag_name,day,ts,value) VALUES (%s, %s,%s,%s)",
        (tag_name,day,now,value)
    )

    return {
        "status": "saved",
        "tag": tag_name,
        "value": value
    }

@app.get("/tags/{tag_name}")
def get_tag_history(tag_name: str):

    today = datetime.now().strftime("%Y-%m-%d")

    rows = get_session().execute("""SELECT * FROM tag_history_v2 where tag_name = %s and day = %s""", (tag_name,today))

    result = []

    for row in rows:
        result.append({
            "timestamp": row.ts,
            "value": row.value
        })
    return result

@app.get("/tags/{tag_name}/latest")
def get_latest_tag_history(tag_name: str):

    today = datetime.now().strftime("%Y-%m-%d")

    rows = get_session().execute("""SELECT * FROM tag_history_v2 where tag_name = %s and day = %s limit 10""", (tag_name,today))

    result = []

    for row in rows:
        result.append({
            "timestamp": row.ts,
            "value": row.value
        })
    return result

@app.get("/health")
def health():
    return {
        "status": "ok"
    }    
            