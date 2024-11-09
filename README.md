
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
5.  Clone the repository:
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
    
## Usage

Once the server is running, you can access the API endpoints from your Laravel application to interact with the allam and preprocess the data before sending it to the allam model.

## Team

- **DR.Eid Albalawi** - Assistant Professor KFU, Team Leader
- **Ibrahim Alnabhan** - Data Analyst & Project Specialist
- **Abdulrahman Alsubayq** - Software Engineer & Cybersecurity Specialist
- **Hasan Alshikh** - Software Engineer & AI Engineer

## Acknowledgements

Thanks to all contributors and ALLAM organizers for the opportunity to develop this innovative solution.
