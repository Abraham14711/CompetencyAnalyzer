from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# Base schemas

class BusinessTypeBase(BaseModel):
    title: str = Field(..., max_length=255)


class VacancyBase(BaseModel):
    title: str


# Response schemas

class BusinessTypeOut(BusinessTypeBase):
    id: UUID
    vacancies: List['VacancyOut'] = []

    class Config:
        from_attributes = True


class VacancyOut(VacancyBase):
    id: UUID
    business_types: List[BusinessTypeOut] = []

    class Config:
        from_attributes = True


# Request schemas

class BusinessTypeCreate(BusinessTypeBase):
    pass


class BusinessTypeUpdate(BusinessTypeBase):
    title: Optional[str] = Field(None, max_length=255)


class VacancyCreate(VacancyBase):
    business_type_ids: List[UUID]


class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    business_type_ids: Optional[List[UUID]] = None


# Other schemas (Answer, User, Question, Competency)

# Answer schemas
class AnswerBase(BaseModel):
    content: str


class AnswerOut(AnswerBase):
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnswerCreate(AnswerBase):
    user_id: str
    created_at: datetime
    updated_at: datetime


class AnswerResponse(BaseModel):
    user_id: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnswerListResponse(BaseModel):
    status: str
    results: int
    answers: List[AnswerResponse]


class AnswerUpdate(BaseModel):
    content: Optional[str] = None
    updated_at: Optional[datetime] = None


# User schemas
class UserBase(BaseModel):
    telegram_id: str
    name: str
    email: EmailStr


class UserOut(UserBase):
    telegram_id: str
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    telegram_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None


# Question schemas
class QuestionBase(BaseModel):
    content: str


class QuestionOut(QuestionBase):
    id: UUID
    competency_id: UUID

    class Config:
        from_attributes = True


class QuestionCreate(QuestionBase):
    id: UUID
    competency_id: UUID


class QuestionUpdate(BaseModel):
    content: Optional[str] = None
    competency_id: Optional[UUID] = None


class QuestionResponse(BaseModel):
    id: UUID
    content: str
    competency_id: UUID

    class Config:
        from_attributes = True


# Competency schemas
class CompetencyBase(BaseModel):
    title: str


class CompetencyOut(CompetencyBase):
    id: UUID

    class Config:
        from_attributes = True


class CompetencyCreate(CompetencyBase):
    id: UUID


class CompetencyUpdate(BaseModel):
    title: Optional[str] = None
