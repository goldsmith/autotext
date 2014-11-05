import os
import re
import string

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

[
  [{'Othello': 'foo\n bar'}, {'Desdemona': ['boo', 'har']}], # ACT 1
  [],
  [],
  []
]

acts = []
for i, act in enumerate(act_scenes_text):
  acts.append([])

  for j, scene in enumerate(act):
    acts[i].append(defaultdict(str))

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

      acts[i][j][character] += unpunctuate(rest_of_line).strip().lower() + ' '

NGRAM_SIZE = 3
connections = defaultdict(set)
def ngrams(input, n):
  input = input.split(' ')
  output = []
  for i in range(len(input)-n+1):
    output.append(' '.join(input[i:i+n]))
  return output

for i, act in enumerate(acts):
  for j, scene in enumerate(act):
    for character, lines in scene.iteritems():
      for ngram in ngrams(lines, NGRAM_SIZE):
        connections[ngram].add(
          'Act %s Scene %s' % (i+1, j+1)
        )

# # clean out boring words
# for combo in itertools.product(STOPWORDS, repeat=NGRAM_SIZE):
#   stupid_thing = ' '.join(combo)
#   if stupid_thing in connections:
#     del connections[stupid_thing]

for text, scenes in sorted(connections.iteritems(), key=lambda x: len(x[1])):
  if len(scenes) > 1:
    print text, scenes

