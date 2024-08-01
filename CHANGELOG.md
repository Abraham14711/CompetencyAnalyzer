# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]

- FrontEnd:
    - Make profile page to help HR's see information about questionaries passed by candidates (users)
- Backend:
    - Database:
        - Rebase answers and users models
    - Admin Panel:
        - Integrate FastAPI Amis Admin Panel into project
        - Add all models to Admin Panel
        - Fix some frontend issues
    - Questions:
        - Add multiple choice answers
        - Create new AI functions that will generate answers based on given question
        - Generate 3 questions with multiple choice type and one full answer
- DevOPS:
    - Make separate container and environment for telegram bot
    - Dockerize nginx

## [0.4] - 2024-07-12

### Added

- Gitlab CI/CD:
    - Linting via flake8

- Docker configured and some migrations on models
- Publishment of working docker images to docker hub
- Deployment of project on the Debian server via Docker
- HR page with information about user's passed quizes
- Whitelist for HR's

### Changed

- Frontend captcha

### Fixed

- Timeout of waiting answer from backend
- Forms validation
- Minimal changes for frontend captcha
- Over hundred lint errors has been fixed
- Tests for database with mock database

### Security

- Minimal changes for frontend captcha

## [0.3] - 2024-07-09

### Added

- Gitlab CI/CD:
    - Great gitlab CI/CD configuration
    - Connection to deployment server via SSH
    - Testing via pytest
- Tests of database using real postgres database
- Adaptive Frontend features
- Validation of forms
- Logo in the header
- Telegram authorization
- Filling database on its creation
- Parsing from files to fill database
- Page for errors
- UI design
- Redirection to HR page after authorization via telegram
- GitFlow integration

### Changed

- README file
- HR page
- Alembic configuration and migrations

### Deprecated

- Google authorization

### Removed

- Google authorization
- Parsing router

### Fixed

- Using wrong version of AI
- Some models and schemas
- Some tests
- Main routing
- Mail service
- Tests for API
- Models, schemas and routers functions
- Error Page Problem for HR Auth

### Security

- Cloudflare checkbox

## [0.2] - 2024-07-04

### Added

- AI function that analyze user answers and rate them
- CI/CD base configuration (not really working)
- Mail delivery with results of passing quiz
- Validation of email via regular expressions
- Telegram Bot using WebApp
- Saving personal data of user in database
- Saving answers in database
- Saving AI answer in database
- AI now consider list of all vacancies

### Changed

- .gitignore file
- API of some models
- Columns of answers model
- Columns of questions model
- Table business_types 

### Removed

- .env file from tracking by git

### Fixed

- Frontend css and js logic of header was replaced with bootstrap solution
- AI function prompt improved
- .idea/ git ignoring
- Minor bags in main (index) page related to the text
- Answers page
- Fails with mail sending configuration

## [0.1] - 2024-06-22

### Added

- API:
    - CRUD functions for questions
    - CRUD functions for answers
    - CRUD functions for competencies
    - CRUD functions for business_types
    - CRUD functions for users

- Alembic migrations
- HTML files for auth
- Added .env to gitignore
- Added MIT License
- Dockerfile and docker compose for database configured
- Added Postges docker image to the project
- Authentification for hr's via google

### Security
- Added nginx with opensource firewall Naxsi to prevent different types of injections and opensource tool Fail2ban to prevent DDOS and DOS.

## [0.0.1] - 2024-06-11

- initial release

<!-- Links -->
[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html

<!-- Versions -->
[unreleased]: https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/compare/v0.1...main?from_project_id=1071&straight=false
[0.4]: https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/tags/v0.4
[0.3]: https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/tags/v0.3
[0.2]: https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/tags/v0.2
[0.1]: https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/tags/v0.1
[0.0.1]: https://gitlab.pg.innopolis.university/d.tskhe/swp-project/-/commit/cb10e000a930fc23af254496108d25efbbffa5e9