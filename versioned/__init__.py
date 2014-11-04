"""
# Versioned v0.1

Versioning is a user-friendly interface to a very common way of versioning files, which 
creates a snapshot on every save, using hardlinks, with `latest.ext` always referring 
to the latest version and other versions named according to when they were created.

You can use it on the command line or from Python.

**Status:** unstable.

Usage:

    versioned (init | update) <dest> [options]
    versioned rm <dest> [options]
    versioned ls <dest> [options]
    versioned <dest> [<src>] [options]

Options:

    -s --max-size <size>        Prune old snapshots to keep the directory under a certain size.
    -n --max-snapshots <n>      Prune snapshots beyond the latest <n>.
    -d --max-days <days>        Prune snapshots older than <days>.
    -r --range <range>...       List snapshots in a range. Get the latest snapshot using `head`, 
                                a range of older snapshots using `-5 -2`, snapshots that are
                                between a certain age using `-9d -4d` and snapshots from a 
                                certain year, month or day using `2014`, `2014-05` and so on.
    -k --keep                   When adding a file from <src> to the versioned directory, 
                                also keep the file in its original location.

Arguments:
    <dest>      The path to either the versioned directory or the file you wish to start versioning.
    <src>       The path to the file that should be 

When initializing a versioned directory, you should refer to it with the desired extension 
of the files that it will contain at the end. `example.txt` will result in a versioned
directory called `example` being created, and all the files therein will have the `.txt`
extension. From then on, you can refer to your versioned directory with or without extension
tacked on.
"""

import sys
import os
import json
from datetime import datetime, timedelta
import functools
from dateutil.parser import parse as dateparse
from docopt import docopt


def set_configuration(target, **options):
    config = os.path.join(target, '.versioned')
    json.dump(options, open(config, 'w'), indent=4)

def get_configuration(target, **options):
    config = os.path.join(target, '.versioned')
    if os.path.exists(config):
        defaults = json.load(open(config))
    else:
        defaults = {}
    defaults.update(options)
    return defaults

def to_date(filename):
    return dateparse(f.splitext()[0])

def is_old(date, days):
    difference = datetime.now() - date
    return difference > timedelta(days=days)

def prune(path, **options):
    config = get_configuration(options)

    # TODO: exclude `latest.ext`!
    files = [f for f in os.listdir(path) if os.isfile(f)]
    matches = [f for f in files if f.endswith(extension)]

    if '--max-snapshots' in options:
        if int(options['--max-snapshots']) < len(matches):
            too_much = len(matches) - int(options['--max-snapshots'])
            for i in range(too_much):
                os.remove(files[i])

    if '--max-size' in options:
        size = [os.path.getsize(f) for f in matches]
        if sum(size) > int(options['--max-size']):
            too_much = int(options['--max-size']) - sum(size)
            will_remove = []
            while sum(will_remove) < too_much:
                will_remove.append(size.pop(0))

            to_remove = matches[:len(will_remove)]
            for f in too_old:
                os.remove(f)

    if '--max-days' in options:
        is_too_old = functools.partial(is_old, days=int(options['--max-days']))
        too_old = [f for f in files if is_too_old(to_date(f))]
        # is it safer to os.join this with the cwd?
        for f in too_old:
            os.remove(f)

    if options['--save-configuration']:
        del options['--save-configuration']
        dump_args(config, open('.versioned', 'w'))


def version(target, source=None):
    config = get_configuration(target)
    now = datetime.now().replace(microsecond=0).isoformat().replace(':', '')

    print 'source', source

    if source:
        source = open(source)
    else:
        source = sys.stdin

    dest = os.path.join(target, now + config['extension'])
    latest = os.path.join(target, 'latest' + config['extension'])

    with open(dest, 'w') as f:
        f.write(source.read())

    if os.path.exists(latest):
        os.remove(latest)

    os.link(dest, latest)

def init(target, size=None, snapshots=None, days=None):
    root, extension = os.path.splitext(target)
    
    if os.path.exists(target):
        is_versioned = os.path.exists(os.path.join(root, '.versioned'))
        if not is_versioned:
            raise Exception("Directory already exists and is not versioned.")
    else:
        os.mkdir(root)

    set_configuration(root, size=size, snapshots=snapshots, days=days, extension=extension)
    return (root, extension)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Versioned 0.1')
    print arguments    

    target = arguments['<dest>']
    source = arguments['<src>']
    days = arguments['--max-days']
    size = arguments['--max-size']
    snapshots = arguments['--max-snapshots']

    if arguments.get('init'):
        init(target, size, snapshots, days)
    else:
        version(target, source)

    # print sys.stdin.isatty()
    # print sys.stdout.isatty()