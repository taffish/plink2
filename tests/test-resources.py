#!/usr/bin/env python3
"""对固定成员安装契约做离线负向/恢复测试，不冒充生产下载。"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

helper = sys.argv[1]
with tempfile.TemporaryDirectory(prefix='plink2-resource-test-') as td:
    t = Path(td)
    payload = b'resource fixture\n'
    m = dict(id='tiny-v1', version='1', source='synthetic fixture', license='CC0 synthetic', files=[dict(name='tiny.txt',url='https://example.invalid/tiny',sha256=hashlib.sha256(payload).hexdigest(),bytes=len(payload))])
    catalog=t/'catalog.json'; catalog.write_text(json.dumps(dict(schema=1,members=[m])))
    root=t/'root'; root.mkdir()
    cases=[]
    def run(label, tail, code=0, marker=None):
        r=subprocess.run([sys.executable,helper,*tail],text=True,capture_output=True)
        ok=(r.returncode==code if code==0 else r.returncode!=0) and (marker is None or marker in r.stdout+r.stderr)
        cases.append(dict(label=label,exit=r.returncode,passed=ok,stdout=r.stdout,stderr=r.stderr))
        print(json.dumps(cases[-1]),flush=True)
        assert ok,label
    args=['--catalog',str(catalog),'--resource-root',str(root),'--member','tiny-v1']
    run('dry-run', ['install',*args,'--dry-run'])
    run('selector-required',['install','--catalog',str(catalog),'--dry-run'],1,'--member is required')
    run('missing-root',['install',*args[:-2],'--resource-root',str(t/'absent'),'--member','tiny-v1'],1,'existing actual')
    key=hashlib.sha256(json.dumps(m,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    stage=root/('.partial-'+key); stage.mkdir(mode=0o700)
    (stage/'tiny.txt').write_bytes(payload)
    lock=open(root/'.plink2-resources.lock','w'); fcntl.flock(lock,fcntl.LOCK_EX)
    run('lock-refusal',['install',*args],1,'locked')
    lock.close()
    run('verified-cache-promote',['install',*args],marker='INSTALLED')
    target=root/'tiny-v1'
    assert target.stat().st_mode & 0o777 == 0o755
    assert all(f.stat().st_mode & 0o777 == 0o644 for f in target.iterdir())
    run('verify',['verify',*args],marker='VERIFIED')
    run('idempotent',['install',*args],marker='VERIFIED')
    (target/'tiny.txt').write_bytes(b'x'*len(payload))
    run('same-size-corrupt',['verify',*args],1,'mismatch')
    run('no-overwrite-corrupt',['install',*args],1,'mismatch')
    (target/'tiny.txt').write_bytes(payload)
    (target/'extra').write_text('unexpected')
    run('extra-file',['verify',*args],1,'unexpected')
    (target/'extra').unlink()
    (target/'tiny.txt').unlink(); (target/'tiny.txt').symlink_to(catalog)
    run('symlink-file',['verify',*args],1,'mismatch')
    (target/'tiny.txt').unlink(); (target/'tiny.txt').write_bytes(payload)
    (target/'receipt.json').write_text('{}')
    run('wrong-receipt',['verify',*args],1,'receipt')
    # URL/size/hash validation must precede network or install.
    for field,value in [('url','http://example.invalid/tiny'),('bytes',0),('sha256','bad'),('name','../escape')]:
        bad=json.loads(json.dumps(m)); bad['files'][0][field]=value
        catalog.write_text(json.dumps(dict(schema=1,members=[bad])))
        run('reject-'+field,['install',*args,'--dry-run'],1)
    print('PASS',len(cases),'resource contract tests')
