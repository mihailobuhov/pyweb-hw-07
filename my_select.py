from sqlalchemy import func, desc, select, and_, distinct

from conf.models import Grade, Teacher, Student, Subject, Group
from conf.db import session


def select_01():  # Знайти 5 студентів із найбільшим середнім балом з усіх предметів
    """
    SELECT
        s.id AS student_id,
        s.fullname AS student_name,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """

    result = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname.label("student_name"),
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Student)
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(5)
        .all()
    )

    return result


def select_02():  # Знайти студента із найвищим середнім балом з певного предмета
    """
    SELECT
        s.id AS student_id,
        s.fullname AS student_name,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    WHERE g.subject_id = 3  -- Предмет, з якого ви хочете знайти середній бал
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """

    result = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname.label("student_name"),
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .filter(Grade.subject_id == 3)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(1)
        .all()
    )

    return result


def select_03():  # Знайти середній бал у групах з певного предмета
    """
    SELECT
        gr.name AS group_name,
        sb.name AS subject,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM groups gr
    JOIN students s ON gr.id = s.group_id
    JOIN grades g ON s.id = g.student_id
    JOIN subjects sb ON sb.id = g.subject_id
    WHERE sb.id = 3  -- Предмет, з якого ви хочете знайти середній бал
    GROUP BY gr.name, sb.name
    ORDER BY average_grade DESC;
    """

    result = (
        session.query(
            Group.name.label("group_name"),
            Subject.name.label("subject"),
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(Subject.id == 3)
        .group_by(Group.name, Subject.name)
        .order_by(desc("average_grade"))
        .all()
    )
    return result


def select_04():  # Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    SELECT ROUND(AVG(grade), 2) AS average_grade
    FROM grades;
    """

    result = (
        session.query(func.round(func.avg(Grade.grade), 2).label("average_grade"))
        .select_from(Grade)
        .all()
    )
    return result


def select_05():  # Знайти які курси читає певний викладач.
    """
    SELECT
        t.id AS teacher_id,
        t.fullname AS teacher,
        sb.name AS subject
    FROM teachers t
    JOIN subjects sb ON t.id = sb.teacher_id
    WHERE t.id = 3;
    """

    result = (
        session.query(
            Teacher.id.label("teacher_id"),
            Teacher.fullname.label("teacher"),
            Subject.name.label("subject"),
        )
        .select_from(Teacher)
        .join(Subject)
        .filter(Teacher.id == 3)
        .all()
    )
    return result


def select_06():  # Знайти список студентів у певній групі.
    """
    SELECT
        s.id AS student_id,
        s.fullname AS student_name,
        gr.name AS group_name
    FROM groups gr
    JOIN students s ON gr.id = s.group_id
    WHERE gr.id = 3
    ORDER BY s.id ASC;
    """

    result = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname.label("student_name"),
            Group.name.label("group_name"),
        )
        .select_from(Group)
        .join(Student)
        .filter(Group.id == 3)
        .order_by(Student.id.asc())
        .all()
    )

    return result


def select_07():  # Знайти оцінки студентів у окремій групі з певного предмета.
    """
    SELECT
        s.id AS student_id,
        s.fullname AS student_name,
        gr.name AS group_name,
        sb.name AS subject,
        g.grade
    FROM groups gr
    JOIN students s ON gr.id = s.group_id
    JOIN grades g ON s.id = g.student_id
    JOIN subjects sb ON sb.id = g.subject_id
    WHERE g.subject_id = 5 AND s.group_id = 2
    ORDER BY s.id ASC;
    """

    result = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname.label("student_name"),
            Group.name.label("group_name"),
            Subject.name.label("subject"),
            Grade.grade,
        )
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(and_(Grade.subject_id == 5, Student.group_id == 2))
        .order_by(Student.id.asc())
        .all()
    )

    return result


def select_08():  # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    """
    SELECT
        t.fullname AS teacher,
        sb.name AS subject,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM teachers t
    JOIN subjects sb ON t.id = sb.teacher_id
    JOIN grades g ON sb.id = g.subject_id
    WHERE t.id = 2
    GROUP BY t.fullname , sb.name
    ORDER BY average_grade DESC;
    """

    result = (
        session.query(
            Teacher.fullname.label("teacher"),
            Subject.name.label("subject"),
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Teacher)
        .join(Subject)
        .join(Grade)
        .filter(Teacher.id == 2)
        .group_by(Teacher.fullname, Subject.name)
        .order_by(desc("average_grade"))
        .all()
    )

    return result


def select_09():  # Знайти список курсів, які відвідує студент.
    """
    SELECT DISTINCT
        s.id AS student_id,
        s.fullname AS student_name,
        sb.name AS subject
    FROM grades g
    JOIN students s ON s.id = g.student_id
    JOIN subjects sb ON sb.id = g.subject_id
    WHERE s.id = 25
    ORDER BY sb.name;
    """

    result = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname.label("student_name"),
            Subject.name.label("subject"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Student.id == 25)
        .distinct()
        .order_by(Subject.name)
        .all()
    )

    return result

def select_10(): # Знайти список курсів, які певному студенту читає певний викладач.
    """
    SELECT DISTINCT
        s.id AS student_id,
        s.fullname AS student_name,
        t.fullname AS teacher,
        sb.name AS subject
    FROM grades g
    JOIN students s ON s.id = g.student_id
    JOIN subjects sb ON sb.id = g.subject_id
    JOIN teachers t ON t.id = sb.teacher_id
    WHERE s.id = 25 AND t.id = 2
    ORDER BY sb.name;
    """

    result = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname.label("student_name"),
            Teacher.fullname.label("teacher"),
            Subject.name.label("subject"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .join(Teacher)
        .filter(and_(Student.id == 25, Teacher.id == 2))
        .distinct()
        .order_by(Subject.name)
        .all()
    )

    return result

def select_11(): # Середній бал, який певний викладач ставить певному студентові.
    """
    SELECT
        t.fullname AS teacher,
        s.fullname AS student,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM teachers t
    JOIN subjects sb ON t.id = sb.teacher_id
    JOIN grades g ON sb.id = g.subject_id
    JOIN students s ON s.id = g.student_id
    WHERE t.id = 3 AND s.id = 15
    GROUP BY t.fullname, s.fullname;
    """

    result = (
        session.query(
            Teacher.fullname.label("teacher"),
            Student.fullname.label("student"),
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Teacher)
        .join(Subject)
        .join(Grade)
        .join(Student)
        .filter(and_(Teacher.id == 3, Student.id == 15))
        .group_by(Teacher.fullname, Student.fullname)
        .all()
    )

    return result

def select_12(): # Оцінки студентів у певній групі з певного предмета на останньому занятті.
    """
    SELECT
        s.id AS student_id ,
        s.fullname AS student,
        gr.grade,
        gr.grade_date AS last_date
    FROM grades gr
    JOIN students s ON gr.student_id = s.id
    WHERE gr.subject_id = 2 AND s.group_id = 3 AND gr.grade_date = (
        SELECT MAX(gr.grade_date) AS last_date
        FROM grades gr
        JOIN students s ON s.id = gr.student_id
        WHERE gr.subject_id = 2 AND s.group_id = 3
    );
    """

    subquery = (
        select(func.max(Grade.grade_date))
        .join(Student)
        .filter(and_(Grade.subject_id == 2, Student.group_id == 3))
    ).scalar_subquery()

    result = (
        session.query(
            Student.id.label("student_id"),
            Student.fullname.label("student"),
            Grade.grade,
            Grade.grade_date.label("last_date"),
        )
        .select_from(Grade)
        .join(Student)
        .filter(
            and_(
                Grade.subject_id == 2,
                Student.group_id == 3,
                Grade.grade_date == subquery,
            )
        )
        .all()
    )

    return result


if __name__ == "__main__":
    # print(select_01())
    # print(select_02())
    # print(select_03())
    # print(select_04())
    # print(select_05())
    # print(select_06())
    # print(select_07())
    # print(select_08())
    # print(select_09())
    # print(select_10())
    # print(select_11())
    print(select_12())