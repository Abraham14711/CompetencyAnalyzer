import uuid
from competencyAnalyser.db.database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, text, Text, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


# Association Table for many-to-many relationship between
# Vacancy and BusinessType
VacancyBusinessType = Table(
    'vacancy_business_type',
    Base.metadata,
    Column('vacancy_id', UUID(as_uuid=True),
           ForeignKey('vacancies.id')),
    Column('business_type_id', UUID(as_uuid=True),
           ForeignKey('business_types.id'))
)


class User(Base):
    __tablename__ = 'users'
    telegram_id = Column(String(255), primary_key=True,
                         unique=True, nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    username = Column(String(255), nullable=False)
    photo_url = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)

    answers = relationship('Answer', backref='user',
                           uselist=False)


class Competency(Base):
    __tablename__ = 'competencies'
    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    title = Column(String(255), unique=True, nullable=False)

    question = relationship('Question', backref='competency',
                            uselist=False)


class Question(Base):
    __tablename__ = 'questions'
    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    competency_id = Column(UUID(as_uuid=True), ForeignKey('competencies.id'))
    content = Column(Text, nullable=False)
    answers = Column(Text, nullable=False)  # separated by &


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    user_id = Column(String(255), ForeignKey('users.telegram_id'))
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class BusinessType(Base):
    __tablename__ = 'business_types'
    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    title = Column(String(255), unique=True, nullable=False)


class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(UUID(as_uuid=True), primary_key=True,
                unique=True, nullable=False, default=uuid.uuid4)
    title = Column(String(255), unique=True, nullable=False)
    competencies = Column(Text, nullable=True)
    # competency.title, separated by &

    business_types = relationship('BusinessType',
                                  secondary=VacancyBusinessType,
                                  backref='vacancy')
