"""Local checkpoint storage only. Does not access a browser or network."""
import argparse, json, re, sqlite3
from pathlib import Path
from urllib.parse import urlparse

FIELDS = ['mim','name_en','name_zh','translation_status','eyes','systemic','genes',
          'molecular_basis_raw','raw_synopsis','source_url','search_url','captured_at','status','notes']

def validate(r):
    if not isinstance(r, dict) or not re.fullmatch(r'\d{6}', str(r.get('mim',''))):
        raise ValueError('A six-digit phenotype MIM number is required')
    if r.get('status') not in ('complete','pending','error'):
        raise ValueError('Invalid status')
    if r['status'] == 'complete':
        for f in FIELDS[:-1]:
            if not isinstance(r.get(f), str) or not r[f].strip():
                raise ValueError(f'{r["mim"]}: missing {f}')
        u = urlparse(r['source_url'])
        if u.scheme != 'https' or u.hostname not in ('omim.org','www.omim.org'):
            raise ValueError('Source must be an observed OMIM HTTPS page')
    return r

def main():
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['ingest','status','export'])
    p.add_argument('db'); p.add_argument('file',nargs='?'); a=p.parse_args()
    if a.action != 'status' and not a.file: p.error('file is required')
    Path(a.db).parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(a.db) as con:
        con.execute('CREATE TABLE IF NOT EXISTS records(mim TEXT PRIMARY KEY, status TEXT NOT NULL, data TEXT NOT NULL)')
        if a.action == 'ingest':
            batch=json.loads(Path(a.file).read_text(encoding='utf-8-sig'))
            if not isinstance(batch,list): raise ValueError('Batch must be an array')
            for r in batch: validate(r)
            with con:
                for r in batch:
                    old=con.execute('SELECT status FROM records WHERE mim=?',(r['mim'],)).fetchone()
                    if old and old[0]=='complete' and r['status']!='complete': continue
                    con.execute('INSERT OR REPLACE INTO records VALUES(?,?,?)',(r['mim'],r['status'],json.dumps(r,ensure_ascii=False)))
        if a.action == 'export':
            rows=[json.loads(x[0]) for x in con.execute('SELECT data FROM records ORDER BY mim')]
            Path(a.file).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
        print(json.dumps(dict(con.execute('SELECT status,count(*) FROM records GROUP BY status')),ensure_ascii=False))

if __name__=='__main__': main()
