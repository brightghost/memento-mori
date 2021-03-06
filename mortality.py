#!/usr/bin/env python3.4

# Please don't use this if it makes you feel bad about yourself. I love you.
# --S Walker 2016/12/19
#
# The MIT License (MIT)
#
# Copyright (c) 2016 S. Walker
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from datetime import *
import os
import textwrap
import argparse

today = date.today()
configfile = os.path.expanduser("~/.config/mortality")

# terminal window size, for textwrap lib
try:
    termh, termw = os.popen('stty size', 'r').read().split()
    termh = int(termh)
    termw = int(termw)
except ValueError:
    # Just try some conservative defaults
    termh, termw = 20, 40

def readConfig():
    '''Return the first non-comment line into a date object.'''
    try:
        with open(configfile, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
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
    parser = argparse.ArgumentParser(description="Show a daily message "
            "regarding your personal march to the grave."
            "The intended use-case is for this script to be sourced in a "
            "shell profile, with no arguments; you will be prompted to create "
            "a config file on first use.")
    parser.add_argument('-p', '--print', action='store_true',
            help="force printing of the message, even if it's "
            "already been shown today.")
    args = parser.parse_args()
    try:
        mtime = datetime.fromtimestamp(os.stat(configfile).st_mtime)
        birthday = readConfig()
        midnight = datetime(today.year, today.month, today.day)
        if (mtime <= midnight) or args.print:
            os.utime(configfile)
            printInfoForBirthday(birthday)
    except (OSError):
        birthday = promptForBirthday()
        with open(configfile, 'a') as f:
            print("# Config file for the mortality.py shell prompt script.\n"
                "# In addition to the birthday below, the  file modify\n"
                "# time is significant as it is used to show the prompt\n"
                "# only once/day.\n"
                "#\n"
                "# github.com/brightghost/memento-mori\n",
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
    nextyearsbirthday = date((today.year + 1), birthday.month, birthday.day)
    if thisyearsbirthday > today:
        daysuntilbirthday = thisyearsbirthday - today
    elif thisyearsbirthday <= today:
        daysuntilbirthday = nextyearsbirthday - today
    daysuntilnewyear = date((today.year + 1), 1, 1) - today
    age = today - birthday
    ageinyears = int(age.days / 365)
    remainder = int(age.days % 365)

    if today == thisyearsbirthday:
        msg1 = "Today is {}. {}You are exactly {} years old!{}".format(
                today.strftime("%A, %B %d"), colors['UNDERLINE'],
                ageinyears, colors['CLEAR'])
    else:
        msg1 = "Today is {}. {}You are {} years and {} days old.{}".format(
                today.strftime("%A, %B %d"), colors['UNDERLINE'],
                ageinyears, remainder, colors['CLEAR'])
    msg2 = "There are {} days until your next birthday, and {} days left in the year.".format(daysuntilbirthday.days, daysuntilnewyear.days)

    print()
    print(textwrap.fill(msg1, width=termw))
    print(textwrap.fill(msg2, width=termw))
    print()

main()
