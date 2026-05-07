import pandas as pd
import random

df_classifer_all_dataset= pd.DataFrame()

#----------------------------------Courses section-----------------------------------#
df_classifer_course_dataset= pd.DataFrame()
question_preq = []
question_optional = []
question_ask_codes = []
question_hours = []
question_level = []
question_titles = []

with open('courses/question_ask_codes.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        question_ask_codes.append(line.strip())

with open('courses/question_hours.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        question_hours.append(line.strip())

with open('courses/question_optional.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        question_optional.append(line.strip())
        
with open('courses/question_preq.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        question_preq.append(line.strip())

with open('courses/question_level.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        question_level.append(line.strip())

with open('courses/question_titles.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        question_titles.append(line.strip())        
        

for i in range(12):
    df_courses_dataset = pd.read_excel('courses/Courses_new.xlsx', sheet_name=i )
    df_courses_dataset = df_courses_dataset.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)
    

    df_courses_dataset= df_courses_dataset[df_courses_dataset["Level"] != "بدون مستوى"]
    df_courses_dataset["Level"].drop_duplicates()
    df_courses_dataset["Major"].drop_duplicates()

    # Iterate over Courses dataset (df_courses_dataset) to get course code
    for title in df_courses_dataset["Course Title"].sample(n=2, random_state=42): # to ensure reproducibility and balanced dataset, we specify n and random state.
        for ask in question_ask_codes:

            df_classifer_course_dataset.loc[len(df_classifer_course_dataset), 'query'] = f"{ask} {title}؟" # question mark must be arabic
            df_classifer_course_dataset.loc[len(df_classifer_course_dataset) - 1, 'size'] = "small" # question mark must be arabic

    for code in df_courses_dataset["Course Code"].sample(n=2, random_state=42):
        for ask in question_titles:

            df_classifer_course_dataset.loc[len(df_classifer_course_dataset), 'query'] = f"{ask} {code}؟" # question mark must be arabic
            df_classifer_course_dataset.loc[len(df_classifer_course_dataset) - 1, 'size'] = "small" # question mark must be arabic

    for title in df_courses_dataset["Course Title"].sample(n=2, random_state=42):
        for ask in question_hours:

            df_classifer_course_dataset.loc[len(df_classifer_course_dataset), 'query'] = f"{ask} {title}؟" # question mark must be arabic
            df_classifer_course_dataset.loc[len(df_classifer_course_dataset) - 1, 'size'] = "small" # question mark must be arabic

    for level, major in zip(df_courses_dataset["Level"].sample(n=2, random_state=42), df_courses_dataset["Major"].sample(n=2, random_state=42)):
        for ask in question_level:

            df_classifer_course_dataset.loc[len(df_classifer_course_dataset), 'query'] = f"{ask} {level} لتخصص {major}؟" # question mark must be arabic
            df_classifer_course_dataset.loc[len(df_classifer_course_dataset) - 1, 'size'] = "large" # question mark must be arabic
            
    for title in df_courses_dataset["Course Title"].sample(n=2, random_state=42):

        for ask in question_preq:
            question = f"{ask} {title}؟"
            df_classifer_course_dataset.loc[len(df_classifer_course_dataset), 'query'] = f"{ask} {title}؟" # question mark must be arabic
            df_classifer_course_dataset.loc[len(df_classifer_course_dataset) - 1, 'size'] = "small" # question mark must be arabic

    for major in df_courses_dataset["Major"].sample(n=2, random_state=42):

        for ask in question_optional:
            question = f"{ask} {major}؟"
            df_classifer_course_dataset.loc[len(df_classifer_course_dataset), 'query'] = f"{ask} {major}؟" # question mark must be arabic
            df_classifer_course_dataset.loc[len(df_classifer_course_dataset) - 1, 'size'] = "large" # question mark must be arabic

df_classifer_course_dataset["topic"] = "course"
df_classifer_course_dataset.drop_duplicates(subset=['query'], inplace=True)

# CONTINUE LATER TO ADD THE OTHER QUESTIONS (hours, level, optional, preq) IN THE SAME WAY.
# We need to specify only a specific number of rows like 5 or 10 and filter them by major to ensure dataset is balanced and not biased toward a specific major.
#----------------------------------Certifications section-----------------------------------#
df_classifer_cert_dataset= pd.DataFrame()
df_cert_dataset = pd.read_excel('certifications/Certifications.xlsx')
questions_ask_for_awarding = []
questions_ask_for_major = []
questions_other = []

df_cert_dataset = df_cert_dataset.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)


with open('certifications/questions_ask_for_awarding.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        questions_ask_for_awarding.append(line.strip())


with open('certifications/questions_ask_for_major.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        questions_ask_for_major.append(line.strip())


with open('certifications/questions_other.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        questions_other.append(line.strip())                


df_cert_dataset.dropna(inplace=True)
for_awarding_dataset = df_cert_dataset.drop_duplicates(subset=["Awarding Body"])
for_major_dataset = df_cert_dataset.drop_duplicates(subset=["Major"])

for award in for_awarding_dataset["Awarding Body"]:
    for ask in questions_ask_for_awarding:
        if "var" in ask:
            df_classifer_cert_dataset.loc[len(df_classifer_cert_dataset), 'query'] = ask.replace("var", award) + "؟" # question mark must be arabic
        
        else:
            df_classifer_cert_dataset.loc[len(df_classifer_cert_dataset), 'query'] = f"{ask} {award}؟" # question mark must be arabic

        df_classifer_cert_dataset.loc[len(df_classifer_cert_dataset) - 1, 'size'] = "large" # question mark must be arabic

for major in for_major_dataset["Major"]:
    for ask in questions_ask_for_major:
        if "var" in ask:
            df_classifer_cert_dataset.loc[len(df_classifer_cert_dataset), 'query'] = ask.replace("var", major) + "؟" # question mark must be arabic
    
        else:
            df_classifer_cert_dataset.loc[len(df_classifer_cert_dataset), 'query'] = f"{ask} {major}؟" # question mark must be arabic

        df_classifer_cert_dataset.loc[len(df_classifer_cert_dataset) - 1, 'size'] = "large" # question mark must be arabic


for other in questions_other:
    question = f"{other}؟"
    df_classifer_cert_dataset.loc[len(df_classifer_cert_dataset), 'query'] = f"{other}؟" # question mark must be arabic
    df_classifer_cert_dataset.loc[len(df_classifer_cert_dataset) - 1, 'size'] = "large" # question mark must be arabic

df_classifer_cert_dataset["topic"] = "certification"
df_classifer_cert_dataset.drop_duplicates(subset=['query'], inplace=True)

#----------------------------------General section-----------------------------------#
df_classifer_general_dataset= pd.DataFrame()
df_general_dataset = pd.read_excel('general/QA.xlsx')
df_general_dataset = df_general_dataset.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)


df_add_delete = df_general_dataset[df_general_dataset["Topic"].str.strip() == "الحذف والإضافة"]
df_graduation_project = df_general_dataset[df_general_dataset["Topic"].str.strip() == "مشروع التخرج"]
df_training = df_general_dataset[df_general_dataset["Topic"].str.strip() == "التدريب الصيفي التعاوني"]
df_clubs = df_general_dataset[df_general_dataset["Topic"].str.strip() == "الأندية الطلابية والأنشطة"]
df_other = df_general_dataset[df_general_dataset["Topic"].str.strip() == "أخرى"]

for question in df_add_delete["question"].sample(n=73, random_state=49):
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset), 'query'] = f"{question}" # question mark must be arabic
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset) - 1, 'size'] = "small" # question mark must be arabic


for question in df_graduation_project["question"].sample(n=73, random_state=49):
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset), 'query'] = f"{question}" # question mark must be arabic
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset) - 1, 'size'] = "small" # question mark must be arabic


