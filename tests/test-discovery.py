#!/usr/bin/env python3
"""隔离验证原资源发现函数；仅把两个固定site路径映射进私有目录，不修改生产文件。

这是发现/选择契约测试，不冒充生产site部署；实际backend只读bind另由真实wrapper验证。
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

SITES = ('/usr/local/share/taffish/resources/plink2', '/opt/taffish/resources/plink2')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prepared(path, label):
    member = path / 'synthetic-v1'
    member.mkdir(parents=True)
    (member / 'tiny.txt').write_text(label + '\n')
    receipt = dict(id='synthetic-v1', version='1', source='synthetic contract fixture',
                   license='CC0 synthetic', files=[dict(name='tiny.txt', bytes=(member/'tiny.txt').stat().st_size,
                   sha256=digest(member/'tiny.txt'), url='https://example.invalid/tiny.txt')])
    (member / 'receipt.json').write_text(json.dumps(receipt) + '\n')
    sums = ''.join(digest(member / name) + '  ' + name + '\n' for name in ('receipt.json', 'tiny.txt'))
    (member / 'SHA256SUMS').write_text(sums)
    (member / 'READY').write_text(digest(member/'SHA256SUMS') + '\n')
    return path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--main',type=Path,default=Path(__file__).resolve().parents[1]/'src/main.taf')
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    source=a.main.read_text()
    prefix, tag = source.split('<taf-app:container:',1)
    assert prefix.startswith('<shell>\n') and 'taf_plink2_mount' in tag
    function=prefix.removeprefix('<shell>\n')
    assert all(function.count(s)==1 for s in SITES)
    names=['none','opt-only','usr-over-opt','personal-over-sites','override-over-all',
           'bad-personal-no-fallback','bad-usr-no-fallback','dangling-usr-no-fallback',
           'empty-override','missing-override','disable-invalid','bad-switch',
           'personal-symlink','usr-symlink','space-usr','corrupt-usr-no-fallback',
           'empty-family-no-fallback','colon-path','comma-path']
    rows=[]
    for backend in ('docker','podman','apptainer'):
        for name in names:
            case=a.out.resolve()/(backend+'-'+name)
            case.mkdir(mode=0o700)
            home=case/'home'; home.mkdir()
            personal=home/'.local/share/taffish/resources/plink2'
            usr=case/'usr-local-resources'; opt=case/'opt-resources'
            mapped=function.replace(SITES[0],shlex.quote(str(usr))).replace(SITES[1],shlex.quote(str(opt)))
            assert mapped.replace(shlex.quote(str(usr)),SITES[0]).replace(shlex.quote(str(opt)),SITES[1])==function
            env={k:v for k,v in os.environ.items() if not k.startswith('TAFFISH_PLINK2_RESOURCE_')}
            env['HOME']=str(home)
            expected=None; invalid=False; disabled=False
            if name not in ('none','bad-switch','colon-path','comma-path'):
                prepared(opt,'opt'); expected=opt
            if name not in ('none','opt-only','bad-switch','colon-path','comma-path'):
                prepared(usr,'usr'); expected=usr
            if name in ('personal-over-sites','override-over-all'):
                prepared(personal,'personal'); expected=personal
            if name=='override-over-all':
                expected=prepared(case/'explicit','explicit'); env['TAFFISH_PLINK2_RESOURCE_PATH']=str(expected)
            if name=='bad-personal-no-fallback':
                personal.mkdir(parents=True); (personal/'bad').write_text('not prepared'); invalid=True
            if name in ('bad-usr-no-fallback','corrupt-usr-no-fallback','disable-invalid'):
                (usr/'synthetic-v1/tiny.txt').write_text('changed'); invalid=True
            if name in ('dangling-usr-no-fallback','usr-symlink','space-usr'):
                moved=case/('actual resource space' if name=='space-usr' else 'actual-usr')
                usr.rename(moved)
                usr.symlink_to(case/'missing' if name=='dangling-usr-no-fallback' else moved)
                invalid=name=='dangling-usr-no-fallback'; expected=moved
            if name=='personal-symlink':
                personal.parent.mkdir(parents=True); personal.symlink_to(usr); expected=usr
            if name=='empty-override': env['TAFFISH_PLINK2_RESOURCE_PATH']=''; invalid=True
            if name=='missing-override': env['TAFFISH_PLINK2_RESOURCE_PATH']=str(case/'missing'); invalid=True
            if name=='disable-invalid': env['TAFFISH_PLINK2_RESOURCE_AUTO_MOUNT']='0'; invalid=False; disabled=True
            if name=='bad-switch': env['TAFFISH_PLINK2_RESOURCE_AUTO_MOUNT']='invalid'; invalid=True
            if name=='empty-family-no-fallback':
                empty=case/'empty-family'; empty.mkdir(); (empty/'.partial-kept').mkdir()
                personal.parent.mkdir(parents=True); personal.symlink_to(empty); invalid=True
            if name in ('colon-path','comma-path'):
                expected=prepared(case/('bad:path' if name=='colon-path' else 'bad,path'),'bad-path')
                env['TAFFISH_PLINK2_RESOURCE_PATH']=str(expected); invalid=True
            script=mapped+'\ntaf_plink2_mount '+shlex.quote(backend)+'\n'
            run=subprocess.run(['sh','-c',script],env=env,capture_output=True,text=True,timeout=20)
            want='--taf-plink2-invalid-resource' if invalid else (
                '--env=TAFFISH_ENV=TAFFISH' if disabled or expected is None else
                ('--bind=' if backend=='apptainer' else '--volume=')+str(expected.resolve())+':/references:ro')
            ok=run.returncode==0 and run.stdout==want
            if invalid: ok=ok and ('invalid/unprepared' in run.stderr or 'must be 0 or 1' in run.stderr)
            row=dict(case=name,backend=backend,exit=run.returncode,stdout=run.stdout,stderr=run.stderr,
                     expected=want,passed=ok,source_sha256=digest(a.main),
                     function_sha256=hashlib.sha256(function.encode()).hexdigest(),
                     only_site_literals_mapped=True,production_site_deployment=False)
            rows.append(row)
            (a.out/'receipt.json').write_text(json.dumps(rows,indent=2))
            print(backend,name,'PASS' if ok else 'FAIL',flush=True)
            assert ok,row
    print('PASS',len(rows),'isolated discovery contract checks')

if __name__=='__main__': main()
