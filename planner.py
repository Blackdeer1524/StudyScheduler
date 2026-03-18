import datetime
from collections import deque
from fractions import Fraction
from dataclasses import dataclass


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

subjects_info: dict[str, dict[int, LectureInfo]] = {
    "Теория вероятностей": {
        10: LectureInfo(hours=1, minutes=25),
        14: LectureInfo(hours=2, minutes=31),
        15: LectureInfo(hours=1, minutes=56),
        16: LectureInfo(hours=1, minutes=38),
        17: LectureInfo(hours=2, minutes=8),
        18: LectureInfo(hours=1, minutes=28),
        19: LectureInfo(hours=1, minutes=14),
        20: LectureInfo(hours=1, minutes=7),
        21: LectureInfo(hours=1, minutes=29),
        22: LectureInfo(hours=1, minutes=14),
        23: LectureInfo(hours=1, minutes=18),
        24: LectureInfo(hours=1, minutes=28),
        25: LectureInfo(hours=1, minutes=0),
        26: LectureInfo(hours=1, minutes=39),
        27: LectureInfo(hours=1, minutes=39),
        28: LectureInfo(hours=1, minutes=35),
        29: LectureInfo(hours=1, minutes=27),
    },
    "Анализ": {
        7:  LectureInfo(hours=3, minutes=24),
        8:  LectureInfo(hours=2, minutes=23),
        9:  LectureInfo(hours=1, minutes=35),
        10: LectureInfo(hours=3, minutes=45),
        11: LectureInfo(hours=1, minutes=29),
        12: LectureInfo(hours=1, minutes=20),
        13: LectureInfo(hours=1, minutes=37),
        14: LectureInfo(hours=1, minutes=38),
        15: LectureInfo(hours=1, minutes=26),
        16: LectureInfo(hours=1, minutes=8),
        17: LectureInfo(hours=1, minutes=40),
        18: LectureInfo(hours=1, minutes=20),
        19: LectureInfo(hours=1, minutes=30),
        20: LectureInfo(hours=1, minutes=23),
        21: LectureInfo(hours=0, minutes=56),
        22: LectureInfo(hours=1, minutes=30),
        23: LectureInfo(hours=1, minutes=3),
        24: LectureInfo(hours=1, minutes=15),
        25: LectureInfo(hours=1, minutes=23),
        26: LectureInfo(hours=1, minutes=14),
        27: LectureInfo(hours=1, minutes=42),
        28: LectureInfo(hours=1, minutes=25),
    },
    "Линейная алгебра": {
        1:  LectureInfo(hours=3, minutes=7),
        2:  LectureInfo(hours=1, minutes=55),
        3:  LectureInfo(hours=1, minutes=36),
        4:  LectureInfo(hours=1, minutes=32),
        5:  LectureInfo(hours=1, minutes=25),
        6:  LectureInfo(hours=1, minutes=36),
        7:  LectureInfo(hours=1, minutes=54),
        8:  LectureInfo(hours=0, minutes=51),
        9:  LectureInfo(hours=1, minutes=30),
        10: LectureInfo(hours=1, minutes=11),
        11: LectureInfo(hours=1, minutes=19),
        12: LectureInfo(hours=1, minutes=36),
        13: LectureInfo(hours=2, minutes=5),
        14: LectureInfo(hours=1, minutes=45),
        15: LectureInfo(hours=1, minutes=24),
        16: LectureInfo(hours=1, minutes=14),
        17: LectureInfo(hours=1, minutes=43),
        18: LectureInfo(hours=1, minutes=58),
        19: LectureInfo(hours=1, minutes=27),
        20: LectureInfo(hours=1, minutes=39),
        21: LectureInfo(hours=0, minutes=59),
        22: LectureInfo(hours=1, minutes=29),
        23: LectureInfo(hours=1, minutes=1),
        24: LectureInfo(hours=1, minutes=10),
        25: LectureInfo(hours=1, minutes=22),
        26: LectureInfo(hours=1, minutes=35),
        27: LectureInfo(hours=1, minutes=20),
        28: LectureInfo(hours=1, minutes=47),
    },
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
