calendar.txt: planner.py subjects.yaml
	python planner.py | grep -v FREE > calendar.txt

generate: generate.py calendar.txt
	python generate.py calendar.txt > custom_study_calendar.ics

