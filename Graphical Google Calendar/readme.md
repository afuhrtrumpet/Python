gcalendarreceiver.py reads data from a user's Google Calendar account, while graphicalcalendar.py uses data created by gcalendarreceiver to construct a graphical calendar using the PyGame libraries.
guicalendarc.py displays the data in a tkinter GUI

Known issues:
- No text wrapping for large events in graphicalcalendar.py
- Recurring events only are displayed on the first date they occurred.
End goal is to run these scripts on a lightweight computer attached to a refrigerator.
