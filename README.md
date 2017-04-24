# pycricket
A python API to fetch scorecards of past matches. 

<b>Installation</b>

```python
pip install pycricket
```

<b>Basic usage</b>

```python
from pycricket import cricket
import json
c = cricket.Cricket()
matches = c.query(mtype=['ODI'],team1=['India'],startdate='2017-01-01')
for match in matches:
	scorecard = c.scorecard(match['id'])
	print json.dumps(scorecard,indent=4)
```

By default, query() takes the following parameters:
```python
query(mtype = ['T20','ODI','Test'],competition=[],gender=['male'],team1=[],team2=[],startdate="2005-02-17",enddate= datetime.datetime.now().strftime ("%Y-%-m-%d"))
```
More options:

```python
mtype = ['T20','ODI','Test','ODM','I20']

competition = ['IPL']

gender = ['male','female']

team1 = team2 = ['India','Pakistan','South Africa','West Indies','Zimbabwe','Bangladesh','England','Australia','Ireland','Sri Lanka'] + other cricket playing nations
```

Look into the 'pycricket/matches.csv' file for more options.

Note: The code has not been properly tested yet. Create issues if you find any problems.
