from datetime import datetime, timezone

from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from competencyAnalyser.api import models
from competencyAnalyser.config import templates, whiteList
from fastapi import APIRouter

from competencyAnalyser.db.database import get_db
from competencyAnalyser.routers.main import app_language
from competencyAnalyser.scripts.ai import generate_user_description
from competencyAnalyser.scripts.translator import TranslatorI18n
from competencyAnalyser.scripts.auth_functions import check_authorized, \
    get_params

from competencyAnalyser.scripts.verifyTheHash import \
    verify_telegram_authentication

router = APIRouter()


@router.get("/auth")
async def auth(request: Request):
    main_translator = TranslatorI18n(app_language)
    context = {
        "request": request,
        "translator": main_translator,
        "auth_page": "auth",
    }

    data = dict(list(request.query_params.items()))
    print(data)

    if data:
        unix_time = datetime.now(timezone.utc).timestamp()
        print("DATA IN WELCOME", data)
        print("UNIX TIME", unix_time)

        if (data["id"] not in whiteList or
                unix_time - float(data["auth_date"]) > 3600 or not
                verify_telegram_authentication(data)):
            return templates.TemplateResponse(
                "general_pages/error.html", {
                    "request": request,
                    "translator": main_translator
                })
        else:
            redirect_url = "https://competency.jobster.uz/hr/show_users"

            query_params = request.query_params
            if query_params:
                h = [f"{key}={value}" for key, value in query_params.items()]
                redirect_url += "?" + "&".join(h)

            return RedirectResponse(url=redirect_url, status_code=302)

    return templates.TemplateResponse("general_pages/auth_page.html", context)


@router.get("/show_users", response_class=HTMLResponse)
async def show_users(request: Request):
    data = request.query_params
    params = get_params(data)

    db = next(get_db())

    users_query = db.query(models.User).all()

    print(users_query)

    users = []
    for user in users_query:
        user_answers = [i[0] for i in db.query(models.Answer.content).filter(
            models.Answer.user_id == user.telegram_id
        )]
        users.append({
            "id": user.telegram_id,
            "name": user.username,
            "description": generate_user_description(
                "; ".join(user_answers),
            )
        })

    if not check_authorized(params):
        return RedirectResponse("/hr/auth")
    else:
        main_translator = TranslatorI18n(app_language)
        context = {
            "request": request,
            "translator": main_translator,
            "users": users
        }

        return templates.TemplateResponse("general_pages/show_users.html",
                                          context)
