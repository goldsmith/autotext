import os
import re
import string
import json

from collections import defaultdict
import itertools

with open(os.path.abspath('./othello.txt'), 'r') as f:
  text = f.read()

with open(os.path.abspath('./stopwords.txt'), 'r') as f:
  STOPWORDS = set(map(lambda s: s.strip(), f.readlines()))

PUNCTUATION = set(string.punctuation)
ACT_SPLIT_RE = r'Actus\s+\w+\.\s+'
SCENE_SPLIT_RE = r'(Scoena|Scena|Scaena)\s+\w+\.\s+'
START_OF_LINE_RE = r'(\w+)\. '
CHARACTER_NICKNAMES = {
  'Clo': 'Clown',
  'Mus': 'Musicians',
  'Iag': 'Iago',
  'Messen': 'Messenger',
  'Othel': 'Othello',
  'Lodoui': 'Lodovico',
  'Aemi': 'Emilia',
  'aemil': 'Emilia',
  'Gra': 'Gratiano',
  'Cassi': 'Cassio',
  'Oth': 'Othello',
  'Bianca': 'Bianca',
  'Lodo': 'Lodovico',
  'Lod': 'Lodovico',
  'Men': 'Messenger',
  'Rodorigo': 'Rodorigo',
  'Iago': 'Iago',
  'Cas': 'Cassio',
  'Othello': 'Othello',
  'Mon': 'Montano',
  'Emil': 'Emilia',
  'Othe': 'Othello',
  'Gent': 'Gentlemen',
  'Des': 'Desdemona',
  'Herald': 'Herald',
  'Rodor': 'Rodorigo',
  'Mont': 'Montano',
  'Desde': 'Desdemona',
  'Officer': 'Officer',
  'Aem': 'Emilia',
  'Duke': 'Duke',
  'All': 'All',
  'Monta': 'Montano',
  'Rodo': 'Rodorigo',
  'Rod': 'Rodorigo',
  'Bian': 'Bianca',
  'Clow': 'Clown',
  'Cassio': 'Cassio',
  'Aemil': 'Emilia',
  'Ia': 'Iago',
  'Sen': 'Senator',
  'Bra': 'Brabrantio',
  'Within': 'Within'
}
CHARACTER_IS_MALE = {
  'Clown': True,
  'Musicians': True,
  'Iago': True,
  'Messenger': True, 
  'Othello': True,
  'Lodovico': True,
  'Emilia': False,
  'Gratiano': True,
  'Cassio': True,
  'Bianca': False,
  'Rodorigo': True,
  'Montano': True,
  'Gentlemen': True,
  'Desdemona': False,
  'Herald': True,
  'Officer': True,
  'Duke': True,
  'All': True,
  'Senator': True,
  'Within': False,
  'Brabrantio': True
}
SCENES_PER_ACT = {
  1: 3,
  2: 3,
  3: 4,
  4: 3,
  5: 2
}
STAGE_DIRECTIONS = ('Exeunt.', 'Exeunt')

def unpunctuate(s):
  return ''.join(ch for ch in s if ch not in PUNCTUATION)

acts_text = re.split(ACT_SPLIT_RE, text)[1:] # remove stuff at top of .txt
assert len(acts_text) == 5

act_scenes_text = [
  filter(lambda match: match not in (None, '', 'Scena', 'Scoena', 'Scaena'), re.split(SCENE_SPLIT_RE, act_text))
  for act_text in acts_text
]

for i, act in enumerate(act_scenes_text):
  print 'Act', i+1, 'Length', len(act)

acts = []
for i, act in enumerate(act_scenes_text):
  acts.append([])

  for j, scene in enumerate(act):
    acts[i].append(defaultdict(int))

    for line in scene.split('\r\n\r\n'):
      line = line.strip()

      match = re.match(START_OF_LINE_RE, line)
      if match is None:
        # probably stage direction or something
        continue

      character_nickname = match.groups()[0]
      if character_nickname in STAGE_DIRECTIONS:
        continue

      character = CHARACTER_NICKNAMES[character_nickname]
      rest_of_line = ''.join(re.split(START_OF_LINE_RE, line)[2:])

      acts[i][j][character] += 1

def scene_index(act, scene):
  index = 0
  for act_index in range(1, act):
    index += SCENES_PER_ACT[act_index]
  return index + scene

assert scene_index(1, 1) == 1
assert scene_index(2, 1) == 4
assert scene_index(4, 2) == 12

def generate_jobs_data():
  jobs_data = []
  for i, act in enumerate(acts):
    for j, scene in enumerate(act):
      total_lines = float(sum(scene.values()))
      for character in set(CHARACTER_NICKNAMES.values()):
        jobs_data.append({
          "job": character,
          "year": scene_index(i + 1, j + 1),
          "count": scene[character],
          "perc": scene[character] / total_lines,
          "sex": "men" if CHARACTER_IS_MALE[character] else "women"
        })
  return jobs_data

with open(os.path.abspath('./data.json'), ('r+')) as f:
  json.dump(generate_jobs_data(), f, indent=4, separators=(',', ': '))
  
