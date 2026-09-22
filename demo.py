import json
from engine import Flag, decide, experiment

flag = Flag('new-search', version=2, percentage=30, attributes={'plan': 'pro'})
decisions = [decide(flag, f'user-{i}', {'plan': 'pro'}) for i in range(8)]
print(json.dumps({'decisions': decisions, 'experiment': experiment('search-v2', 'user-1', {'control': 50, 'treatment': 50})}, indent=2))
