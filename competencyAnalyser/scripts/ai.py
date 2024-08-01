from fastapi import APIRouter
from openai import OpenAI
from starlette.staticfiles import StaticFiles

from competencyAnalyser.config import API_KEY

router = APIRouter()
client = OpenAI(api_key=API_KEY)
router.mount("/static", StaticFiles(directory="static"), name="static")

# Словарь для хранения инструкций на разных языках
instructions = {
    "ru": {
        "system": "Ты система, оценивающая компетенции человека по шкале от 1 "
                  "до 5 в зависимости от его ответов на представленные "
                  "вопросы, и предоставляющая вакансии, которые подходят "
                  "этому кандидату. По вопросам ниже тебе нужно оценить "
                  "компетенции, нужные для вакансий, которые кандидат выбрал. "
                  "Оценки тебе нужно вывести в столбик (каждую с новой "
                  "строки) без лишних подробностей (только название "
                  "компетенции и оценку от 1 до 5). Твой ответ должен "
                  "содержать только компетенцию и оценку от 1 до 5, "
                  "без объяснений и подробностей. Выдавай весь своей ответ на "
                  "русском языке.",
        "user": "После этого в соответствие оценкам компетенций, которые ты "
                "дал кандидату по его ответам, выбери, какие вакансии "
                "подходят кандидату, учитывая вакансии которые он выбрал "
                "изначально сам. Выбирай не только из тех вакансий, "
                "которые выбрал кандидат, но и смотри также все остальные "
                "вакансии из списка. Выбери не больше 4 вакансий."
                "Твой ответ должен содержать только список из "
                "оценок компетенций и список из названий вакансий."
                "Если за большую часть"
                "компетенций у человека оценка 1, то не выдавай ему вакансий."
                "Выдавай весь своей ответ на русском языке."
    },
    "en": {
        "system": "You are a system that evaluates a person's competencies on "
                  "a scale from 1 to 5 based on their answers to the given "
                  "questions, and provides job positions suitable for this "
                  "candidate. For the questions below, you need to evaluate "
                  "the competencies required for the job positions the "
                  "candidate has chosen. The ratings should be output in a "
                  "column (each on a new line) without any extra details ("
                  "just the competency name and the rating from 1 to 5). Your "
                  "response should contain only the competency and the rating "
                  "from 1 to 5, without explanations and details. Give your "
                  "entire answer in English.",
        "user": "After that, according to the competency ratings you gave the "
                "candidate based on their answers, choose which job positions "
                "are suitable for the candidate, considering the positions "
                "they initially selected themselves. Not only choose from the "
                "jobs"
                "that the candidate has chosen, but also look at all the "
                "other jobs on the list. Choose not more than 4 vacancies."
                "Your response should contain only a list of competency "
                "ratings and a list of job"
                "titles. If a person scores 1 on most of the "
                "competencies, don't give them jobs."
                "Give your entire answer in English."
    }
}


def ai_analyze(questions: list, competencies: list, answers: list,
               vacancies: list, picked_vacancies: list, language: str = 'ru'):
    examples = open("static/examples.txt", 'r', encoding="utf-8").read()
    examples_en = open("static/examples_en.txt", 'r', encoding="utf-8").read()

    assist = {
        "ru":
            f"Примеры правильного поведения: {examples}"
            f"Список вакансий, выбранных кандидатом: {picked_vacancies}"
            f"Список всех вакансий: {vacancies}",
        "en":
            f"Examples of right behaviour: {examples_en}"
            f"List of all vacancies: {vacancies}"
            f"List of vacancies selected by the candidate: {picked_vacancies}"
    }

    string = {
        "ru": "".join(list(
            f"Отталкиваясь от вопроса и ответа на него кандидата ниже, "
            f"оцени его"
            f"{competencies[i]}: Вопрос: {questions[i]}\nОтвет кандидата:"
            f"{answers[i]}."
            for i in range(len(questions)))),
        "en": "".join(list(
            f"Basing on the question and the candidate's answer below,"
            f"assess the candidate's "
            f"{competencies[i]}: Question: {questions[i]}"
            f"\nCandidate's answer: {answers[i]}."
            for i in range(len(questions))))
    }

    system_instruction = instructions[language]["system"]
    user_instruction = instructions[language]["user"]
    assistant_instruction = assist[language]
    string_str = string[language]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": string_str},
            {"role": "assistant", "content": assistant_instruction},
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_instruction}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


def generate_answers_to_pick(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """
            Тебе нужно генерировать ответы на вопросы в следующем формате:
            ответы должны быть разделены знаком "\\n". Например,
            <ответ1>\\n<ответ2>\\n<ответ3>\\n<ответ4>
            Ты система, которая генерирует 
          ответы на вопрос. На вход тебе приходит вопрос и ты должна дать 4 
          возможных варианта ответа, как бы могли ответить на это вопрос 
          опрашиваемые. Представь, что на первый вопрос ты отвечаешь как 
          беззаботный и безответственный человек, на второй как только 
          начавший работать человек, который не имеет большого опыта; на 
          третий как человек, который уже много лет работает, но еще не стал 
          большим профессионалом своего дела; и на четвертый, как человек 
          профессионал, который очень ответственный и управляет людьми"""},
            {"role": "user",
             "content": f"Сгенерируй 4 возможных варианта ответа на следующий "
                        f"вопрос: {question}"},
            {"role": "assistant",
             "content": """Ты готовишь ответы на вопросы в соответствии
             с указанным форматом:
             ответы должны быть разделены знаком "\\n".
             Например, <ответ1>\\n<ответ2>\\n<ответ3>\\n<ответ4>"""
             }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


def ai_translate_text(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """Ты переводчик с одного заданного 
            языка на другой. Если текст на русском языке, переведи его на 
            английский, а если он на английском,
            то переведи его на русский."""},
            {"role": "user",
             "content": "Если текст ниже на русском языке, то переведи его на "
                        "английский, а если он на английском,"
             f"то переведи его на русский. Переведи этот текст: {text}."
                        f"В ответе должен быть только переведённый текст."},
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


def generate_user_description(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """Ты система, которая генерирует 
            описание для профиля пользователя отталкиваясь от его оценок по 
            различным компетенциям. Тебе нужно написать, какими качествами 
            обладает пользователь в зависимости от его компетенций и оценкам 
            по ним, где 1- плохо, а 5- прекрасно. """},
            {"role": "user",
             "content": f"В зависимости от компетенций и "
             f"оценкам по ним у кандидаты, напиши ему описание профиля: {text}"}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
