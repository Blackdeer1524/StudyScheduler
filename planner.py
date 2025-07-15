import datetime
from fractions import Fraction
from dataclasses import dataclass


END = datetime.datetime(datetime.datetime.today().year, 8, 31)


buffer = [("Algebra", 35, 7)]
days_total = (END - datetime.datetime.today()).days
subjects_count = len(buffer)


@dataclass(frozen=True)
class SubjectInfo:
    already_done: int
    total_count: int


subjects_info: dict[str, SubjectInfo] = {}
total_lectures_count = 0

for i in range(subjects_count):
    name, total_count, already_done = buffer[i]  # input().split()
    total_count = int(total_count)
    subjects_info[name] = SubjectInfo(already_done, total_count)
    total_lectures_count += total_count - already_done


dayly_amount = Fraction(total_lectures_count, days_total)

current_dose = 0

subjects_targets = {
    name: Fraction(info.total_count - info.already_done, info.total_count)
    for name, info in subjects_info.items()
}

today = END
cc = {s: info.total_count for s, info in subjects_info.items()}
for i in range(days_total):
    cur_date = today - datetime.timedelta(days=i)
    current_dose += dayly_amount
    actual_count = int(current_dose)
    current_dose -= actual_count
    print(f"[{cur_date.date()}]:", end="")
    if actual_count == 0:
        print("FREE DAY")
        continue

    for j in range(actual_count):
        least_done_percent = Fraction(-1, 1)
        least_done_subject: str | None = None
        for subject, percentage_done in subjects_targets.items():
            if least_done_percent < percentage_done:
                least_done_percent = percentage_done
                least_done_subject = subject
        assert least_done_subject is not None
        print(f"{least_done_subject} {cc[least_done_subject]}", end="")
        subjects_targets[least_done_subject] -= Fraction(
            1, subjects_info[subject].total_count
        )
        cc[least_done_subject] -= 1
    print()
