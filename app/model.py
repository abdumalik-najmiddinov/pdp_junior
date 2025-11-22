from sqlalchemy import (create_engine, Column, Integer, String,
                        Text, Boolean)
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql://postgres:abdumalik@localhost:5432/postgres",
                       echo=True)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
db = Session()
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
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
