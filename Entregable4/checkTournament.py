#!/usr/bin/env python3

import sys

def error(m):
    sys.stderr.write(m + "\n")
    sys.exit(1)

def parseError(nl, m):
    error("Error in line {}: {}".format(nl, m))

def parseInput(input):
    result = []
    currentDay = 0
    matches = None
    for nl, l in enumerate(input):
        nl += 1
        l = l.strip()
        if l.startswith("Day"):
            matches = []
            result.append(matches)
            n = l.split()[1]
            if n.endswith(":"):
                day = parseInt(n[:-1], nl)
                if currentDay + 1 != day:
                    parseError(nl, "Wrong day number.")
                currentDay = day
            else:
                parseError(nl, "Wrong day line format.")
        else:
            c = l.split()
            if len(c) != 3:
                parseError(nl, "Wrong line format, expected a match line.")
            if c[1] != "vs":
                parseError(nl, "The second item in a match must be vs.")
            p1 = parsePlayer(c[0], nl)
            p2 = parsePlayer(c[2], nl)
            if matches is None:
                parseError(nl, "There must be a day line before the first match.")
            matches.append((p1, p2))
    return result

def checkTournament(tournament, nplayers):
    if len(tournament) != nplayers - 1:
        error ("There should be {} days.".format(nplayers - 1))

    day = {}
    for nday, matches in enumerate(tournament):
        nday += 1
        if len(matches) != nplayers // 2:
            error("The day {} should have {} matches.".format(nday, nplayers // 2))
        for p1, p2 in matches:
            p1, p2 = min(p1, p2), max(p1, p2)
            if (p1, p2) in day:
                error("The match {} vs {} is repeated on days {} and {}.".format(p1, p2, day[(p1, p2)], nday))
            day[(p1, p2)] = nday
        players = set([p1 for p1,_ in matches] + [p2 for _,p2 in matches])
        if len(players) != nplayers:
            error("Not all players participate in day {}.".format(nday))
    return True

def parseInt(n, nl):
    try:
        return int(n)
    except ValueError:
        parseError(nl, "Found {} where a number was expected.".format(n))

def parsePlayer(p, nl):
    if p[0] != "p":
        parseError(nl, "A player name must begin with p, found {}.".format(p))
    parseInt(p[1:], nl)
    return p

if len(sys.argv) == 1:
    error("No number of players given.")
if len(sys.argv) == 2:
    input = sys.stdin
else:
    try:
        input = open(sys.argv[2])
    except:
        error ("Error opening input file ({}).".format(sys.argv[2]))
try:
    nplayers = int(sys.argv[1])
except ValueError:
    error("Bad number of players ({})".format(sys.argv[1]))

tournament = parseInput(input)
if checkTournament(tournament, nplayers):
    print ("No errors detected")
else:
    print ("Errors in the tournament")