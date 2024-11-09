
# SANA Project

![GitHub repo size](https://img.shields.io/github/repo-size/abdulrahmansbq/sana-api)
![GitHub contributors](https://img.shields.io/github/contributors/abdulrahmansbq/sana-api)
![GitHub stars](https://img.shields.io/github/stars/abdulrahmansbq/sana-api?style=social)
![GitHub forks](https://img.shields.io/github/forks/abdulrahmansbq/sana-api?style=social)
![GitHub issues](https://img.shields.io/github/issues/abdulrahmansbq/sana-api)


Welcome to the GitHub repository of **SANA TEAM**, crafted for the **ALLAM** hackathon.

## Installation

SANA is built with two primary components:

1. FastAPI (Python) - A RESTful API that processes data with ALLAM LLM and interacts with the front-end. (Back-end)
2. Web Application (Laravel) - A web application that interacts with the API. (Front-end)

Follow these steps to set up the API:
### Prerequisites

Ensure you have Python installed on your machine. The project uses various Python packages, which can be installed via pip:

```bash
conda create -n sana python=3.11 
```

```bash
conda activate sana
```

```bash
pip install -r requirements.txt
```

### Setting Up

1. Clone the repository:
    ```bash
    git clone https://github.com/abdulrahmansbq/sana-api.git
    ```
2. Set up the API environment(Add openai api key in .env file):
    ```bash
    OPENAI_API_KEY=############
    WATSONX_APIKEY=############
    WATSONX_PROJECT_ID=############
    WATSONX_SPACE_ID=############
    LARAVEL_ENDPOINT="https://sanasa.xyz"
    LARAVEL_API_KEY=YOUR_LARAVEL_API_KEY
    ```
3. Run the server:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
4.  Now you should install the Laravel project to interact with the API.
5.  Clone the repository: https://github.com/hsndev18/sana_web For the web application.
    ```bash
    git clone https://github.com/hsndev18/sana_web
    ```
4. Set up the WepAPP Laravel environment:
    ```bash
    cd sana_web
    composer install
    ```
5. copy .env.example > .env
6. change database connection to your own connection with mysql
   ```php
    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_DATABASE=YOUR_DATABASE_NAME
    DB_USERNAME=YOUR_DATABASE_USERNAME
    DB_PASSWORD=YOUR_DATABASE_PASSWORD
    ```
7. run migration
    ```php
    php artisan migrate --seed
    ```
8. Run web app
   ```php
   php artisan serve
   php artisan horizon
   ```
9. Now you can access the web app from your browser.
10. Enjoy!

### Evaluation of Summarizing and Question Answer

## QAPromptAndEval.ipynb 
- This notebook includes the setup and evaluation process for generating and evaluating summaries and multiple-choice questions (MCQs) based on Arabic text content. Key components in this notebook include:

1. Text Preprocessing: Prepares the input Arabic text for effective summarization.
2. Summarization Prompt: Utilizes a prompt to condense Arabic text into concise summaries using specified parameters.
3. Question Generation Prompt: Formulates MCQs based on the summarized content with varying difficulty levels.
4. Evaluation Metrics: Measures the quality of summaries based on metrics like content preservation, linguistic integrity, and readability.
5. Detailed Score Analysis: Provides JSON-formatted evaluation results with scores for each generated question, including overall score, format, language, and option analysis.

## RAGEval.ipynb
- This notebook extends the evaluation capabilities with more advanced assessments and an integration of multiple models for Arabic text processing. It includes:

1. Model Setup: Configures and initializes two models (model_1 and model_2), which are used for generating responses based on specific parameters such as decoding_method, max_new_tokens, and repetition_penalty.
2. Embedding-Based Search (Proximity Search): A proximity search method that utilizes BERT embeddings for finding contextually similar answers within a dataset, enabling more accurate and relevant responses.
3. Prompt Construction: Constructs detailed prompts using predefined text inputs (prompt_input1 and prompt_input2) along with dynamically input questions, which are processed by the model to generate context-aware responses.
4. Output Evaluation: Evaluates and displays generated responses to validate the relevance and accuracy of answers produced by the models.

## Usage

Once the server is running, you can access the API endpoints from your Laravel application to interact with the allam and preprocess the data before sending it to the allam model.

## Team

- **Dr.Eid Albalawi** - Assistant Professor KFU, Team Leader
- **Ibrahim Alnabhan** - Data Analyst & Project Specialist
- **Abdulrahman Alsubayq** - Software Engineer & Cybersecurity Specialist
- **Hasan Alshikh** - Software Engineer & AI Engineer

## Acknowledgements

Thanks to all contributors and ALLAM organizers for the opportunity to develop this innovative solution.
