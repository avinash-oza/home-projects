from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from datetime import datetime

if __name__ == '__main__':
    test_calendar = None
    cal = GoogleCalendar(test_calendar)
    # e = Event(
    #     'Test Event',
    #     start=datetime(2022, 1, 16, 22, 30),
    #     end=datetime(2022, 1, 16, 22, 45)
    # )
    # cal.add_event(e)
    for e in cal.get_events():
        print(e.id)