for question in df_training["question"].sample(n=73, random_state=49):
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset), 'query'] = f"{question}" # question mark must be arabic
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset) - 1, 'size'] = "small" # question mark must be arabic


for question in df_clubs["question"].sample(n=15, random_state=49):
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset), 'query'] = f"{question}" # question mark must be arabic
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset) - 1, 'size'] = "small" # question mark must be arabic


for question in df_other["question"]:
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset), 'query'] = f"{question}" # question mark must be arabic
    df_classifer_general_dataset.loc[len(df_classifer_general_dataset) - 1, 'size'] = "small" # question mark must be arabic

df_classifer_general_dataset["topic"] = "general"

#----------------------------------Final section-----------------------------------#

def calculate_diff_range():
    maximum_rows_dataset = max(len(df_classifer_course_dataset), len(df_classifer_cert_dataset), len(df_classifer_general_dataset))
    
    if maximum_rows_dataset - len(df_classifer_course_dataset) not in range(10):
        print("Course dataset is inbalanced or the max dataset is too big compared to the others")

    elif maximum_rows_dataset - len(df_classifer_cert_dataset) not in range(10):
        print("Certification dataset is inbalanced or the max dataset is too big compared to the others")

    elif maximum_rows_dataset - len(df_classifer_general_dataset) not in range(10):
        print("General dataset is inbalanced or the max dataset is too big compared to the others")

    else:
        print("All datasets are balanced")

calculate_diff_range()

print(len(df_classifer_course_dataset))
print(len(df_classifer_cert_dataset))
print(len(df_classifer_general_dataset))

df_classifer_all_dataset = pd.concat([df_classifer_course_dataset, df_classifer_cert_dataset, df_classifer_general_dataset], ignore_index=True)

df_classifer_all_dataset["query"] = '\u202b' + df_classifer_all_dataset['query'] + '\u202c' # for RTL

df_classifer_all_dataset.to_excel('classifier_dataset2.xlsx', index=False)