#!/usr/bin/env python3

from bs4 import BeautifulSoup
import csv
import operator
import requests

if __name__ == '__main__':

   url = 'https://www.soccerstats.com/latest.asp?league=england' #URL
   response = requests.get(url) #RESPONSE
   if response.status_code in [200]:
      print('It worked!')
   bs = BeautifulSoup(response.text, 'html.parser') #CONTENT
   
   output = open('table.csv', 'w')
   writer = csv.writer(output, quoting=csv.QUOTE_ALL, lineterminator='\n')
   writer.writerow(['Position', 'Team', 'Games Played', 'Win', 'Draw', 'Lose', 'Goals For', 'Goals Against', 'Goal Difference', 'Points'])

   teams  = []
   gfs = []
   gas = []

   btable = bs.findAll('table', {'id': 'btable'})[0]

   for tr in btable.findAll('tr', {'class': 'odd'}):
      pos = tr.select('td:nth-of-type(1)')[0].get_text().strip()
      team = tr.select('td:nth-of-type(2)')[0].get_text().strip()
      played = tr.select('td:nth-of-type(3)')[0].get_text().strip()
      win = tr.select('td:nth-of-type(4)')[0].get_text().strip()
      draw = tr.select('td:nth-of-type(5)')[0].get_text().strip()
      lose = tr.select('td:nth-of-type(6)')[0].get_text().strip()
      gf = tr.select('td:nth-of-type(7)')[0].get_text().strip()
      ga = tr.select('td:nth-of-type(8)')[0].get_text().strip()
      gd = tr.select('td:nth-of-type(9)')[0].get_text().strip()
      pts = tr.select('td:nth-of-type(10)')[0].get_text().strip()

      #print(pos, team, played, win, draw, lose, gf, ga, gd, pts)
      writer.writerow([pos, team, played, win, draw, lose, gf, ga, gd, pts])

      teams.append(team)
      gfs.append(int(gf))
      gas.append(int(ga))

   goals_for = dict(zip(teams, gfs)) #Goals For Dictionary.
   goals_against = dict(zip(teams, gas)) #Goals Against Dictionary.
   
   print(max(goals_for.items(), key=operator.itemgetter(1)))
   print(max(goals_against.items(), key=operator.itemgetter(1)))
   
   writer.writerow([''])
   writer.writerow(['Most Goals Scored:', max(goals_for.items(), key=operator.itemgetter(1))[0]])
   writer.writerow(['Most Goals Conceded:', max(goals_against.items(), key=operator.itemgetter(1))[0]])