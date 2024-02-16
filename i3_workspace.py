#!/usr/bin/env python3
import subprocess
import json
import argparse


class config:
    tag_to_symbol = {
        "mail": "",
        "web": "",
        "code": "",
        "notes": "",
        "film": "",
        "music": "",
        "tunnel": "",
        "teaching": "",
        "paperwork": "",
        "admin": "",
        "reading": "",
        "chat": "",
        "paper": "",
        "calculation": "",
    }

    # What separates the number from the symbols
    separator = " "

    # If this is true the workspace number is suppressed
    compressed = False


# TODO Make a workspace class?
def i3_workspaces():
    """Get the parsed output of i3-msg's get_workspaces"""
    invocation = ["i3-msg", "-t", "get_workspaces"]
    out = subprocess.check_output(invocation)
    return json.loads(out.decode('utf-8'))


def workspace_focused():
    """ Get the focused workspace structure """
    wks = [w for w in i3_workspaces() if w['focused']]
    if len(wks) > 1:
        raise SystemExit("More than one focused workspace?")
    else:
        return wks[0]


def workspace_from_num(num):
    """ Get the workspace structure of workspace num"""
    wks = [w for w in i3_workspaces() if w['num'] == num]
    if len(wks) > 1:
        raise SystemExit("Number " + str(num) +
                         " assigned to more than one workspace")
    else:
        return wks[0]


def workspace_rename(work, newname):
    """ Rename a workspace """
    invocation = ["i3-msg", "rename", "workspace", '"'+work["name"]+'"',
                  "to", '"'+newname+'"']
    out = subprocess.check_output(invocation)
    js = json.loads(out.decode('utf-8'))
    if not js[0]['success']:
        SystemExit("Renaming was not successful")


def workspace_get_symbols(work):
    """ Parse workspace symbols assigned by this script """
    return [c for c in work['name']
            if not c.isdigit() and c != config.separator]


def workspace_set_symbols(work, symbols):
    """ Set a particular set of symbols to a workspace """
    name = str(work['num'])

    if symbols:
        if config.compressed:
            name = "".join(symbols)
        else:
            name += config.separator
            name += "".join(symbols)
    workspace_rename(work, name)


def workspace_autodetermine_symbols(work):
    wins = build_workspace_windows_map()[work['num']]

    tags = set()
    for w in wins:
        prop = w['window_properties']

        if 'window_role' in prop:
            role = prop['window_role'].lower()
            if role == 'browser':
                tags.add('web')

        if 'class' in prop:
            clss = prop['class'].lower()

            if clss in ["firefox", "qutebrowser"]:
                tags.add('web')
            elif "thunderbird" in clss:
                tags.add('mail')
            elif "mpv" in clss:
                tags.add('film')

    if not tags:
        raise ValueError("Could not find any tags for this workspace.")

    return [config.tag_to_symbol[t] for t in tags]


def content_tree():
    """ Return the tree of all content windows """
    invocation = ["i3-msg", "-t", "get_tree"]
    out = subprocess.check_output(invocation)
    tree = json.loads(out.decode('utf-8'))
    return [
        window
        for node in tree['nodes']
        for content in node['nodes']
        for window in content['nodes']
        if content['name'] == 'content'
    ]


def build_workspace_windows_map():
    """ Return the mapping from the workspace number
        to the list of window leafs on that workspace """
    def traverse_tree(tree):
        if tree['window']:
            return [tree]
        else:
            return [w for sub in tree['nodes'] for w in traverse_tree(sub)]

    return {win['num']: traverse_tree(win) for win in content_tree()}


def main():
    parser = argparse.ArgumentParser(description="Add tags to an i3 workspace")
    parser.add_argument("--num", metavar='num', type=int,
                        help="The workspace to tag")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--clear-tags", action='store_true', default=False,
                       help="Clear all tags")
    group.add_argument("--add-tags", metavar='tag', nargs='+', type=str,
                       help='Add a list of tags to a workspace')
    group.add_argument("--string-tags", metavar="string", type=str,
                       help="Add an arbitrary string")
    group.add_argument("--remove-tags", metavar='tag', nargs='+', type=str,
                       help='Remove a list of tags from a workspace')
    group.add_argument("--auto-tags", action='store_true', default=False,
                       help="Automatically determine tags for workspace")
    group.add_argument("--set-tags", metavar='tag', nargs='+', type=str,
                       help='Set a single tag to a workspace')
    group.add_argument("--list-tags", action="store_true",
                       default=False, help="List workspace tags and exit")

    # Parse args
    args = parser.parse_args()

    if args.list_tags:
        print("The following tags are known")
        for tag, symbol in config.tag_to_symbol.items():
            print("    {:15s} ( {:2s} )".format(tag, symbol))
        return

    # Determine info of workspace act upon
    if (args.num):
        work = workspace_from_num(args.num)
    else:
        work = workspace_focused()

    def unknown_tag_exit(e):
        raise SystemExit("Unknown tag: " + str(e.args[0]) + ". Valid are:\n  "
                         + " ".join(sorted(config.tag_to_symbol.keys())))

    symbols = workspace_get_symbols(work)
    if args.add_tags:
        try:
            symbols += [config.tag_to_symbol[t] for t in args.add_tags
                        if (not config.tag_to_symbol[t] in symbols)]
        except KeyError as e:
            unknown_tag_exit(e)
    elif args.remove_tags:
        try:
            remsymbols = [config.tag_to_symbol[t] for t in args.remove_tags]
        except KeyError as e:
            unknown_tag_exit(e)
        symbols = [s for s in symbols if s not in remsymbols]
    elif args.set_tags:
        try:
            symbols = [config.tag_to_symbol[t] for t in args.set_tags]
        except KeyError as e:
            unknown_tag_exit(e)
    elif args.clear_tags:
        symbols = []
    elif args.string_tags:
        symbols.append(args.string_tags)
    else:  # args.auto_tags is the default
        try:
            symbols = workspace_autodetermine_symbols(work)
        except ValueError as e:
            raise SystemExit("Could not autodetermine tags for this "
                             "workspace.")

    workspace_set_symbols(work, symbols)


if __name__ == "__main__":
    main()
