import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from time import sleep
from logger import logger
from datetime import datetime
from data_loader import (
    course_facts_list,
    course_texts,
    cert_facts_list,
    cert_texts,
)
from retrieve import smart_retrieve
from query_classifer import analyze_query_intent


logger.info("Loading API keys..")
load_dotenv()


api_keys = [
    os.getenv("API_KEY1"),  # Primary
    os.getenv("API_KEY2"),  # Backup 1
    os.getenv("API_KEY3"),  # Backup 2
    os.getenv("API_KEY4"),  # Backup 3
]

models = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3-flash-preview"
]

# you may add if you have more, just add them to .env
    #os.getenv("API_KEY2"),  # Backup 1
    #os.getenv("API_KEY3"),  # Backup 2
    #os.getenv("API_KEY4"),  # Backup 3

user_history = {}

current_model = models[0]
current_key_index = 0
google_api_key = api_keys[current_key_index]
client = genai.Client(api_key=google_api_key)
model_id = 0

def switch_to_next_model():
    global model_id, current_model

    if not any(models):
        logger.error("You don't have any models.")
        return False

    for i in range(1, len(models)):
        current_model_check = models[(model_id + i) % len(models)]
        if current_model_check:
            model_id = (model_id + i) % len(models)
            break

    else:
        logger.error("No alternative model to switch to.")
        return False

    current_model = current_model_check

    logger.info(f"Switched to model {model_id}/{len(models)}")

    return True


def switch_to_next_key():
    global current_key_index, google_api_key, client

    if not any(api_keys):
        logger.error("You don't have any valid API key.")
        return False

    for i in range(1, len(api_keys)):
        google_api_key = api_keys[(current_key_index + i) % len(api_keys)]
        if google_api_key:
            current_key_index = (current_key_index + i) % len(api_keys)
            break
    else:
         logger.error("No alternative valid API key to switch to.")
         return False


    client = genai.Client(api_key=google_api_key)
    logger.info(f"Switched to API key {current_key_index}/{len(api_keys)}")
    return True

def is_rate_limit_error(error) -> bool:
    error_msg = str(error).lower()
    rate_limit_indicators = [
        "quota", "rate limit", "resource exhausted",
        "exceeded", "429", "billing", "overloaded"
    ]
    return any(indicator in error_msg for indicator in rate_limit_indicators)

def generate_answer(query: str, major: str, batch: str, student_id: str) -> str:
    if student_id in user_history:
        time_passed = ((datetime.now() - user_history[student_id]["timestamp"][0]).total_seconds() / 60)
        if int(time_passed) >= 30: # if more than 30 minutes it will get deleted
            del user_history[student_id]


    topic, size = analyze_query_intent(query)
    retrieved_facts, topic = smart_retrieve(query, topic, size)

    if topic == "course":
        query += f"\nالتخصص : {major}"
        query += f"\nالدفعة : {batch}"

    context_lines = []
    for fact in retrieved_facts:
        if fact in course_facts_list:
            idx = course_facts_list.index(fact)
            context_lines.append(course_texts[idx])
        elif fact in cert_facts_list:
            idx = cert_facts_list.index(fact)
            context_lines.append(cert_texts[idx])
        else:
            context_lines.append(f"السؤال : {fact[0]}\nالإجابة : {fact[1]}")

    context = (
        ("\n" + ("-" * 20) + "\n").join(context_lines)
        if context_lines
        else "لا توجد معلومات متاحة"
    )

    system_prompt = """أنت مرشد أكاديمي ذكي في كلية علوم وهندسة الحاسب بجامعة جدة.
مهمتك هي الإجابة على 3 أنواع من الأسئلة :
- المقررات الدراسية
- الشهادات الإحترافية
- الإستفسارات العامة الأكاديمية

الأسئلة الموجهة لك هي أسئلة من قبل طلاب الكلية.
أجب بدقة، وبشكل مباشر، وباستخدام المعلومات المقدمة لك في السياق.
جاوب حسب التخصص والدفعة إذا كان السؤال عن المقررات الدراسية.
جاوب فقط على الأسئلة أكاديمية وقم برفض أي سؤال غير أكاديمي.
السؤال غير الاكاديمي الوحيد الذي يمكنك إجابته هو استفسار الطالب عن رسائله وإجاباتك السابقة، أو إذا كان سؤاله يتعلق بإجابتك السابقة.
قم بمراجعة إجاباتك السابقة دائما، إذا كانت أحد الإجابات السابقة تحوي إجابة السؤال الحالي فيمكنك استعمالها.
في حال لم تكن متأكدا من الإجابة لأن السؤال يتطلب معلومة موثوقة والمعلومة غير متاحة فلا تجب على السؤال."""
    history_exists = user_history.get(student_id, {})
    history_lines = ''

    if history_exists:
        query_exists = len(user_history[student_id]["query"])
        if query_exists:
            for counter in range(query_exists):
                history_lines += f'Q{counter}: {user_history[student_id]["query"][counter]}\n'
                history_lines += f'A{counter}: {user_history[student_id]["answer"][counter]}\n'
                history_lines += f'{user_history[student_id]["timestamp"][counter]}\n'
                history_lines += "-----------------\n"

    user_prompt = f"""
<history>
هذه هي الرسائل السابقة للمستخدم مع إجابتك على كل سؤال، حيث Q تعني السؤال و A تعني الإجابة، والتاريخ هو تاريخ كل سؤال وإجابة.
-----------
{history_lines}
</history>

<context>
{context}
</context>

<task>
{query}
</task>
"""

    keys_tried = 0
    models_tried = 0
    retry = 0

    if os.getenv("DEBUG_AI") == "on":
        logger.info(f"History: {history_lines}")
        logger.info(f"Query: {query}, Topic : {topic}, Size: {size}")
        logger.info(f"Context: {context_lines}")

    while keys_tried < len(api_keys):
        try:
            response = client.models.generate_content(
                model=current_model,
                config=types.GenerateContentConfig(system_instruction=system_prompt),
                contents=user_prompt,
            )
            answer = response.text.strip()
            if student_id not in user_history: # If it was the first chat or it got deleted
                user_history[student_id] = {"query":[], "answer": [], "timestamp": []}

            user_history[student_id]["query"].append(query) # Append the answered query to the history
            user_history[student_id]["answer"].append(answer) # Append the answered query to the history
            user_history[student_id]["timestamp"].append(datetime.now()) # Append the timestamp to the history


            return answer if answer else "لا أملك معلومات كافية للإجابة على هذا السؤال."

        except ServerError as e:

            retry += 1

            if retry == 4:
                logger.error(f"Non-rate-limit error on {type(e).__name__}: {e}")
                break

            sleep(2 ** retry)
            continue

        except Exception as e:
            if is_rate_limit_error(e):
                logger.error(f"Rate-limit error on key {current_key_index + 1}: {type(e).__name__}: {e}")
                keys_tried += 1
                if keys_tried < len(api_keys):
                    logger.info("Switching to next API key...")
                    if switch_to_next_key() == False:
                        break
                    retry = 0
                    continue

                elif models_tried < len(models) - 1:
                    keys_tried = 0
                    logger.info("Switching to next model...")
                    if switch_to_next_model() == False:
                        break
                    retry = 0
                    models_tried += 1
                    continue

            else:
                logger.error(f"Non-rate-limit error on key {current_key_index + 1}: {type(e).__name__}: {e}")
            break



    return "عذرًا، حدث خطأ في الاتصال بخدمة الذكاء الاصطناعي. يرجى المحاولة مرة أخرى."
