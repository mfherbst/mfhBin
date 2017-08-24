#!/usr/bin/env python3

import argparse
try:
    from passlib.hash import bcrypt
    from passlib.hash import apr_md5_crypt
except ImportError as e:
    raise SystemExit("htpasswd.py requires the python modules passlib and"
                     " bcrypt to be installed. On Debian and Ubuntu run \n"
                     "'apt-get install python3-passlib python3-bcrypt'")


def password_interactive():
    import getpass

    # Prompt for password:
    pass1 = 1
    pass2 = 2
    while pass1 != pass2:
        if pass1 != 1:
            print("Passwords did not match. Try again.")
        pass1 = getpass.getpass("Enter password:  ")
        pass2 = getpass.getpass("Repeat password: ")
    return pass1


def get_args():
    """
    Parse the commandline arguments and return the args object.
    """
    parser = argparse.ArgumentParser(
        description="Small python implementation of htpasswd. "
        "See https://httpd.apache.org/docs/current/programs/htpasswd.html "
        "for more details."
    )

    algo = parser.add_mutually_exclusive_group(required=True)
    algo.add_argument("-m", dest="algo", action="store_const", const=apr_md5_crypt,
                      help="Use apache's MD5 to store the password")
    algo.add_argument("-B", dest="algo", action="store_const", const=bcrypt,
                      help="Use bcrypt to store the password")
    algo.add_argument("-d", dest="algo", action="store_const", const=None,
                      help="Use crypt() to store the password.")
    algo.add_argument("-s", dest="algo", action="store_const", const=None,
                      help="Use SHA to store the password.")
    algo.add_argument("-p", dest="algo", action="store_const", const=None,
                      help="Use plaintext passwords.")

    parser.add_argument("-C", dest="bcrypt_cost", type=int, default=None,
                        help="Specify the cost for the bcrypt algorithm."
                        "Valid range is from 4 to 31, default is 12.",
                        choices=range(4, 32))

    file_action = parser.add_mutually_exclusive_group()
    file_action.add_argument("-D", dest="delete_user", default=False,
                             action="store_true",
                             help="Delete the user if it is found.")
    file_action.add_argument("-v", dest="verify_user", default=False,
                             action="store_true",
                             help="Verify the password of a user.")

    operation_mode = parser.add_mutually_exclusive_group()
    operation_mode.add_argument("-b", dest="operation_mode", action="store_const",
                                const="batch",
                                help="Batch mode: Get passwords from commandline.")
    operation_mode.add_argument("-i", dest="operation_mode", action="store_const",
                                const="stdin",
                                help="Read the password from stdin.")

    file_mode = parser.add_mutually_exclusive_group()
    file_mode.add_argument("-c", dest="file_mode", action="store_const",
                           const="create",
                           help="Create a file with the given entry. If the file "
                           "already exists it is overwritten silently.")
    file_mode.add_argument("-n", dest="file_mode", action="store_const",
                           const="stdout",
                           help="Just display the outcome on the screen and do "
                           "not create any passwdfile.")

    parser.add_argument("username",
                        help="The username to put into the passwd file.")
    # parser.add_argument("passwdfile", help="The password file to work on.")

    #
    # Parse args
    #
    args = parser.parse_args()

    if args.operation_mode is None:
        args.operation_mode = "interactive"
    if args.file_mode is None:
        args.file_mode = "append"

    if args.algo is None:
        raise SystemExit("The password storage algorithm you chose is not yet "
                         "supported. Most likely this is because it is insecure "
                         "and hence deprecated anyway.")

    if args.operation_mode == "batch":
        raise SystemExit("Batch mode (-b) is not supported, since it is insecure.")
    if args.operation_mode == "stdin":
        raise SystemExit("Stdin mode (-i) is not yet supported.")
    if args.file_mode == "append":
        raise SystemExit("Append mode is not yet supported. Specifý '-n' on the "
                         "commandline.")
    if args.file_mode == "create":
        raise SystemExit("Create mode (-c) is not yet supported.")
    if args.verify_user or args.delete_user:
        raise SystemExit("Deleting (-D) or verifying (-v) a user is not yet "
                         "supported.")

    if args.bcrypt_cost:
        if args.algo != bcrypt:
            raise SystemExit("Const (-C) can only be specified if bcrypt is "
                             "selected as algorithm.")
        else:
            args.algo = args.algo.using(rounds=args.bcrypt_cost)

    return args


def hash_password(pw, algo):
    # encrypt is deprecated in the newer versions
    # of passlib, so we fall back to it only if needed.
    if hasattr(algo, "hash"):
        return algo.hash(pw)
    else:
        return algo.encrypt(pw)


def main():
    # That simple for now:

    args = get_args()
    pw = password_interactive()
    print(args.username + ":" + hash_password(pw, args.algo))


if __name__ == "__main__":
    main()
