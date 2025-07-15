calendar.txt: planner.py
	python planner.py | grep -v FREE > calendar.txt

generate: generate.py calendar.txt
	python generate.py calendar.txt > custom_study_calendar.ics

