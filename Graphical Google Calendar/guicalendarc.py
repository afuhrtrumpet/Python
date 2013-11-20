from Tkinter import *
import calendar
from datetime import date
import json

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.fWidth = self.master.winfo_screenwidth()
        self.fHeight = self.master.winfo_screenheight()
        self.master.minsize(width=self.fWidth, height=self.fHeight)
        self.master.config()

        inputfile = open("calendaroutput.json", "r")
        inputdata = inputfile.read()
        self.eventjson = json.loads(inputdata)

        self.month = date.today().month
        self.year = date.today().year

        self.master.bind('<Left>', self.left_key)
        self.master.bind('<Right>', self.right_key)

        self.currMonth = Label(self, text=self.getMonthText(self.month) + " " + str(self.year), font=("Helvetica", 36))
        self.currMonth.grid(row=0, column=0, columnspan=7)

        self.monthLbls=[]
        self.eventLbls=[]
        for r in range(0, 6):
            monthRow = []
            eventRow = []
            for c in range(0, 7):
                monthRow.append(Label(self, text="", font=("Helvetica", 20), wraplength=self.fWidth/7, justify=CENTER))
                monthRow[c].grid(row=2+2*r, column=c)
                eventRow.append(Label(self, text="", font=("Helvtica", 20), wraplength=self.fWidth/7, justify=CENTER))
                eventRow[c].grid(row=3+2*r, column=c)
                self.columnconfigure(c, minsize=self.fWidth/7)
            self.monthLbls.append(monthRow)
            self.eventLbls.append(eventRow)

        self.buildMonth()
        
        self.pack(fill=BOTH, expand=YES)

        for i in range(0, 7):
            Label(self, text=self.getWeekday(i), font=("Helvetica", 20)).grid(row=1, column=i)

    def left_key(self, event):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.currMonth['text'] = self.getMonthText(self.month) + " " + str(self.year)
        self.buildMonth()

    def right_key(self, event):
        self.month += 1
        if self.month ==  13:
            self.month = 1
            self.year += 1
        self.currMonth['text'] = self.getMonthText(self.month) + " " + str(self.year)
        self.buildMonth()

    @staticmethod
    def getMonthText(month):
        if month == 1:
            return "January"
        elif month == 2:
            return "February"
        elif month == 3:
            return "March"
        elif month == 4:
            return "April"
        elif month == 5:
            return "May"
        elif month == 6:
            return "June"
        elif month == 7:
            return "July"
        elif month == 8:
            return "August"
        elif month == 9:
            return "September"
        elif month == 10:
            return "October"
        elif month == 11:
            return "November"
        elif month == 12:
            return "December"

    @staticmethod
    def getWeekday(day):
        if day == 0:
            return "Sunday"
        elif day == 1:
            return "Monday"
        elif day == 2:
            return "Tuesday"
        elif day == 3:
            return "Wednesday"
        elif day == 4:
            return "Thursday"
        elif day == 5:
            return "Friday"
        elif day == 6:
            return "Saturday"

    def buildMonth(self):
        self.resetLbls()
        calendar.setfirstweekday(6)
        cal = calendar.monthcalendar(self.year, self.month)
        for r in range(0, len(cal)):
            for c in range(0, 7):
                if cal[r][c] != 0:
                    self.monthLbls[r][c]['text'] = str(cal[r][c])
                    identifier = str(self.month) + " " + str(cal[r][c]) + " " + str(self.year)
                    if identifier in self.eventjson:
                        events = ""
                        for event in self.eventjson[identifier]:
                            events = events + event["title"] + '\n'
                        self.eventLbls[r][c]['text'] = events

    def resetLbls(self):
        for r in range(0, 6):
            for c in range(0, 7):
                self.monthLbls[r][c]['text'] = ""
                self.eventLbls[r][c]['text'] = ""

root = Tk()
app = Application(root)
app.mainloop()
