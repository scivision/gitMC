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

    ret = subprocess.check_output(cmd, cwd=path).decode('utf8')
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

        try:
            ret = subprocess.check_output(['git',mode], cwd=d)
            if ret:
                print(' -->',d.name)
                print(ret.decode('utf8'))
        except subprocess.CalledProcessError:
            failed.append(str(d)) # do str() here to avoid awkward print expansion

        sleep(randrange(10)*.1 +1 )  # don't hammer the remote server, delay of 1-2 seconds

    if failed:
        print('git',mode,'ERROR:', file=stderr)
        # no backslash allowed in f-stringss
        print('\n'.join(failed), file=stderr)

    return failed
