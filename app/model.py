from sqlalchemy import (create_engine, Column, Integer, String,
                        Text, Boolean)
from sqlalchemy.orm import declarative_base, sessionmaker
engine = create_engine(
    "postgres://koyeb-adm:npg_Etdp5HAqB8iP@ep-red-wind-a2xnedrh.eu-central-1.pg.koyeb.app/koyebdb",
    echo=True
)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
db = SessionLocal()
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gmail = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    confirm_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True, autoincrement=True)
    your_name = Column(String, nullable=False, unique=True)
    gmail = Column(String, nullable=False, unique=True)
    subject = Column(String, nullable=False)
    message = Column(Text)


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String, nullable=False, unique=True)
    course_name = Column(String, nullable=False)
    about = Column(String, nullable=False)
    age_limit = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    course_id = Column(Integer, nullable=False)


class Teacher(Base):
    __tablename__ = "teachers"
    image = Column(String, nullable=False, unique=True)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)


class Blog(Base):
    __tablename__ = "blog"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String, nullable=False)
    about = Column(String, nullable=False)


Base.metadata.create_all(engine)
