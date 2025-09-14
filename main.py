import argparse
from sqlalchemy.exc import SQLAlchemyError
from conf.db import session
from conf.models import Teacher, Group, Student, Subject, Grade
import random
from faker import Faker

fake = Faker()

# --- Teacher CRUD operations ---
def create_teacher(name):
    teacher = Teacher(fullname=name)
    session.add(teacher)
    session.commit()
    print(f"Teacher {name} created with ID {teacher.id}")

def list_teachers():
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(f"ID: {teacher.id}, Name: {teacher.fullname}")

def update_teacher(id, name):
    teacher = session.query(Teacher).filter_by(id=id).first()
    if teacher:
        teacher.fullname = name
        session.commit()
        print(f"Teacher ID {id} updated to {name}")
    else:
        print(f"Teacher with ID {id} not found")

def delete_teacher(id):
    teacher = session.query(Teacher).filter_by(id=id).first()
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"Teacher ID {id} deleted")
    else:
        print(f"Teacher with ID {id} not found")

# --- Group CRUD operations ---
def create_group(name):
    group = Group(name=name)
    session.add(group)
    session.commit()
    print(f"Group {name} created with ID {group.id}")

def list_groups():
    groups = session.query(Group).all()
    for group in groups:
        print(f"ID: {group.id}, Name: {group.name}")

def update_group(id, name):
    group = session.query(Group).filter_by(id=id).first()
    if group:
        group.name = name
        session.commit()
        print(f"Group ID {id} updated to {name}")
    else:
        print(f"Group with ID {id} not found")

def delete_group(id):
    group = session.query(Group).filter_by(id=id).first()
    if group:
        session.delete(group)
        session.commit()
        print(f"Group ID {id} deleted")
    else:
        print(f"Group with ID {id} not found")

# --- Student CRUD operations ---
def create_student(name, group_id):
    student = Student(fullname=name, group_id=group_id)
    session.add(student)
    session.commit()
    print(f"Student {name} created with ID {student.id}")

def list_students():
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.id}, Name: {student.fullname}, Group ID: {student.group_id}")

def update_student(id, name, group_id):
    student = session.query(Student).filter_by(id=id).first()
    if student:
        student.fullname = name
        student.group_id = group_id
        session.commit()
        print(f"Student ID {id} updated to {name}")
    else:
        print(f"Student with ID {id} not found")

def delete_student(id):
    student = session.query(Student).filter_by(id=id).first()
    if student:
        session.delete(student)
        session.commit()
        print(f"Student ID {id} deleted")
    else:
        print(f"Student with ID {id} not found")

# --- Subject CRUD operations ---
def create_subject(name, teacher_id):
    subject = Subject(name=name, teacher_id=teacher_id)
    session.add(subject)
    session.commit()
    print(f"Subject {name} created with ID {subject.id}")

def list_subjects():
    subjects = session.query(Subject).all()
    for subject in subjects:
        print(f"ID: {subject.id}, Name: {subject.name}, Teacher ID: {subject.teacher_id}")

def update_subject(id, name):
    subject = session.query(Subject).filter_by(id=id).first()
    if subject:
        subject.name = name
        session.commit()
        print(f"Subject ID {id} updated to {name}")
    else:
        print(f"Subject with ID {id} not found")

def delete_subject(id):
    subject = session.query(Subject).filter_by(id=id).first()
    if subject:
        session.delete(subject)
        session.commit()
        print(f"Subject ID {id} deleted")
    else:
        print(f"Subject with ID {id} not found")

# --- Grade CRUD operations ---
def create_grade(student_id, subject_id, grade, grade_date):
    grade = Grade(student_id=student_id, subject_id=subject_id, grade=grade, grade_date=grade_date)
    session.add(grade)
    session.commit()
    print(f"Grade for student ID {student_id} and subject ID {subject_id} created with ID {grade.id}")

def list_grades():
    grades = session.query(Grade).all()
    for grade in grades:
        print(f"ID: {grade.id}, Student ID: {grade.student_id}, Subject ID: {grade.subject_id}, Grade: {grade.grade}, Grade Date: {grade.grade_date}")

def update_grade(id, grade_value):
    grade = session.query(Grade).filter_by(id=id).first()
    if grade:
        grade.grade = grade_value
        session.commit()
        print(f"Grade ID {id} updated to {grade_value}")
    else:
        print(f"Grade with ID {id} not found")

def delete_grade(id):
    grade = session.query(Grade).filter_by(id=id).first()
    if grade:
        session.delete(grade)
        session.commit()
        print(f"Grade ID {id} deleted")
    else:
        print(f"Grade with ID {id} not found")

# --- Main function to parse arguments ---
def main():
    parser = argparse.ArgumentParser(description="Manage the database via CLI")
    parser.add_argument("-a", "--action", required=True, help="Action to perform", choices=["create", "list", "update", "remove"])
    parser.add_argument("-m", "--model", required=True, help="Model to manage", choices=["Teacher", "Group", "Student", "Subject", "Grade"])
    parser.add_argument("--id", type=int, help="ID of the record to update or delete")
    parser.add_argument("-n", "--name", type=str, help="Name of the teacher of the student or group or subject")
    parser.add_argument("--group_id", type=int, help="Group ID for student")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID for subject")
    parser.add_argument("--subject_id", type=int, help="Subject ID for grade")
    parser.add_argument("--grade", type=int, help="Grade value")
    parser.add_argument("--grade_date", type=str, help="Grade date")

    args = parser.parse_args()

    # Teacher operations
    if args.model == "Teacher":
        if args.action == "create" and args.name:
            create_teacher(args.name)
        elif args.action == "list":
            list_teachers()
        elif args.action == "update" and args.id and args.name:
            update_teacher(args.id, args.name)
        elif args.action == "remove" and args.id:
            delete_teacher(args.id)
        else:
            print("Invalid arguments for Teacher model")

    # Group operations
    elif args.model == "Group":
        if args.action == "create" and args.name:
            create_group(args.name)
        elif args.action == "list":
            list_groups()
        elif args.action == "update" and args.id and args.name:
            update_group(args.id, args.name)
        elif args.action == "remove" and args.id:
            delete_group(args.id)
        else:
            print("Invalid arguments for Group model")

    # Student operations
    elif args.model == "Student":
        if args.action == "create" and args.name and args.group_id:
            create_student(args.name, args.group_id)
        elif args.action == "list":
            list_students()
        elif args.action == "update" and args.id and args.name and args.group_id:
            update_student(args.id, args.name, args.group_id)
        elif args.action == "remove" and args.id:
            delete_student(args.id)
        else:
            print("Invalid arguments for Student model")

    # Subject operations
    elif args.model == "Subject":
        if args.action == "create" and args.name and args.teacher_id:
            create_subject(args.name, args.teacher_id)
        elif args.action == "list":
            list_subjects()
        elif args.action == "update" and args.id and args.name:
            update_subject(args.id, args.name)
        elif args.action == "remove" and args.id:
            delete_subject(args.id)
        else:
            print("Invalid arguments for Subject model")

    # Grade operations
    elif args.model == "Grade":
        if args.action == "create" and args.student_id and args.subject_id and args.grade and args.grade_date:
            create_grade(args.student_id, args.subject_id, args.grade, args.grade_date)
        elif args.action == "list":
            list_grades()
        elif args.action == "update" and args.id and args.grade:
            update_grade(args.id, args.grade)
        elif args.action == "remove" and args.id:
            delete_grade(args.id)
        else:
            print("Invalid arguments for Grade model")

if __name__ == "__main__":
    main()
