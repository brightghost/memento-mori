#!/usr/bin/env python3.4

from datetime import *
import os
import textwrap

today = date.today()
configfile = os.path.expanduser("~/.config/mortality")

# terminal window size, for textwrap lib
termh, termw = os.popen('stty size', 'r').read().split()
termh = int(termh)
termw = int(termw)


def readConfig():
    '''Return the first non-comment line into a date object.'''
    try:
        with open(configfile, 'r') as f:
            for line in f:
                line = line.strip()
                if not line.startswith("#"):
                    return datetime.strptime(line, "%Y-%m-%d").date()
    except:
        print("Error reading the memento-mori config file (", configfile, ")")
        print("Try deleting this file to start fresh.")
        raise

def promptForBirthday():
    '''Prompt interactively for birthday if we can't find one stored.'''
    print()
    print(textwrap.fill("This is the memento-mori shell script. Looks like you don't have a config file yet. It's pretty easy. Just enter your birthday in the format YYYY/MM/DD :", width=termw))
    print()
    while True:
        try:
            birthday = datetime.strptime(input("Birhday: "), "%Y/%m/%d").date()
        except ValueError:
            print("Sorry, couldn't parse that. Please try again.")
            continue
        else:
            break
    return birthday


def main():
    '''Check that we have birthday saved and then print our info
    only if it's the first terminal of the day; tracked by touching
    the config file.'''
    try:
        mtime = datetime.fromtimestamp(os.stat(configfile).st_mtime)
        birthday = readConfig()
        midnight = datetime(today.year, today.month, today.day)
        if mtime <= midnight:
            os.utime(configfile)
            printInfoForBirthday(birthday)
    except (OSError):
        birthday = promptForBirthday()
        with open(configfile, 'a') as f:
            print("# Config file for the mortality.py shell prompt script. \
                # In addition to the birthday below, the  modify time is \
                # significant as it is used to show the prompt only once/day.", \
                file=f)
            print(birthday, file=f)
            printInfoForBirthday(birthday)

def printInfoForBirthday(birthday):
    colors = { 'HEADER': '\033[95m',
        'BLUE': '\033[94m',
        'GREEN': '\033[92m',
        'CLEAR': '\033[0m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m' }
    origin = date(today.year, 1, 1) - timedelta(1)
    thisyearsbirthday = date(today.year, birthday.month, birthday.day)
    daysuntilbirthday = thisyearsbirthday - today
    daysuntilnewyear = date((today.year + 1), 1, 1) - today
    age = today - birthday
    ageinyears = int(age.days / 365)
    remainder = today - origin

    msg1 = "Today is {}{} You are {} years and {} days old.{}".format(\
            today.strftime("%A, %B, %d."), colors['UNDERLINE'], ageinyears, remainder.days, colors['CLEAR'])
    msg2 = "There are {} days until your next birthday, and {} days left in the year.".format(\
            daysuntilbirthday.days, daysuntilnewyear.days)
    print()
    print(textwrap.fill(msg1, width=termw))
    print(textwrap.fill(msg2, width=termw))
    print()

main()
