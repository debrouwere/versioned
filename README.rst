Versioned v0.1
==============

Versioning is a user-friendly interface to a very common way of
versioning files, which creates a snapshot on every save, using
hardlinks, with ``latest.ext`` always referring to the latest version
and other versions named according to when they were created.

You can use it on the command line or from Python.

**Status:** unstable.

Usage:

::

    versioned (init | update) <dest> [options]
    versioned rm <dest> [options]
    versioned ls <dest> [options]
    versioned <dest> [<src>] [options]

Options:

::

    -s --max-size <size>        Prune old snapshots to keep the directory under a certain size.
    -n --max-snapshots <n>      Prune snapshots beyond the latest <n>.
    -d --max-days <days>        Prune snapshots older than <days>.
    -r --range <range>...       List snapshots in a range. Get the latest snapshot using `head`, 
                                a range of older snapshots using `-5 -2`, snapshots that are
                                between a certain age using `-9d -4d` and snapshots from a 
                                certain year, month or day using `2014`, `2014-05` and so on.
    -k --keep                   When adding a file from <src> to the versioned directory, 
                                also keep the file in its original location.

Arguments: The path to either the versioned directory or the file you
wish to start versioning. The path to the file that should be

When initializing a versioned directory, you should refer to it with the
desired extension of the files that it will contain at the end.
``example.txt`` will result in a versioned directory called ``example``
being created, and all the files therein will have the ``.txt``
extension. From then on, you can refer to your versioned directory with
or without extension tacked on.
