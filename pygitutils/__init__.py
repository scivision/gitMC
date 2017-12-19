"""
NOTE: cwd=str() is for Python 3.5 compatibility e.g. Raspberry Pi. Perhaps remove in 2018 when Raspbian is updated to Python 3.6 default.
"""
from pathlib import Path
from sys import stderr
import colorama
import subprocess
from random import randrange
from time import sleep
#%%
def gitemail(path:Path, user:str, exclude:list=None):
    if (path/'.nogit').is_file():
        return

    cmd=['git','log','--pretty="%ce"']

    ret = subprocess.check_output(cmd, cwd=str(path)).decode('utf8')
    ret = ret.replace('"','')
    ret = filter(None,ret.split('\n')) # remove blanks
    emails = set(ret)
    if exclude:
        emails = emails.difference(set(exclude))
# %%
    emails = list(emails)
    if not (len(emails)==1 and not user!=emails[0].split('@')[0]):
        if str(path) != '.':
            print(colorama.Back.MAGENTA + str(path))

        print(colorama.Back.BLACK + '\n'.join(list(emails)))

    return emails


def codepath():
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('codepath',help='path to code root',
                   nargs='?', default='~/code')
    p = p.parse_args()

    rdir = Path(p.codepath).expanduser()

    return rdir

def fetchpull(mode='fetch'):

    rdir = codepath()

    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    print('git',mode,len(dlist),'paths under',rdir)
    failed=[]
    for d in dlist:
        if (d/'.nogit').is_file(): #user requesting this directory not to be synced
            continue

        print(' -->',d.name,end="",flush=True)
        try:
            # don't use timeout as it doesn't work right when waiting for user input (password)
            subprocess.check_output(['git',mode], cwd=str(d))
            print('\r',end="")
        except subprocess.CalledProcessError:
            failed.append(d.name)

        sleep(randrange(10)*.1 +1 )  # don't hammer the remote server, delay of 1-2 seconds

    print()
    if failed:
        print('git',mode,'ERROR under',rdir, file=stderr)
        # no backslash allowed in f-stringss
        print('\n'.join(failed), file=stderr)

    return failed
