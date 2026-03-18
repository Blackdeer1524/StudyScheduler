import datetime
from collections import deque
from fractions import Fraction
from dataclasses import dataclass
import yaml


@dataclass(frozen=True)
class LectureInfo:
    hours: int
    minutes: int

    @property
    def total_minutes(self) -> int:
        return self.hours * 60 + self.minutes


TODAY = datetime.datetime.today()
DEADLINE = datetime.datetime(TODAY.year, 4, 15)
DAYS_LEFT = (DEADLINE - TODAY).days + 2

with open("subjects.yaml", encoding="utf-8") as _f:
    _raw = yaml.safe_load(_f)

subjects_info: dict[str, dict[int, LectureInfo]] = {
    subject: {
        int(lec_num): LectureInfo(**info)
        for lec_num, info in lectures.items()
    }
    for subject, lectures in _raw.items()
}

total_minutes = sum(
    lec.total_minutes
    for lectures in subjects_info.values()
    for lec in lectures.values()
)

daily_target = Fraction(total_minutes, DAYS_LEFT)

total_time: dict[str, int] = {
    name: sum(lec.total_minutes for lec in lectures.values())
    for name, lectures in subjects_info.items()
}

# Fraction of total subject time already done (starts at 0)
time_done: dict[str, Fraction] = {name: Fraction(0) for name in subjects_info}

remaining: dict[str, deque[int]] = {
    name: deque(sorted(lectures.keys()))
    for name, lectures in subjects_info.items()
}

budget = Fraction(0)

for i in range(DAYS_LEFT - 1, -1, -1):
    cur_date = DEADLINE - datetime.timedelta(days=i)
    budget += daily_target

    assigned_today = False

    while True:
        candidates = [
            (s, remaining[s][0])
            for s in subjects_info
            if remaining[s]
        ]
        if not candidates:
            break  # all lectures scheduled

        # Tier 1: lectures that fit within the remaining budget
        fitting = [
            (s, lec_num)
            for s, lec_num in candidates
            if subjects_info[s][lec_num].total_minutes <= budget
        ]

        if fitting:
            # least-done fraction, tie-broken by largest (tightest-fit) duration
            s, lec_num = min(
                fitting,
                key=lambda x: (time_done[x[0]], -subjects_info[x[0]][x[1]].total_minutes),
            )
        elif not assigned_today:
            # Tier 2: force-assign from least-done subject
            s, lec_num = min(candidates, key=lambda x: time_done[x[0]])
        else:
            break

        dur = subjects_info[s][lec_num].total_minutes
        remaining[s].popleft()
        budget -= dur
        time_done[s] += Fraction(dur, total_time[s])
        h, m = divmod(dur, 60)
        print(f"[{cur_date.date()}]:{s} {lec_num} ({h}h {m}m)")
        assigned_today = True

    if not assigned_today:
        print("FREE DAY")
