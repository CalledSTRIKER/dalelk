from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, Field
from collections import defaultdict
import sqlite3
import re
import time
import uuid
import os
from datetime import datetime


app = FastAPI()

# Change later for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


banned_ips = {}
violations = defaultdict(list)

def get_real_ip(request: Request):
    return request.headers.get("X-Real-IP") or get_remote_address(request)

limiter = Limiter(key_func=get_real_ip)
app.state.limiter = limiter

def ban_ip(ip, duration_minutes=60):
    banned_ips[ip] = datetime.now().timestamp() + (duration_minutes * 60)

def check_ban(request: Request):
    ip = get_real_ip(request)
    now = datetime.now().timestamp()
    banned_until = banned_ips.get(ip)

    if banned_until is None:
        return

    if now < banned_until:
        raise HTTPException(status_code=403, detail="You've been banned temporary for repeated rate limits excessions.")

    else:
        del banned_ips[ip]

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    ip = get_real_ip(request)
    now = datetime.now()
    violations[ip] = [v for v in violations[ip] if (now - v).total_seconds() <= 86400]
    violations[ip].append(now)
    count = len(violations[ip])

    if count == 4:
        ban_ip(ip)
        return JSONResponse(status_code=403, content={"detail":"You've been banned for 1 hour for repeated rate limits excessions."})

    elif count > 6:
        ban_ip(ip, 21600)
        return JSONResponse(status_code=403, content={"detail":"You've been banned for much longer time for repeated rate limits excessions."})

    return JSONResponse(status_code=429, content={"detail":"Too many requests."})



# Majors
majors_dict = {
    "cs": "علوم الحاسب",
    "ai": "الذكاء الاصطناعي",
    "ds": "علوم البيانات",
    "cy": "الأمن السيبراني",
    "sw": "هندسة البرمجيات",
    "ce": "هندسة الحاسب والشبكات"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "feedback.db")


# Feedback model
class FeedbackModel(BaseModel):
    question: str = Field(..., max_length=500)
    answer: str = Field(..., max_length=3000)
    feedback: str
    question_id: str
    response_time: float

# Query model
class QueryModel(BaseModel):
    question: str

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS feedbacks (
        question_id TEXT PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        response_time REAL NOT NULL,
        feedback TEXT NOT NULL CHECK(feedback IN ('good', 'bad')),
        uj_major TEXT NOT NULL,
        uj_student_id TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    conn.commit()
    return conn

# The AI Function
def process_query(question: str, major: str, batch: str, student_id: str):
    return {"answer": "This is a mock answer for demonstration purposes."}

# Question endpoint

@app.post("/api/query",  dependencies=[Depends(check_ban)])
@limiter.limit("4/minute")
def query(request: Request, body: QueryModel):
    # For calculating response time
    start_time = time.perf_counter()

    # Giving it an unique ID
    question_id = str(uuid.uuid4())

    # Sanitizing input from prompt injection
    question = re.sub(r"[<>;{}[\]#/$]", "", body.question).strip()

    # Extracting cookies
    student_id = request.cookies.get("uj_student_id")
    major_key = request.cookies.get("uj_major")

    # Question length check
    if len(question) < 3:
        raise HTTPException(status_code=400, detail="Error: Question is too short.")

    # Check if cookies exist
    if not student_id or not major_key:
        raise HTTPException(status_code=400, detail="Error: Student ID and major are required.")

    # Student ID digits constraint
    if not re.fullmatch(r"\d{7}", student_id):
        raise HTTPException(status_code=400, detail="Error: Student ID must be 7 digits.")

    # Must be one of the majors in the dictonary
    if major_key not in majors_dict:
        raise HTTPException(status_code=400, detail="Invalid major value.")

    major = majors_dict[major_key]

    # Extracting the batch from Student ID
    student_batch = str(student_id)[:2]

    if int(student_batch) > 23:
        student_batch = "الجديدة"
    else:
        student_batch = "القديمة"

    # Calling the AI
    response = process_query(question, major, student_batch, student_id)

    # For calculating response time
    end_time = time.perf_counter()
    r_time = round((end_time - start_time) * 1000, 2) # convert to milliseconds

    # Adding response time and question id
    response["response_time"] = r_time
    response["question_id"] = question_id


    return response

@app.post("/api/feedback", dependencies=[Depends(check_ban)])
@limiter.limit("20/minute")
def submit_feedback(request: Request, data: FeedbackModel):
    # Get the current timestamp
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    student_id = request.cookies.get("uj_student_id")
    major_key = request.cookies.get("uj_major")

    if not student_id or not major_key:
        raise HTTPException(status_code=400, detail="Error: Student ID and major are required.")

    if not re.fullmatch(r"\d{7}", student_id):
        raise HTTPException(status_code=400, detail="Error: Student ID must be 7 digits.")

    if major_key not in majors_dict:
        raise HTTPException(status_code=400, detail="Invalid major value.")

    # Checking if all fields exist
    for field_name, value in data.dict().items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise HTTPException(status_code=400, detail=f"The field '{field_name}' cannot be empty")

    # Feedback value must be good or bad
    feedback_value = data.feedback.lower()
    if feedback_value not in ["good", "bad"]:
        raise HTTPException(status_code=400, detail="Feedback must be 'good' or 'bad'")

    # Response time must be positive and float.
    if not isinstance(data.response_time, float) or data.response_time <= 0:
       raise HTTPException(status_code=400, detail="Response time must be a positive float")

    conn = get_db()
    cursor = conn.cursor()
    # If the record for the same question exists; delete it and add the new one.
    cursor.execute("DELETE FROM feedbacks WHERE question_id = ?", (data.question_id,))

    # Inserting the data into the database using prepared statements to prevent SQL Injection.
    cursor.execute("""
        INSERT INTO feedbacks (question_id, question, answer, response_time, feedback, uj_major, uj_student_id, created_at )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (data.question_id, data.question, data.answer, data.response_time, feedback_value,  majors_dict[major_key], student_id, created_at))

    conn.commit()
    conn.close()

    return {"message": "Feedback saved successfully."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False)