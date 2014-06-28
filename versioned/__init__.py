""" Versioned.

Usage:
    versioned [<dest>] <src> -sndc

Options:
    -s --max-size <size>        Prune old versions once the directory grows over a certain size.
    -n --max-snapshots <n>      ...
    -d --max-days <days>        ...
    -c --save-configuration     ...

- if dest exists and is a versioned directory (assessed by the presence of a latest.ext file), apply any housekeeping that's required (pruning old versions)
- if dest exists and is a file, move it to a same-named versioned directory
- if anything is passed on stdin, this becomes the latest version
- versioned will look for .versioned in that directory, which optionally contains housekeeping rules
versioned <src> <dest>
- same mechanics
"""

import os
from datetime import datetime, timedelta
import functools
from dateutil.parser import parse as dateparse
from docopt import docopt


def to_args(obj):
    lines = map(' '.join, obj.items)
    return '\n'.join(lines)

def from_args(str):
    lines = str.strip().split('\n')
    pairs = map(lambda line: line.split(' ', 1), lines)
    return dict(pairs)

def dump_args(obj, f):
    f.write(to_ini(obj))
    f.close()

def load_args(f):
    obj = from_ini(f.read())
    f.close()
    return obj

def get_configuration(options):
    config = os.path.join(dest, '.versioned')
    if os.path.exists(config):
        defaults = load_args(config)
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
    files = [f for f in files os.listdir(path) if os.isfile(f)]
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

def version(dest, src=None):
    dest, extension = os.path.splitext(dest)
    is_versioned = os.path.exists(os.path.join(dest, 'latest' + extension))
    now = datetime.now().replace(microsecond=0).isoformat()    

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Versioned 0.1')
    
