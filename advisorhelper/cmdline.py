import argparse

import sys

import os

from advisorhelper.commands.create_algorithm import Command


def execute():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-A", "--algorithm", help="create a new algorithm")
    group.add_argument("-M", "--model", help="create a new model")
    parser.add_argument("-p", "--path", help="specify the path you want to create the algorithm")
    args = parser.parse_args()

    if (not args.algorithm) and (not args.model):
        print("error: need to use flag -A or -M")
        sys.exit(1)

    # check whether the path is valid
    if args.path:
        if not os.path.isdir(args.path):
            print('error: not a valid path')
            sys.exit(1)
        path = args.path
    else:
        path = os.getcwd()

    # create new algorithm
    if args.algorithm:
        print(path)
        cmd = Command(args.algorithm, path)
        cmd.run()

    # create new model
    if args.model:
        print(args.model)


if __name__ == "__main__":
    execute()
