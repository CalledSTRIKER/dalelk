import pandas as pd
import os
pd.set_option('display.max_rows', None)
print("Loading & preprocessing courses..")
# ===========================================
# Courses Dataset
# ===========================================

courses_dataset = os.path.join(os.path.dirname(__file__), "datasets", "Courses_new.xlsx")
courses_file = pd.ExcelFile(courses_dataset)

list_of_dfs = []

for sheet in courses_file.sheet_names:
    
    df = courses_file.parse(sheet)

    # And append it to the list
    list_of_dfs.append(df)
    
# Combine all DataFrames into one
course_df = pd.concat(list_of_dfs, ignore_index=True)

course_df = course_df.dropna(how='all')

# Facts as dictionaries
course_facts_list = []
for idx, row in course_df.iterrows():
    fact = {col: row[col] for col in course_df.columns}
    course_facts_list.append(fact)

# Courses facts texts
course_texts = []
for fact in course_facts_list:
    text = (
        f"المقرر: {fact['Course Title']} | "
        f"الرمز: {fact['Course Code']} | "
        f"التخصص: {fact['Major']} | "
        f"المستوى: {fact['Level']} | "
        f"الدفعة: {fact['Batch']} | "
        f"الساعات: {fact['Credit Hours']} | "
        f"النوع: {'إلزامي' if fact['Elective'] == 'لا' else 'اختياري'} | "
        f"المتطلبات: {fact['Course Prerequisites']}"
    )
    course_texts.append(text)

print("Loading & preprocessing certificates..")
# ===========================================
# Certification Dataset
# ===========================================
cert_dataset = os.path.join(os.path.dirname(__file__), "datasets", "Certifications.xlsx")
cert_df = pd.read_excel(cert_dataset)
cert_df = cert_df.dropna(how='any')
cert_df = cert_df.drop(columns="Subdomain")  # we don't need it

# Facts as dictionaries
cert_facts_list = []
for idx, row in cert_df.iterrows():
    fact = {col: row[col] for col in cert_df.columns}
    cert_facts_list.append(fact)

# Certification facts
cert_texts = []
courses_for_cert = []
codes_and_titles = ""

# Build joined "course title - code" string
for codes, titles in zip(cert_df["Course Code"], cert_df["Course Title"]):
    codes = codes.split(",")
    titles = titles.split(",")
    for code, title in zip(codes, titles):
        codes_and_titles += f"{title} - {code}\n"
    else:
        courses_for_cert.append(codes_and_titles)
        codes_and_titles = ""

for i, fact in enumerate(cert_facts_list):
    text = (
        f"الشهادة: {fact['Certificate Name']} | "
        f"الجهة المانحة: {fact['Awarding Body']} | "
        f"التخصص: {fact['Major']} | "
        f"المواضيع: {fact['Topic']} | "
        f"المقررات المرتبطة (يفضل أخذها): \n{courses_for_cert[i]}"
    )
    cert_texts.append(text)

print("Loading & preprocessing Q&A..")
# ===========================================
# Q&A Dataset
# ===========================================
qa_dataset = os.path.join(os.path.dirname(__file__), "datasets", "QA.xlsx")
qa_df = pd.read_excel(qa_dataset)
qa_df = qa_df.dropna(how='any')

questions_and_answers = list(zip(qa_df["question"], qa_df["answer"]))

ids = qa_df["id"].values
questions = qa_df["question"].tolist()
