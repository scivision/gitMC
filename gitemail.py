#!/usr/bin/env python
"""
report author emails for all repos under root.
Important for being sure your contributions are plotted in Github (non-registered emails do not plot).

To keep email privacy, use githubusername@users.noreply.github.com
"""
import subprocess as S
from colorama import init,Fore,Back
#
from pygitutils import codepath

def gitemail():

    rdir = codepath()

    cmd=['git','log','--pretty="%ae %ce"']

    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    for d in dlist:
        try:
            ret = S.check_output(cmd,  cwd=str(d)).decode('utf8')
            ret = ret.replace('"','')
            uniq_emails = set(ret.split('\n'))

            print(Back.MAGENTA + str(d))
            print(Back.BLACK + '\n'.join(list(uniq_emails)))
        except S.CalledProcessError as e:
            print('{}  {}'.format(d,e))

if __name__ == '__main__':

    gitemail()



