from bs4 import BeautifulSoup
from collections import OrderedDict
import os
import csv
import json
import datetime
from __init__ import get_data


class Cricket():

	def __init__(self):
		pass

	def convert(self,input):
		l = []
		for x in input.items():
			d = x[1]
			d['name'] = str(x[0])
			if 'overs' in d:
				d['overs'] = float(str(d['overs']/6) + "." + str(d['overs']%6))
			l.append(d)

		return l

	def query(self,mtype = ['T20','ODI','Test'],competition=[],gender=['male'],team1=[],team2=[],startdate="2005-02-17",enddate= datetime.datetime.now().strftime ("%Y-%-m-%d")): 
		
		with open(get_data('matches.csv'), 'r') as f:
			reader = csv.reader(f)
			result = list(reader)
			l = []
			for r in result:
				mt,comp,g,t1,t2,d = r[1],r[2],r[3],r[4],r[5],r[7]
				dc = {'id':r[0],'mtype':mt,'competition':comp,'gender':g,'team1':t1,'team2':t2,'venue':r[6],'date':r[7]}

				if mt in mtype and g in gender and d >= startdate and d <= enddate:
					if comp in competition:
						if team1:
							if team2:
								if (t1 in team1 and t2 in team2) or (t1 in team2 and t2 in team1):
									l.append(dc)
							else:
								if t1 in team1 or t1 in team2:
									l.append(dc)
						else:
							l.append(dc)
					else:
						if team1:
							if team2:
								if (t1 in team1 and t2 in team2) or (t1 in team2 and t2 in team1):
									l.append(dc)
							else:
								if t1 in team1 or t1 in team2:
									l.append(dc)
						else:
							l.append(dc)
		return l
					

	def scorecard(self,matchid):
		cnt = 0
		for subdir, dirs, files in os.walk(get_data('data')):
			for file in files:
				path = subdir + "/" + file
				mid = file.split('.')[0]
				if(matchid == mid):
					content = open(path)
					soup = BeautifulSoup(content,"lxml")
					data = {}
					match = {}
					info = soup.find('info')
					teams = info.find('teams').find_all('team')
					team1 = teams[0].get_text()
					team2 = teams[1].get_text()
					mtype = info.find('match_type').get_text()
					venue = info.find('venue').get_text()
					try:
						city = info.find('city').get_text()
					except:
						city = ""
					date = info.find('dates').find('date').get_text()
					innings = soup.find('innings').find_all('inning')
					try:
						pp = info.find('player_of_match').find('player_of_match').get_text()
					except:
						pp = ""
					try:
						comp = info.find('competition').get_text()
					except:
						comp = ""
					gender = info.find('gender').get_text()
					match['teams'] = str(team1 + " vs " + team2)
					match['mtype'] = str(mtype)
					if city:
						match['city'] = str(city)
					match['date'] = str(date)
					if venue:
						match['venue'] = str(venue)
					if pp:
						match['mom'] = str(pp)
					match['id'] = mid
					data['matchinfo'] = match
					inning_list = []
					for inning in innings:
						dinning = {}
						deliveries = inning.find('deliveries').find_all('delivery')
						cnt = 0
						ino = int(inning.find('inningsnumber').get_text())
						bat_team = inning.find('team').get_text()
						bowl_team = team1
						if bat_team == team1:
							bowl_team = team2
						bat = OrderedDict()
						bowl = OrderedDict()
						total = 0
						total_overs = 0
						total_wickets = 0
						over_runs = 0
						balls = 0
						maiden = 0
						over_no = 0
						for d in deliveries:
							batsman = d.find('batsman').get_text()
							bowler = d.find('bowler').get_text()
							non_striker = d.find('non_striker').get_text()
							bruns = int(d.find('runs').find('batsman').get_text())
							truns = int(d.find('runs').find('total').get_text())
							over = int(d.find('over').get_text())
							wide = 0
							noball = 0
							bye = 0
							legbye = 0
							
					
							if d.find('extras') is not None:
								if d.find('extras').find('wides') is not None:
									wide = 1
								if d.find('extras').find('noballs') is not None:
									noball = 1
								if d.find('extras').find('byes') is not None:
									bye = 1
								if d.find('extras').find('legbyes') is not None:
									legbye = 1
							if batsman not in bat:
								bat[batsman] = {'runs':0,'balls':0,'fours':0,'six':0,'dismissal':'not out'}
							if non_striker not in bat:
								bat[non_striker] = {'runs':0,'balls':0,'fours':0,'six':0,'dismissal':'not out'}
							if bowler not in bowl:
								bowl[bowler] = {'overs':0,'maiden':0,'runs':0,'wickets':0}
							bat[batsman]['runs'] += bruns
							if wide == 0:
								bat[batsman]['balls'] += 1
							if bruns == 4:
								bat[batsman]['fours'] += 1
							if bruns == 6:
								bat[batsman]['six'] += 1
							total += truns
							if bye == 1 or legbye == 1:
								over_runs += bruns
								bowl[bowler]['runs'] += bruns
							else:
								over_runs += truns
								bowl[bowler]['runs'] += truns
							if wide == 0 and noball == 0:
								cnt += 1
								balls += 1
								bowl[bowler]['overs'] += 1
							if balls == 6:
								total_overs += 1
								over_no += 1
								if over_runs == 0:
									maiden = 1
								over_runs = 0
								bowl[bowler]['maiden'] += maiden
								maiden = 0
								balls = 0
							
							if d.find('wickets') is not None:
								s = ""
								w = d.find('wickets').find('wicket')
								if w.find('kind'):
									s = s + w.find('kind').get_text() + " "
								if w.find('fielders'):
									s = s + w.find('fielders').find('fielder').get_text() + " "
								if w.find('kind').get_text() != 'run out':
									if w.find('kind').get_text() != 'bowled' and w.find('kind').get_text() != 'hit wicket':
										s = s + "bowled" + " " +  bowler
									else:
										s = s + bowler
									bowl[bowler]['wickets'] += 1
								player_out = w.find('player_out').get_text()
								bat[player_out]['dismissal'] = str(s)
								total_wickets += 1

						if balls != 0:
							total_overs = float(str(total_overs) + "." + str(balls))

						dinning['runs'] = total
						dinning['wickets'] = total_wickets
						dinning['batteam'] = str(bat_team)
						dinning['bowlteam'] = str(bowl_team)
						dinning['inning_no'] = ino
						dinning['overs'] = total_overs

						x = {}
						x['batting'] = (self.convert(bat))
						x['bowling'] = (self.convert(bowl))
						x['summary'] = dinning
						inning_list.append(x)

						
					data['innings'] = inning_list
					return data
					


