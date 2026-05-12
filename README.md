# Dalelk: The Official AI Academic Assistant for the College of Computer Science and Engineering for Jeddah University

```
 
.   
├── classifier_training/               # The brain that understands what the user is asking about
│   ├── certifications/                # Questions certifications folder
│   ├── courses/                       # Questions courses folder
│   ├── general/                       # Questions general folder
│   ├── classifier_dataset.xlsx        # Used to train the intent classifier
│   ├── create_dataset.py              # A script that automatically generates dataset questions
│   └── Evaluation_100.xlsx            # Dataset for training/evaluation
│
├── datasets/
│   ├── Certifications.xlsx            # Dataset about professional certifications
│   ├── Courses_new.xlsx               # Dataset for the new course plan
│   ├── QA.xlsx                        # General academic Q&A dataset
│   └── Students Survey.xlsx           # Dataset built from students questions
│
├── frontend/                          # Frontend website implementation with responsive UI and API integration
│   ├── public/
│   ├── src/                           # Main source code (components, pages, hooks)
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
│
├── models/                            # Trained AI models used by Dalelk
│   └── fine_tuned_marbert/            # Fine-tuned, trained on Dalelk's datasets
│
├── unit testing/                      # Backend API endpoint tests and rate limiting validation
│   ├── main.py
│   ├── unit_test.py
│   └── unit_test_ratelimit.py
│
├── build_embeddings.py
├── data_loader.py
├── llm_inference.py
├── load_embeddings.py
├── logger.py
├── main.py
├── NOTICE.txt
├── query_classifer.py
├── query_classifier_training.ipynb
├── requirements.txt
├── retrieve.py
└── setup.py


##  Getting Started

### 1. Get Your API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated API key
5. Paste it in the project where the API key is required

