from __future__ import print_function
try:
    from pathlib import Path
    Path().expanduser()
except (ImportError,AttributeError):
    from pathlib2 import Path
#
from sys import stderr
from platform import system
import os
import subprocess as S
from random import randrange
from time import sleep
#%%
def codepath():
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('codepath',help='path to code root',nargs='?')
    p = p.parse_args()

    if p.codepath:
        rdir = Path(p.codepath)
    else:
        # autodetect root directory  c:\code or ~/code  arbitrary choice
        plat = system().lower()
        if plat.startswith('cygwin'): # assume /cygdrive/c, you're welcome to change
            rdir = Path(os.environ['SYSTEMDRIVE'])
        else:
            rdir = Path.home() # windows, not Cygwin and all other OS

        rdir = rdir / 'code'

    return rdir

def fetchpull(mode='fetch'):

    rdir = codepath()

    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    print('git',mode,len(dlist),'paths under',rdir)
    failed=[]
    for d in dlist:
        if (d/'.nogit').is_file(): #user requesting this directory not to be synced
            continue

        try:
            ret = S.check_output(['git',mode], cwd=str(d))
            if ret:
                print(' -->',d.name)
                print(ret.decode('utf8'))
        except S.CalledProcessError:
            failed.append(d)

        sleep(randrange(10)*.1 +1 )  # don't hammer the remote server, delay of 1-2 seconds

    if failed:
        print('git',mode,'ERROR:')
        # no backslash allowed in f-stringss
        print("{}".format('\n'.join([str(f) for f in failed])), file=stderr)

    return failed
