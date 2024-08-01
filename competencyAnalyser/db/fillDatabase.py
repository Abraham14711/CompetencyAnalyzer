# -*- coding: utf-8 -*-

from competencyAnalyser.db.database import get_db

from competencyAnalyser.constants import FILE_PATH, FILE_PATH_2, FILE_PATH_3
from competencyAnalyser.api.models import Competency, Question, Vacancy
from competencyAnalyser.api.models import BusinessType

from competencyAnalyser.scripts.ai import generate_answers_to_pick


# Filling database with questions and competencies from file
def fill_qc(db):
    print("Filling database with questions and competencies from file")
    with open(FILE_PATH, 'r', encoding="utf-8") as f:
        data = f.read()
    chunks = data.split("&")

    for chunk in chunks:
        competency, _questions = chunk.split("=")
        questions_list = _questions.split(";")

        # Check if the competency already exists in the database
        competency_query = db.query(Competency).filter_by(
            title=competency)
        existing_competency = competency_query.first()

        if not existing_competency:
            new_competency = Competency(title=competency)
            db.add(new_competency)
            db.commit()
            db.refresh(new_competency)
        else:
            new_competency = existing_competency

        # check if the question already exists in the database

        for question in questions_list:
            if not question.strip():  # Skip empty lines
                continue
            question_query = db.query(Question).filter_by(
                content=question)
            existing_question = question_query.first()
            if not existing_question:
                new_question = Question(
                    content=question, competency_id=new_competency.id,
                    # answers="test1&test2&test3",
                    answers=generate_answers_to_pick(question),
                )
                db.add(new_question)
                db.commit()
                db.refresh(new_question)


# Filling database with vacancies and competencies from file
def fill_vc(db):
    print("Filling database with vacancies and competencies from file")
    with open(FILE_PATH_3, 'r', encoding="utf-8") as f:
        data = f.read()
    chunks = data.split(";")

    for chunk in chunks:
        if not chunk.strip():  # Skip empty lines
            continue

        parts = chunk.split(":")
        vacancy_title, competencies_list = parts

        # Check if the vacancy already exists in the database
        vacancy_query = db.query(Vacancy).filter_by(title=vacancy_title)
        existing_vacancy = vacancy_query.first()

        if not existing_vacancy:
            new_vacancy = Vacancy(title=vacancy_title,
                                  competencies=competencies_list)
            db.add(new_vacancy)
            db.commit()
            db.refresh(new_vacancy)
        else:
            existing_vacancy.competencies = competencies_list


# Filling database with business types and vacancies from file
def fill_vb(db):
    print("Filling database with vacancies and business types from file")
    with open(FILE_PATH_2, 'r', encoding="utf-8") as f:
        data = f.read()
    chunks = data.split(";")

    for chunk in chunks:
        if not chunk.strip():  # Skip empty lines
            continue

        parts = chunk.split(":")
        vacancy_title = parts[0].strip()
        business_types_list = [b.strip()
                               for b in parts[1:]
                               if b.strip()]

        # Check if the vacancy already exists in the database
        vacancy = db.query(Vacancy).filter_by(title=vacancy_title).first()

        # Associate business types with the vacancy
        for business_type_title in business_types_list:
            existing_business_type = db.query(BusinessType).filter_by(
                title=business_type_title).first()

            new_business_type = existing_business_type
            if not existing_business_type:
                new_business_type = BusinessType(
                    title=business_type_title
                )
                db.add(new_business_type)
                db.commit()
                db.refresh(new_business_type)

            # Associate business type with the vacancy
            if new_business_type not in vacancy.business_types:
                vacancy.business_types.append(new_business_type)

            db.commit()
            db.refresh(vacancy)


def fill_initial_db():
    db = next(get_db())

    fill_qc(db)
    fill_vc(db)
    fill_vb(db)
