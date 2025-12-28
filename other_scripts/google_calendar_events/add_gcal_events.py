import argparse
import logging
from datetime import timedelta

import pandas as pd
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


def read_events_file(file_path):
    logger.info(f"Reading events from file_path={file_path}")
    events_df = pd.read_csv(file_path)
    events_df["event_date_start"] = pd.to_datetime(
        events_df["event_date_start"]
    ).dt.tz_localize("America/New_York")
    events_df["event_date_end"] = pd.to_datetime(
        events_df["event_date_end"]
    ).dt.tz_localize("America/New_York")

    logger.info(f"Read {len(events_df)} events from file_path={file_path}")

    return events_df


def add_events(events_df, calendar, dry_run):
    for idx, row in events_df.iterrows():
        event_name = row["event_name"]
        start_dt = row["event_date_start"]
        end_dt = row["event_date_end"]
        location = row["location"]

        logger.info(
            f"Adding event_name={event_name} with start={start_dt},end={end_dt},location={location}"
        )

        if not dry_run:
            e = Event(event_name, start=start_dt, end=end_dt, location=location)
            calendar.add_event(e)


def main():
    parser = argparse.ArgumentParser(description="Adds events from a file to calendar")
    parser.add_argument("--calendar-id", type=str, help="Google calendar id")
    parser.add_argument(
        "--wipe-calendar",
        action="store_true",
        help="Wipe the calendar before adding events",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print out what is being done but don't do it",
    )
    parser.add_argument(
        "--events-file-path",
        type=str,
        required=True,
        help="CSV file containing events to be added",
    )

    args = parser.parse_args()
    calendar_id = args.calendar_id
    wipe_calendar = args.wipe_calendar
    dry_run = args.dry_run
    events_file_path = args.events_file_path

    logger.info(f"Calendar id={calendar_id}")
    if dry_run:
        logger.info(f"Dry run mode enabled, no changes will be made")

    cal = GoogleCalendar(calendar_id)

    df_events = read_events_file(events_file_path)

    if not dry_run and wipe_calendar:
        logger.info(f"Wiping calendar before adding new events to it")
        s = df_events["event_date_start"].min()
        e = df_events["event_date_start"].max() + timedelta(hours=1)
        for e in cal.get_events(time_min=s, time_max=e):
            logger.info(f"Deleting event={e.summary}")
            cal.delete_event(e)

    add_events(df_events, cal, dry_run)


if __name__ == "__main__":
    main()
