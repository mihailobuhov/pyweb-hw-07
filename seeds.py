import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Group, Student, Subject, Grade

fake = Faker()


def insert_groups():  # Додавання груп
    for _ in range(3):
        group = Group(
            name=fake.word()
        )
        session.add(group)


def insert_teachers():  # Додавання викладачів
    for _ in range(3):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.add(teacher)


def insert_subjects():  # Додавання предметів із вказівкою викладача
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        for _ in range(2):
            subject = Subject(
                name=fake.word(),
                teacher=teacher
            )
            session.add(subject)


def insert_students_and_grades():
    groups = session.query(Group).all()
    subjects = session.query(Subject).all()

    for group in groups:
        for _ in range(10):
            student = Student(
                fullname=fake.name(),
                group=group
            )
            session.add(student)
            session.flush() # Зберігаємо студента, щоб отримати його ID

            for subject in subjects:
                for _ in range(3):
                    grade = Grade(
                        grade=random.randint(1, 100),
                        grade_date=fake.date_this_decade(),
                        student_id=student.id,
                        subject_id=subject.id
                    )
                    session.add(grade)


if __name__ == '__main__':
    try:
        insert_groups()
        insert_teachers()
        insert_subjects()
        insert_students_and_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
