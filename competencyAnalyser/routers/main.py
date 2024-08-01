import json
from random import sample
import regex

import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette import status
from hcaptcha.hcaptcha import HCaptchaVerifier

from starlette.responses import JSONResponse, RedirectResponse

from competencyAnalyser.additional_scripts.main import flatten
from competencyAnalyser.scripts.ai import ai_analyze
from competencyAnalyser.scripts.mail import send_email
from competencyAnalyser.api import models
from competencyAnalyser.config import CAPTCHA_SECRET_KEY, templates
from competencyAnalyser.db.database import get_db
from competencyAnalyser.scripts.auth_functions import get_params

import logging

from competencyAnalyser.scripts.translator import TranslatorI18n
from competencyAnalyser.scripts.auth_functions import (check_authorized,
                                                       get_user_id)

from competencyAnalyser.scripts.auth_functions import send_telegram_message

logger = logging.getLogger(__name__)
logging.basicConfig(filename='main.log', level=logging.INFO)

router = APIRouter()

verifier = HCaptchaVerifier(CAPTCHA_SECRET_KEY)

app_language = "ru"


@router.get("/")
async def index():
    return RedirectResponse("/home", status_code=status.HTTP_302_FOUND)


@router.get("/home")
async def home(request: Request, db: Session = Depends(get_db)):
    vacancies = [
        [str(vacancy.id), vacancy.title]
        for vacancy in db.query(models.Vacancy).all()
    ]
    logger.info(f"Vacancies: {vacancies}")  # log vacancies (vacancies)
    main_translator = TranslatorI18n(app_language)
    context = {"request": request, "vacancies": vacancies,
               "translator": main_translator,
               "query_params": request.query_params}
    return templates.TemplateResponse("general_pages/index.html", context)


@router.get("/error")
async def error(request: Request):
    main_translator = TranslatorI18n(app_language)
    context = {"request": request, "translator": main_translator}
    return templates.TemplateResponse("general_pages/error.html", context)


@router.post("/set-locale", response_class=HTMLResponse)
async def set_locale(request: Request):
    global app_language
    form_data = await request.form()
    locale = form_data.get("locale")
    print(locale)

    if locale:
        request.state.locale = locale
    app_language = request.state.locale


@router.get("/quiz", response_class=HTMLResponse)
async def quiz(request: Request, db: Session = Depends(get_db)):
    main_translator = TranslatorI18n(app_language)
    buttons = request.query_params

    print("buttons", buttons.values())
    print("buttons keys", buttons.keys())
    print("raw buttons", buttons)
    res = ""
    for i in buttons["buttons"]:
        res += i
    vacancies = [vacancy for vacancy in res.split(",")]
    logger.info(f"Vacancies: {vacancies}")
    print(f"Vacancies: {vacancies}")

    competencies_list = (
        list(
            set(
                flatten(
                    list(
                        i[0].split("&")
                        for i in db.query(models.Vacancy.competencies).filter(
                            models.Vacancy.title.in_(vacancies)).all()
                    )
                )
            )
        )
    )

    logger.info(f"Competencies: {competencies_list}")
    print(f"Competencies: {competencies_list}")
    competencies_id_list = [_id[0] for _id in db.query(
        models.Competency.id).filter(
        models.Competency.title.in_(competencies_list)).all()]
    print(f"competencies_id_list: \n{competencies_id_list}")

    logger.info(f"Competencies ID: {competencies_id_list}")
    print(f"Competencies ID: {competencies_id_list}")

    questions = sample(
        list(
            [question[0], q_answers[0], i + 1]
            for i, (question, q_answers) in
            enumerate(
                zip(
                    db.query(models.Question.content).filter(
                        models.Question.competency_id.in_(
                            competencies_id_list)).all(),
                    db.query(models.Question.answers).filter(
                        models.Question.competency_id.in_(
                            competencies_id_list)).all()
                )
            )
        ),
        len(vacancies) * 4
    )

    logger.info(f"Questions: {questions}")
    print(f"Questions: {questions}")

    vacancies_str = ",".join(vacancies)

    logger.info(f"Vacancies string for query parameter: {vacancies_str}")
    print(f"Vacancies string for query parameter: {vacancies_str}")

    context = {"request": request,
               "picked_vacancies": vacancies_str,
               "questions": questions,
               "translator": main_translator}

    return templates.TemplateResponse("general_pages/quiz.html", context)


