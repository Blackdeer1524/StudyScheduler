import datetime
from fractions import Fraction
from dataclasses import dataclass


@dataclass(frozen=True)
class SubjectInfo:
    already_done: int
    total_count: int


subjects_info: dict[str, SubjectInfo] = {
    "Algebra": SubjectInfo(
        already_done=14,
        total_count=33
    ),
    "Probability": SubjectInfo(
        already_done=0,
        total_count=27,
    )
}

TODAY = datetime.datetime.today()
DEADLINE = datetime.datetime(TODAY.year, 8, 31)
DAYS_TOTAL = (DEADLINE - TODAY).days + 1

subjects_count = len(subjects_info)
total_lectures_count = sum(info.total_count - info.already_done for info in subjects_info.values())

dayly_load = Fraction(total_lectures_count, DAYS_TOTAL)
current_dose = Fraction(0, 1)

# сколько уже сделано
subjects_goals = {
    name: Fraction(info.total_count - info.already_done, info.total_count)
    for name, info in subjects_info.items()
}

# считаем с конца. иначе план может на сегодня ничего не выдать
today = DEADLINE
next_lecture_to_schedule = {s: info.total_count for s, info in subjects_info.items()}
for i in range(DAYS_TOTAL):
    cur_date = today - datetime.timedelta(days=i)
    current_dose += dayly_load
    actual_count = int(current_dose)
    current_dose -= actual_count
    if actual_count == 0:
        print("FREE DAY")
        continue

    for j in range(actual_count):
        least_done_percent = Fraction(-1, 1)
        least_done_subject: str | None = None
        for subject, percentage_done in subjects_goals.items():
            if least_done_percent < percentage_done:
                least_done_percent = percentage_done
                least_done_subject = subject
        assert least_done_subject is not None
        print(f"[{cur_date.date()}]:{least_done_subject} {next_lecture_to_schedule[least_done_subject]}")
        subjects_goals[least_done_subject] -= Fraction(
            1, subjects_info[least_done_subject].total_count
        )
        next_lecture_to_schedule[least_done_subject] -= 1
