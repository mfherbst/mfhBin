#!/usr/bin/env python3

import email
import imaplib
import ssl
import subprocess
import os
import time
import yaml


def pass_get_password(passpath):
    """
    Run pass to get the password at a particular passpath
    """
    out = subprocess.check_output(["pass", "show", passpath],
                                  universal_newlines=True)
    return out.split("\n")[0]


def notify_alert_message(alertmail):
    """
    Take an alertmail and send a message to the user.
    """
    body = ""
    for entry in alertmail.get_payload():
        body += entry.as_string()

    command = [
        "notify-send", "--icon", "error", "--urgency", "critical",
        "--expire-time", "0", alertmail["subject"], body
    ]
    subprocess.call(command)


def get_alert_mails(server, user, password, only_unseen=False, delete_seen=False):
    """
    Login to the imap server and return all alert emails.

    only_unseen    If true only return unseen alert emails
    """
    imap = imaplib.IMAP4(server)
    context = ssl.create_default_context()
    imap.starttls(ssl_context=context)

    imap.login(user, password)
    imap.select()

    # Search for relevant messages
    query = "ALL"
    if only_unseen:
        query = "(UNSEEN)"
    typ, data = imap.search(None, query)

    # Yield those where the subject matches
    include = ["[!]", "alert"]   # Match keywords
    exclude = ["resolve"]      # Exclude keywords (higher preference)
    for num in data[0].split():
        typ, data = imap.fetch(num, '(RFC822)')
        message = email.message_from_string(str(data[0][1], "utf-8"))

        subject = message["subject"].lower()
        if any(k in subject for k in include) and \
           not any(k in subject for k in exclude):
            yield message

            imap.store(num, "+FLAGS", "\\Seen")
            if delete_seen:
                imap.store(num, "+FLAGS", "\\Deleted")

    imap.close()
    imap.logout()


def execute_watch_loop(config, watch_pid=None):
    """
    The loop which does the actual work.

    If watch_pid is given the process will exit, when this
    pid is gone.
    """
    if config["password"].startswith("@pass"):
        passpath = config["password"][5:].strip()
        password = pass_get_password(passpath)
    else:
        password = config["password"]

    alert_action = notify_alert_message
    if config["alert_action"] != "notify-send":
        raise SystemExit("The only supported alert action is 'notify-send'")

    # Fork into background
    if os.fork() != 0:
        raise SystemExit()

    if watch_pid:
        def keep_running():
            try:
                os.kill(watch_pid, 0)
                return True
            except ProcessLookupError:
                return False
    else:
        def keep_running():
            return True

    while keep_running():
        alerts = get_alert_mails(config["server"], config["user"], password,
                                 only_unseen=config["only_unseen"],
                                 delete_seen=config["delete_seen"])

        for msg in alerts:
            alert_action(msg)

        time.sleep(config["interval"])


def dump_default_config(path):
    config = {
        "server":          "mail.example.com",
        "user":            "john-doe",
        "password":        "mypass",
        "interval":        60,
        "only_unseen":     True,
        "delete_seen":     False,
        "alert_action":    "notify-send",
    }
    with os.open(path, "w") as cfg:
        yaml.safe_dump(config, cfg)


def main():
    configfile = "~/.mfhBin/watch_monitoring_alert_mails.yaml"
    configfile = os.path.expanduser(configfile)

    if not os.path.exists(configfile):
        dump_default_config(configfile)
        raise SystemExit("Config file not found. Default configuration dumped at '" +
                         configfile + "'.")

    with open(configfile, "r") as cfg:
        config = yaml.safe_load(cfg)
    execute_watch_loop(config)


if __name__ == "__main__":
    main()
