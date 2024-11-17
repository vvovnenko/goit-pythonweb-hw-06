import random
from datetime import datetime, timedelta
from itertools import chain

from faker import Faker

from models import Group, Student, Teacher, Subject, Grade
from connect import session


fake = Faker()

with session.begin():

    groups = list(
        map(
            lambda group_name: Group(name=group_name), ["Group-1", "Group-2", "Group-3"]
        )
    )

    students = list(
        map(lambda _: Student(name=fake.name(), group=random.choice(groups)), range(40))
    )

    teachers = list(map(lambda _: Teacher(name=fake.name()), range(4)))

    subjects = list(
        map(
            lambda subject_name: Subject(
                name=subject_name, teacher=random.choice(teachers)
            ),
            [
                "Physics",
                "Math",
                "History",
                "Biology",
                "Literature",
                "Art",
            ],
        )
    )

    grades = list(
        chain.from_iterable(
            map(
                lambda student: [
                    Grade(
                        grade=random.randint(40, 100),
                        created=datetime.now() - timedelta(days=random.randint(1, 365)),
                        student=student,
                        subject=random.choice(subjects),
                    )
                    for _ in range(random.randint(10, 20))
                ],
                students,
            )
        )
    )

    session.add_all(groups + students + teachers + subjects + grades)

session.close()
