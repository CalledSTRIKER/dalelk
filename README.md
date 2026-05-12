# Dalelk: The Official AI Academic Assistant for the College of Computer Science and Engineering for Jeddah University

```
 
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
├── build_embeddings.py                # bulid embeddings for dataset
├── data_loader.py                     # loading and preparing all the datasets into the program
├── llm_inference.py                   # communicating with the LLM to generate the final answer for the user.
├── load_embeddings.py                 
├── logger.py                          # Loading everything that happens in the program
├── main.py                            # the entry point of Dalelk where everything starts and comes together.
├── NOTICE.txt                         # google policy
├── query_classifer.py                 # The query classifier that analyze the user's intent
├── query_classifier_training.ipynb    # Jupyter Notebook where the MARBert model was trained and fine-tuned.
├── requirements.txt                   # lists all the Python libraries that Dalelk needs to run.
├── retrieve.py                        # finding the most relevant information to answer the user's question.
└── setup.py                           # packaging and setting up Dalelk as a Python project.
```

##  Getting Started

### 1. Get Your Google API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **"Get API Key"**
4. Click **"Create API Key"**
5. Choose your project
6. Copy the generated API key
7. Paste it in the project in the .env file in the API_KEY1 field.


### 2. Get Your Hugging Face API Key
1. Go to [Hugging Face](https://huggingface.co/)
2. Sign in with your account
3. Go to [Embedding Gemma](https://huggingface.co/google/embeddinggemma-300m) and accept the usage policy
4. Click on your profile picture → **"Settings"**
5. Go to **"Access Tokens"**
6. Click **"New Token"**
7. Give it a name and set access to **"Read"**
8. Click **"Create Token"**
9. Copy the generated token
10. Paste it in the project in the .env file in the hf_token field.


### 3. Download the Classifier Model
1. Go to the **Releases** page of this repository
2. Download the classifier model file
3. Place it inside the `models/` folder

### 4. Extract the Model
1. Extract the downloaded file
2. Make sure the extracted content follows this exact path:
>  !!! **Windows users:** !!! When extracting, make sure the final path looks like this and does not have an extra folder:
> `models/fine_tuned_marbert/(model files directly here)`
