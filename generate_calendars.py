import os
import zipfile
from datetime import datetime

# Directory setup
BASE_DIR = "/Users/shubhayu/Documents/antigravity/splendid-raman"
GEN_DIR = os.path.join(BASE_DIR, "output", "general")
BATCH_B_DIR = os.path.join(BASE_DIR, "output", "batch_b")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")

os.makedirs(GEN_DIR, exist_ok=True)
os.makedirs(BATCH_B_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def create_ics(filename, cal_name, prod_id, color, events):
    """
    Creates an RFC-5545 compliant ICS file with VALARM (15 mins) and colors.
    """
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{prod_id}",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{cal_name}",
        "X-WR-TIMEZONE:Asia/Kolkata",
        f"X-APPLE-CALENDAR-COLOR:{color}",
        f"COLOR:{color}",
        "BEGIN:VTIMEZONE",
        "TZID:Asia/Kolkata",
        "X-LIC-LOCATION:Asia/Kolkata",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0530",
        "TZOFFSETTO:+0530",
        "TZNAME:IST",
        "DTSTART:19700101T000000",
        "END:STANDARD",
        "END:VTIMEZONE"
    ]

    for ev in events:
        lines.append("BEGIN:VEVENT")
        lines.append(f"UID:{ev['uid']}")
        lines.append(f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}")
        lines.append(f"DTSTART;TZID=Asia/Kolkata:{ev['dtstart']}")
        lines.append(f"DTEND;TZID=Asia/Kolkata:{ev['dtend']}")
        lines.append(f"SUMMARY:{ev['summary']}")
        if 'location' in ev and ev['location']:
            lines.append(f"LOCATION:{ev['location']}")
        if 'description' in ev and ev['description']:
            # escape newlines for ICS
            desc = ev['description'].replace("\n", "\\n")
            lines.append(f"DESCRIPTION:{desc}")
        lines.append("STATUS:CONFIRMED")
        lines.append("TRANSP:OPAQUE")
        lines.append("BEGIN:VALARM")
        lines.append("ACTION:DISPLAY")
        lines.append("DESCRIPTION:Class in 15 minutes")
        lines.append("TRIGGER:-PT15M")
        lines.append("END:VALARM")
        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")
    lines.append("") # final newline

    content = "\r\n".join(lines)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filename} with {len(events)} events.")

print("Script template ready.")
