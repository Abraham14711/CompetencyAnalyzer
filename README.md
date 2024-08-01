# The AI-Based Competency Assessment Tool

Welcome to The AI-Based Competency Assessment Tool! This web application is designed to evaluate and enhance individual competencies such as accountability, adaptability, and ambition. By generating customized tests and utilizing a vast database of interview questions and situational tests, the tool offers tailored assessments and adaptive testing. It employs AI to provide automated scoring, detailed reports, and benchmarking against industry standards. Users receive personalized improvement plans with actionable advice, tailored development activities, and targeted coaching tips. The intuitive dashboard ensures easy navigation and mobile compatibility, while robust security measures protect user data. Built with PostgreSQL, FastAPI, and OpenAI solution Chat GPT-3.5 turbo for the AI, the tool is hosted on the cloud aiming to deliver precise, actionable insights to help users achieve their full potential.

This README will guide you through the process of cloning the repository, installing dependencies, and running the application.

## Table of Contents

- [License](#license)
- [Images](#images)
- [Tools](#tools)
- [Telegram bot](#telegram-bot)
- [Contributing](#contributing)
- [Prerequisites](#prerequisites)
- [Cloning the Repository](#cloning-the-repository)
- [Installing Dependencies](#installing-dependencies)
- [Running the Application](#running-the-application)
- [Presentation](#presentation)

## License

For our project we have MIT LICENSE, here reference:

https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/blob/main/LICENSE

## Images

<img src="https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/raw/assets/Main%20page.PNG" width="650" align="center">


<center> Start page </center>


<img src="https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/raw/assets/Choosing.PNG" width="650" align="center">


<center> Here you can choose vacancies </center>

<img src="https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/raw/assets/Start%20quiz.PNG" width="650">


<center> Here you need to write your full name and email </center>


<img src="https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/raw/assets/QuizPNG.PNG" width="650">


<center> Quiz in proccess </center>
<img src="https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/raw/assets/ResultsPNG.PNG" width="650" align="center">


<center> Here you can see your results </center>

## Tools

1) AI tools:
    - OpenAI
2) Backend tools:
    - Python
    - Alembic
    - PostgreSQL/SQLAlchemy
    - Pydantic
    - FastAPI
    - Jinja2Templates
    - Poetry
    - Uvicorn
    - Flake8
    - Pytest
    - Pytest-cov
    - Statlette
    - Dotenv
    - Os
3) DevOps tools:
    - CI/CD
    - Docker
    - Git, GitHub, GitFlow, GitHub Actions, GitLab
    - Nginx
    - Bash
4) Frontend tools:
    - HTML
    - CSS
    - JavaScript
    - Bootstrap5
5) CS tools:
    - Naxi
    - Fail2ban
    - Iptables
    - Let's encrypt/certbot

## Telegram bot

In addition to our website, our product has a Telegram bot which allows users to access the website via WebApp.

Link to the bot (for start you need to write "/start"):

https://t.me/competency_analyser_bot

## Contributing
Contributions are always welcome! To contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes.
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature-branch).
- Open a pull request.

Please ensure your pull request adheres to the following guidelines:

1. Describe the changes in detail.
2. Include any relevant screenshots or code samples.
3. Ensure that the code is properly formatted and free of any linting errors. (You can use our CI/CD pipeline with lint checking)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed [Docker](https://www.docker.com/get-started/)
- You have contacted with main developers for setting up environment variables.

## Cloning the Repository

To clone the repository, follow these steps:

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to clone the project.
3. Run the following command:

    ```sh
    https://gitlab.pg.innopolis.university/d.tskhe/swp-project
    ```

4. Navigate to the project directory:

    ```sh
    cd swp-project
    ```

## Run the application and telegram bot locally

To install the required dependencies, run the following command in the project directory:

```sh
docker compose up --build -d
```

## Presentation
https://docs.google.com/presentation/d/1DnRGGPQJsbGHxRvMXOcbendTPQqKEZS8iNoGTdgIUJ4/edit?usp=sharing
