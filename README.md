# Dalelk: The Official AI Academic Assistant for the College of Computer Science and Engineering for Jeddah University

```
.
├── classifier_training - This folder is responsible for training the intent classifier - the brain of Daleelak that understands what the user is asking about.
│   ├── certifications - Questions about certifications & datasets about certifications
│   └── courses - Questions about courses & datasets about courses
├── datasets 
│   ├── general - General dataset folder
│   ├── classifier_dataset.xlsx - The questions used to train the intent classifier
│   ├── create_dataset.py - A script that automatically generates dataset questions
│   ├── Evaluation_100.xlsx - Dataset for training/evaluation containing query, topic, size, and language
│   ├── Certifications.xlsx - Dataset about professional certifications
│   ├── Courses_new.xlsx - Dataset for the new course plan for the College of Computer Science and Engineering
│   ├── QA.xlsx - General academic Q&A dataset — includes COOP summer training questions, student clubs, and more
│   └── Students Survey.xlsx - Dataset built from real questions that students asked in the student survey — collected, answered, and structured into a dataset
├── frontend
│   ├── node_modules 
│   ├── public
│   ├── src
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── models
│   └── fine_tuned_marbert
├── unit testing
│   ├── main.py
│   ├── unit_test.py
│   └── unit_test_ratelimit.py
├── build_embeddings.py
├── data_loader.py
├── llm_inference.py
├── load_embeddings.py
├── logger.py
├── main.py
├── NOTICE.txt
├── query_classifier.py
├── query_classifier_training.ipynb
├── requirements.txt
├── retrieve.py
└── setup.py

```
