from feeds import fetch,run
from engine import Flag,decide
from collections import Counter

def acquire():
    source=fetch('https://api.github.com/events?per_page=100')
    source=dict(source,payload=[{key:event[key] for key in ('id','type','repo','created_at')} for event in source['payload']])
    return {'sources':[source]}


def analyze(snapshot):
    events=snapshot['sources'][0]['payload']
    repos=sorted({e['repo']['name'] for e in events})
    small=Flag('event-enrichment',1,25)
    large=Flag('event-enrichment',2,50)
    rows=[{'repository':repo,'at_25_percent':decide(small,repo)['enabled'],
           'at_50_percent':decide(large,repo)['enabled'],'decision':decide(large,repo)} for repo in repos]
    return {'project':'RolloutLab','real_repositories':len(repos),
            'enabled_at_25_percent':sum(r['at_25_percent'] for r in rows),
            'enabled_at_50_percent':sum(r['at_50_percent'] for r in rows),
            'cohort_preserved':all(not r['at_25_percent'] or r['at_50_percent'] for r in rows),
            'decisions':rows[:30]}


if __name__=='__main__': run(acquire,analyze)
