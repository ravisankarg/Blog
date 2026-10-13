#!/usr/bin/env python3
"""Read-only GitHub inventory discovery. Does not curate, publish, or remove posts."""
import argparse,json,subprocess
from datetime import datetime,timezone
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--owner',default='ravisankarg')
p.add_argument('--output',type=Path,default=Path('research/discovery/repositories.json'))
p.add_argument('--from-json',type=Path,help='Validate/normalize an existing raw GitHub list or saved inventory offline')
a=p.parse_args()
if a.from_json:
    raw=json.loads(a.from_json.read_text());repos=raw['repositories'] if isinstance(raw,dict) else raw
else:
    repos=[];page=1
    while True:
        result=subprocess.run(['gh','api',f'users/{a.owner}/repos?per_page=100&page={page}&sort=updated'],capture_output=True,text=True)
        if result.returncode:raise SystemExit('GitHub discovery failed; existing catalogue unchanged. '+result.stderr.strip())
        batch=json.loads(result.stdout)
        if not isinstance(batch,list):raise SystemExit('Unexpected GitHub inventory response')
        repos.extend(batch)
        if len(batch)<100:break
        page+=1
fields=['name','html_url','description','fork','has_pages','homepage','pushed_at','default_branch','visibility']
public=[{k:r.get(k) for k in fields} for r in repos if not r.get('private',False) and r.get('visibility','public')=='public' and r.get('owner',{}).get('login',a.owner)==a.owner]
if not public:raise SystemExit('Empty public inventory; refusing to overwrite discovery output')
if len({r['name'] for r in public})!=len(public):raise SystemExit('Duplicate repositories in discovery response')
payload={'checkedAt':datetime.now(timezone.utc).isoformat(),'owner':a.owner,'repositories':public}
a.output.parent.mkdir(parents=True,exist_ok=True)
temp=a.output.with_suffix('.tmp');temp.write_text(json.dumps(payload,indent=2)+'\n');temp.replace(a.output)
root=Path(__file__).resolve().parents[1]
old=root/'research/repository-inventory.json'
if old.exists():
    before={r['name']:r for r in json.loads(old.read_text())['repositories']};after={r['name']:r for r in public}
    print('Added:',', '.join(sorted(after.keys()-before.keys())) or 'none')
    print('Absent (review; do not delete automatically):',', '.join(sorted(before.keys()-after.keys())) or 'none')
    print('Changed:',', '.join(n for n in sorted(before.keys()&after.keys()) if any(before[n].get(k)!=after[n].get(k) for k in fields)) or 'none')
print(f'{len(public)} public repositories saved to {a.output}. Review their contents and live pages before changing posts.json.')
