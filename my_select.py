from connect import session
from pprint import pprint
from sqlalchemy import func, desc, select

from models import Student, Group, Subject, Teacher, Grade


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""

    return (
        session.execute(
            select(
                Student.name.label("student_name"),
                func.avg(Grade.grade).label("average_grade"),
            )
            .join(Grade)
            .group_by(Student.id)
            .order_by(desc(func.avg(Grade.grade)))
            .limit(5)
        )
        .mappings()
        .all()
    )


def select_2(subject_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    return (
        session.execute(
            select(
                Student.name.label("student_name"),
                func.avg(Grade.grade).label("average_grade"),
                Subject.id.label("subject_id"),
                Subject.name.label("subject_name"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.id == subject_id)
            .group_by(Student.id, Subject.id)
            .order_by(desc(func.avg(Grade.grade)))
        )
        .mappings()
        .first()
    )


def select_3(subject_id: int):
    """Знайти середній бал у групах з певного предмета"""
    return (
        session.execute(
            select(
                Group.name.label("group_name"),
                func.avg(Grade.grade).label("average_grade"),
                Subject.name.label("subject_name"),
            )
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Grade.subject_id == subject_id)
            .group_by(Group.id, Subject.name)
        )
        .mappings()
        .all()
    )


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)"""
    return session.query(func.avg(Grade.grade)).scalar()


def select_5(teacher_id: int):
    """Знайти які курси читає певний викладач"""
    return (
        session.execute(
            select(
                Teacher.name.label("teacher_name"),
                Subject.name.label("subject_name"),
            )
            .join(Subject, Subject.teacher_id == Teacher.id)
            .filter(Teacher.id == teacher_id)
        )
        .mappings()
        .all()
    )


def select_6(group_id: int):
    """Знайти список студентів у певній групі."""
    return (
        session.execute(
            select(
                Group.name.label("group_name"),
                Student.id.label("student_id"),
                Student.name.label("student_name"),
            )
            .join(Student, Student.group_id == Group.id)
            .filter(Group.id == group_id)
        )
        .mappings()
        .all()
    )


def select_7(group_id: int, subject_id: int):
    """Знайти оцінки студентів у окремій групі з певного предмета"""
    return (
        session.execute(
            select(
                Group.name.label("group_name"),
                Student.name.label("student_name"),
                Subject.name.label("subject_name"),
                Grade.grade,
            )
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Group.id == group_id, Subject.id == subject_id)
        )
        .mappings()
        .all()
    )


def select_8(teacher_id: int):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    return (
        session.execute(
            select(
                Teacher.name.label("teacher_name"),
                Subject.name.label("subject_name"),
                func.avg(Grade.grade).label("average_grade"),
            )
            .join(Subject, Subject.teacher_id == Teacher.id)
            .join(Grade, Grade.subject_id == Subject.id)
            .filter(Teacher.id == teacher_id)
            .group_by(Subject.id, Teacher.id)
        )
        .mappings()
        .all()
    )


def select_9(student_id: int):
    """Знайти список курсів, які відвідує певний студент."""
    return (
        session.execute(
            select(
                Student.name.label("student_name"),
                Subject.name.label("subject_name"),
            )
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Student.id == student_id)
            .distinct()
        )
        .mappings()
        .all()
    )


def select_10(student_id: int, teacher_id: int):
    """Список курсів, які певному студенту читає певний викладач."""
    return (
        session.execute(
            select(
                Teacher.name.label("teacher_name"),
                Student.name.label("student_name"),
                Subject.name.label("subject_name"),
            )
            .join(Subject, Subject.teacher_id == Teacher.id)
            .join(Grade, Grade.subject_id == Subject.id)
            .join(Student, Student.id == Grade.student_id)
            .filter(Teacher.id == teacher_id, Student.id == student_id)
            .distinct()
        )
        .mappings()
        .all()
    )


def print_results(title, result):
    print(title)
    pprint(result)
    print("\n")


print_results(f"1. {select_1.__doc__}", select_1())
print_results(f"2. {select_2.__doc__} (SubjectId: 3)", select_2(3))
print_results(f"3. {select_3.__doc__} (SubjectId: 2)", select_3(2))
print_results(f"4. {select_4.__doc__}", select_4())
print_results(f"5. {select_5.__doc__} (TeacherId: 2)", select_5(2))
print_results(f"6. {select_6.__doc__} (GroupId: 2)", select_6(2))
print_results(f"7. {select_7.__doc__} (GroupId: 1, SubjectId: 1)", select_7(1, 1))
print_results(f"8. {select_8.__doc__} (TeacherId: 3)", select_8(3))
print_results(f"9. {select_9.__doc__} (StudentId: 9)", select_9(9))
print_results(f"10. {select_10.__doc__} (StudentId: 6, TeacherId: 4)", select_10(6, 4))

session.close()
