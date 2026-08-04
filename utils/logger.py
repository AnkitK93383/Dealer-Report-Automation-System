import csv
import os
from datetime import datetime


LOG_FILE = "logs/usage_log.csv"


def log_usage(
    username,
    reports,
    emails_sent,
    success,
    failed,
    skipped,
    duration
):

    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.exists(LOG_FILE)

    with open(
        LOG_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file, delimiter=",")

        if not file_exists:

            writer.writerow([
                "Date",
                "Time",
                "Username",
                "Reports",
                "Emails Sent",
                "Success",
                "Failed",
                "Skipped",
                "Duration"
            ])

        now = datetime.now()

        writer.writerow([
            now.strftime("%d-%m-%Y"),
            now.strftime("%H:%M:%S"),
            username,
            reports,
            emails_sent,
            success,
            failed,
            skipped,
            f"{duration:.2f} sec"
        ])