@router.post("/answers")
async def get_answers(request: Request, db: Session = Depends(get_db)):
    data = await request.form()
    logger.info(f"User answers: {data}")
    print(f"User answers: {data}")
    try:
        params = {
            "id": data["id"], "first_name": data["first_name"],
            "username": data["username"], "photo_url": data["photo_url"],
            "auth_date": data["auth_date"], "hash": data["hash"]
        }
    except:
        params = {}

    data = jsonable_encoder(data)
    name_data = data['pers_data']
    email = data['email']
    picked_vacancies = data['picked_vacancies'].split(",")
    data = list(data.items())

    if not regex.match(r"[^@]+@[^@]+\.[^@]+", email):
        return JSONResponse(status_code=400,
                            content={"message": "Invalid email format"})
    personal_data = {"name": name_data, "email": email}

    logger.info(f"Personal data: {personal_data}")
    print(f"Personal data: {personal_data}")

    form_questions = []
    form_answers = []

    if params == {}:
        for i in range(3, len(data)):
            form_questions.append(data[i][0])
            form_answers.append(data[i][1])

    else:
        for i in range(9, len(data)):
            form_questions.append(data[i][0])
            form_answers.append(data[i][1])

    competencies_id_list = [
        i[0] for i in
        db.query(models.Question.competency_id).filter(
            models.Question.content.in_(form_questions)).all()
    ]

    competencies = [competency[0] for competency_id in competencies_id_list
                    for competency in
                    db.query(models.Competency.title).filter(
                        models.Competency.id == competency_id).all()]

    vacancies = [vacancy[0] for vacancy in db.query(models.Vacancy.title).all()]

    ai_answer = ai_analyze(questions=form_questions, answers=form_answers,
                           competencies=competencies, vacancies=vacancies,
                           picked_vacancies=picked_vacancies,
                           language=app_language)

    if params != {} and check_authorized(params):
        user_id = get_user_id(params)
        send_telegram_message(user_id, ai_answer)

    send_email(email, personal_data, ai_answer)
    logger.info("Email sent successfully!")
    logger.info(f"AI answer: {ai_answer}")
    logger.info("Personal data: " + str(personal_data))
    logger.info("Questions: " + ",".join(form_questions))
    logger.info("Answers: " + ",".join(form_answers))
    logger.info("Picked vacancies: " + str(picked_vacancies))
    logger.info("Competencies: " + str(competencies))
    logger.info("Vacancies: " + str(vacancies))
    print("Email sent successfully!")
    print(f"AI answer: {ai_answer}")
    print("Personal data: " + str(personal_data))
    print("Questions: " + ",".join(form_questions))
    print("Answers: " + ",".join(form_answers))
    print("Picked vacancies: " + str(picked_vacancies))
    print("Competencies: " + str(competencies))
    print("Vacancies: " + str(vacancies))

    content = json.dumps({
        "answers": {form_questions[question_index]: form_answers[question_index]
                    for question_index in range(len(form_questions))},
        "AI answer": ai_answer,
        "picked vacancies": picked_vacancies,
        "competencies to check": competencies
    }, ensure_ascii=False)

    logger.info("Content: " + content)
    print("Content: " + content)

    user = params

    logger.info("User: " + str(user))
    print("User: " + str(user))

    if params != {} and check_authorized(user):
        user_query = db.query(models.User).filter(
            models.User.telegram_id == get_user_id(user)).first()

        if user_query is None:
            # Save personal data to DB
            if "first_name" not in user.keys():
                user['first_name'] = personal_data['name'].split()[0]
            if "last_name" not in user.keys():
                if len(personal_data['name'].split()) > 1:
                    user['last_name'] = personal_data['name'].split()[1]
                else:
                    user['last_name'] = ""
            new_user = models.User(
                telegram_id=get_user_id(user),
                first_name=user['first_name'],
                last_name=user['last_name'],
                username=personal_data['name'],
                photo_url=user['photo_url'],
                email=personal_data['email']
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

        # Save answers to DB
        new_answer = models.Answer(
            user_id=get_user_id(user), content=content
        )
        db.add(new_answer)
        db.commit()
        db.refresh(new_answer)

    return fastapi.responses.RedirectResponse(
        '/answers?' + ai_answer,
        status_code=status.HTTP_302_FOUND)


@router.get("/answers")
async def answers(request: Request):
    answer = ""
    for i in request.query_params:
        answer += i

    main_translator = TranslatorI18n(app_language)
    context = {
        "request": request,
        "answer": answer,
        "translator": main_translator
    }

    return templates.TemplateResponse("general_pages/results.html", context)


@router.get("/authorize_user")
async def authorize_user(request: Request):
    main_translator = TranslatorI18n(app_language)
    context = {
        "request": request,
        "translator": main_translator
    }

    if check_authorized(dict(list(request.query_params.items()))):
        redirect_url = "https://competency.jobster.uz/home"

        query_params = request.query_params
        if query_params:
            redirect_url += "?" + "&".join(
                f"{key}={value}" for key, value in query_params.items())

        return RedirectResponse(url=redirect_url, status_code=302)

    return templates.TemplateResponse("general_pages/user_auth.html", context)


@router.get("/.env")
async def env_reach(request: Request):
    main_translator = TranslatorI18n(app_language)
    context = {
        "request": request,
        "translator": main_translator
    }
    return templates.TemplateResponse("general_pages/env_reach.html", context)
