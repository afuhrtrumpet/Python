#Uses JSON generated from gcalendarreceiver to create a graphical calendar.
import calendar
import pygame
from datetime import date
import json

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 175
HEIGHT = 150
TOPMARGIN = 50

pygame.init()
size = [WIDTH * 7, HEIGHT * 5 + TOPMARGIN * 2]
screen = pygame.display.set_mode(size)

month = date.today().month
year = date.today().year
pygame.display.set_caption("Calendar")
done = False;
datefont = pygame.font.SysFont("monospace", 24)
monthfont = pygame.font.SysFont("monospace", 36)
eventfont = pygame.font.SysFont("monospace", 18)

inputfile = open("calendaroutput.json", "r")
inputdata = inputfile.read()
eventjson = json.loads(inputdata)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                month -= 1
                if month == 0:
                    month = 12
                    year -= 1
            if event.key == pygame.K_RIGHT:
                month += 1
                if month == 13:
                    month = 1
                    year += 1
    screen.fill(WHITE)
    if month == 1:
        monthtext = "January"
    elif month == 2:
        monthtext = "February"
    elif month == 3:
        monthtext = "March"
    elif month == 4:
        monthtext = "April"
    elif month == 5:
        monthtext = "May"
    elif month == 6:
        monthtext = "June"
    elif month == 7:
        monthtext = "July"
    elif month == 8:
        monthtext = "August"
    elif month == 9:
        monthtext = "September"
    elif month == 10:
        monthtext = "October"
    elif month == 11:
        monthtext = "November"
    elif month == 12:
        monthtext = "December"
    pygame.draw.rect(screen, BLACK, [0, 0, WIDTH * 7, TOPMARGIN], 2)
    screen.blit(monthfont.render(monthtext + " " + str(year), 1, BLACK), (WIDTH * 7 / 4, 0))
    for i in range(0, 7):
        if i == 0:
            day = "Sunday"
        elif i == 1:
            day = "Monday"
        elif i == 2:
            day = "Tuesday"
        elif i == 3:
            day = "Wednesday"
        elif i == 4:
            day = "Thursday"
        elif i == 5:
            day = "Friday"
        elif i == 6:
            day == "Saturday"
        daytext = datefont.render(day, 1, BLACK)
        screen.blit(daytext, (i * WIDTH, TOPMARGIN))
        pygame.draw.rect(screen, BLACK, [i * WIDTH, TOPMARGIN, WIDTH, TOPMARGIN], 2)
    calendar.setfirstweekday(6)
    cal = calendar.monthcalendar(year, month)
    for r in range(0, len(cal)):
        for c in range(0, 7):
            pygame.draw.rect(screen, BLACK, [c * WIDTH, r * HEIGHT + TOPMARGIN * 2, WIDTH, HEIGHT], 2)
            if cal[r][c] != 0:
                text = datefont.render(str(cal[r][c]), 1, BLACK)
                screen.blit(text, (c * WIDTH, r * HEIGHT + TOPMARGIN * 2))
                identifier = str(month) + " " + str(cal[r][c]) + " " + str(year)
                eventcount = 0
                if identifier in eventjson:
                    for event in eventjson[identifier]:
                        text = eventfont.render(event["title"], 1, BLACK)
                        screen.blit(text, (c * WIDTH, r * HEIGHT + TOPMARGIN * 2 + 25 + 20 * eventcount))
                        eventcount += 1
    pygame.display.flip()
pygame.quit();
