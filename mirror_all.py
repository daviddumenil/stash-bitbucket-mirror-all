#!/usr/bin/python
#
# @author Jason LeMonier
# @author David Dumenil
#
# Mirror ALL Projects & Repositories for a given stash url to another git server
#
# Loop through all projects: [P1, P2, ...]
#    P1 > for each project make a directory with the key "P1"
#    Then clone every repository inside of directory P1
#    Then mirror up to the remote repo
#    Backup a directory, create P2, ...
#
# Added ACTION_FLAG bit so the same logic can run fetch --all on every repository and/or clone.

import sys
import os
import stashy

ACTION_FLAG = 1     # Bit: +1=Clone, +2=fetch --all

url  = os.environ["STASH_URL"]  # "https://mystash.com/stash"
user = os.environ["STASH_USER"] # joedoe"
pwd  = os.environ["STASH_PWD"]  # Yay123
part_to_change  = os.environ["STASH_URL_PART_TO_CHANGE"]  # mystash.com
part_to_replace_with  = os.environ["STASH_URL_PART_TO_REPLACE_WITH"]  # mynewstash.com


stash = stashy.connect(url, user, pwd)

def mkdir(xdir):
    if not os.path.exists(xdir):
        os.makedirs(xdir)

def run_cmd(cmd):
    print ("Directory cwd: %s "%(os.getcwd() ))
    print ("Running Command: \n    %s " %(cmd))
    os.system(cmd)

start_dir = os.getcwd()

for project in stash.projects:
    pk = project_key = project["key"]
    mkdir(pk)
    os.chdir(pk)

    for repo in stash.projects[project_key].repos.list():
        for url in repo["links"]["clone"]:
            href = url["href"]
            repo_dir = href.split("/")[-1].split(".")[0]

            if (url["name"] == "http"):
                print ("        url.href: %s"% href)  # https://joedoe@mystash.com/stash/scm/app/ae.git
                print ("Directory cwd: %s Project: %s"%(os.getcwd(), pk))

            if not os.path.exists(repo_dir):
                run_cmd("git clone --mirror %s" % url["href"])
                # chdir into directory "ae" based on url of this repo, fetch, chdir back
                cur_dir = os.getcwd()
                os.chdir(repo_dir)
                run_cmd("git fetch --prune")
                mirror_url = string.replace(url["href"], part_to_change, part_to_replace_with)
                run_cmd("git push --mirror %s" % mirror_url)
                os.chdir(cur_dir)
            else:
                print ("Directory: %s/%s exists already. Skipping clone. "%(os.getcwd(), repo_dir))

        break

    os.chdir(start_dir) # avoiding ".." in case of incorrect git directories
