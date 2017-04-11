#!/usr/bin/env python3
import subprocess
import sys
import json
import argparse

class config:
    tag_to_symbol={
        "mail": "",
        "web": "",
        "code": "",
        "notes": "",
        "film": "",
        "music": "",
    }

    # What separates the number from the tags
    separator=" "

# ------------------------------------------------------

# TODO Make a workspace class?
def i3_workspaces():
    """Get the parsed output of i3-msg's get_workspaces"""
    invocation=["i3-msg", "-t", "get_workspaces"]
    out = subprocess.check_output(invocation)
    return json.loads(out.decode('utf-8'))

def workspace_focused():
    """ Get the focused workspace structure """
    wks=[ w for w in i3_workspaces() if w['focused'] ]
    if len(wks) > 1:
        raise SystemExit("More than one focused workspace?")
    else:
        return wks[0]

def workspace_from_num(num):
    """ Get the workspace structure of workspace num"""
    wks=[ w for w in i3_workspaces() if w['num'] == num]
    if len(wks) > 1:
        raise SystemExit("Number " + str(num) + " assigned to more than one workspace")
    else:
        return wks[0]

def workspace_rename(work, newname):
    """ Rename a workspace """
    invocation=["i3-msg", "rename", "workspace", '"'+work["name"]+'"', "to", '"'+newname+'"']
    out=subprocess.check_output(invocation)
    js = json.loads(out.decode('utf-8'))
    if not js[0]['success']:
        SystemExit("Renaming was not successful")

def workspace_get_symbols(work):
    """ Parse workspace symbols assigned by this script """
    splitted = work['name'].split(config.separator)
    if len(splitted) > 1:
        return [ c for c in splitted[1]]
    else:
        return []

def workspace_set_symbols(work, symbols):
    """ Set a particular set of symbols to a workspace """
    name=str(work['num'])
    if symbols:
        name+=config.separator+"".join(symbols)
    workspace_rename(work,name)

def main():
    parser = argparse.ArgumentParser(description="Add tags to an i3 workspace")
    parser.add_argument("--workspace", metavar='num', type=int, help="The workspace to tag")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--clear", action='store_true', default=False, help="Clear all tags")
    group.add_argument("--add", metavar='tag', nargs='+', type=str, help='Add a list of tags to a workspace')
    group.add_argument("--set", metavar='tag', nargs='+', type=str, help='Set a single tag to a workspace')

    # Parse args
    args = parser.parse_args()

    # Determine info of workspace act upon
    if (args.workspace):
        work = workspace_from_num(args.workspace)
    else:
        work = workspace_focused()

    symbols=workspace_get_symbols(work)
    try:
        if args.add:
            symbols+=[ config.tag_to_symbol[t] for t in args.add
                       if (not config.tag_to_symbol[t] in symbols) ]
        elif args.set:
            symbols=[ config.tag_to_symbol[t] for t in args.set ]
        elif args.clear:
            symbols=[]
    except KeyError as e:
        raise SystemExit("Unknown tag: " + str(e.args[0]) + ". Valid are:\n  "
                         + " ".join(config.tag_to_symbol.keys()))

    workspace_set_symbols(work,symbols)

#--------------------

if __name__ == "__main__":
    main()

