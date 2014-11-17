#!/usr/bin/env python3

from __future__ import print_function
import argparse
import os
import sys


def main(argv=sys.argv[1:]):
    """
    Get the package names in an isolated install space in topological order.
    """
    parser = argparse.ArgumentParser(
        description='Find all package names in an isolated install space and '
                    'order them topologically based on the run dependencies',
    )
    parser.add_argument(
        'root',
        help='The root of the isolated install space',
    )
    args = parser.parse_args(argv)

    package_names = [d for d in os.listdir(args.root)
                     if os.path.isdir(os.path.join(args.root, d))]
    run_dependencies = {}
    for pkg_name in package_names:
        run_dependencies[pkg_name] = []
        marker_file = os.path.join(
            args.root, pkg_name, 'share', 'ament_index', 'resource_index',
            'package_run_dependencies', pkg_name)
        if os.path.exists(marker_file):
            with open(marker_file, 'r') as h:
                run_dependencies[pkg_name] = \
                    [d for d in h.read().split(';') if d in package_names]

    # select packages with no dependencies in alphabetical order
    to_be_ordered = list(package_names)
    ordered = []
    while to_be_ordered:
        pkg_name_without_deps = [
            name for name in to_be_ordered if not run_dependencies[name]]
        if not pkg_name_without_deps:
            assert False
        pkg_name_without_deps.sort()
        pkg_name = pkg_name_without_deps[0]
        to_be_ordered.remove(pkg_name)
        ordered.append(pkg_name)
        # remove item from dependency lists
        for k in list(run_dependencies.keys()):
            if pkg_name in run_dependencies[k]:
                run_dependencies[k].remove(pkg_name)

    for name in ordered:
        print(name)


if __name__ == '__main__':
    main()