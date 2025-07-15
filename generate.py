from datetime import datetime, timedelta
import sys


def main():
    if len(sys.argv) < 2:
        print("filepath for a schedule wasn't given")
        sys.exit(1)

    # Load the calendar text content
    with open(sys.argv[1], "r") as f:
        calendar_text = "".join(f.readlines())

    # Start generating .ics file
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "PRODID:-//Custom Calendar Import//EN",
    ]

    # Process each line in the calendar text
    for line in calendar_text.strip().split("\n"):
        if not line.strip():
            continue
        date_str, title = line.strip().split("]:")
        date_str = date_str.strip("[")
        title = title.strip()

        start_date = datetime.strptime(date_str, "%Y-%m-%d")
        end_date = start_date + timedelta(days=1)  # All-day event ends next day (exclusive)

        # Format date in YYYYMMDD format for all-day events
        start_fmt = start_date.strftime("%Y%m%d")
        end_fmt = end_date.strftime("%Y%m%d")

        # Create VEVENT entry
        ics_lines += [
            "BEGIN:VEVENT",
            f"SUMMARY:{title}",
            f"DTSTART;VALUE=DATE:{start_fmt}",
            f"DTEND;VALUE=DATE:{end_fmt}",
            "END:VEVENT",
        ]

    ics_lines.append("END:VCALENDAR")

    # Write to .ics file
    ics_content = "\n".join(ics_lines)
    ics_path = "./custom_study_calendar.ics"
    with open(ics_path, "w") as f:
        f.write(ics_content)

if __name__ == "__main__":
    main()

