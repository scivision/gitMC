from __future__ import print_function
from platform import system
import os
import subprocess as S
from random import randrange
from time import sleep
#%%
try:
    from pathlib import Path
    Path().expanduser()
except (ImportError,AttributeError):
    from pathlib2 import Path
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

    print('git {} {} paths under {}'.format(mode,len(dlist),rdir))
    failed=[]
    for d in dlist:
        try:
            ret = S.check_output(['git',mode], cwd=str(d))
            if ret:
                print(' --> {}'.format(d.name))
                print(ret.decode('utf8'))
            else:
                print(d.name)
        except S.CalledProcessError:
            failed.append(d)

        sleep(randrange(10)*.1) # don't hammer the remote server, delay of 0-1 second

    if failed:
        print('git {} ERROR: \n{}'.format(mode,
                          '\n'.join([str(f) for f in failed])))

    return failed