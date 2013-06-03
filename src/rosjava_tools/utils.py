#!/usr/bin/env python
#
# License: Apache 2.0
#   https://raw.github.com/ros-java/rosjava_core/hydro-devel/rosjava_tools/LICENSE
#

##############################################################################
# Imports
##############################################################################

import os
import errno
import pwd

##############################################################################
# Methods
##############################################################################


def which(program):
    '''
      Looks for program in the environment.

      @param program : string name of the program (e.g. 'ls')
      @type str
      @return absolute pathname of the program or None
      @rtype str or None
    '''
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, unused_fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


def author_name():
    """
    Utility to compute logged in user name

    :returns: name of current user, ``str``
    """
    import getpass
    name = getpass.getuser()
    try:
        login = name
        name = pwd.getpwnam(login)[4]
        name = ''.join(name.split(','))  # strip commas
        # in case pwnam is not set
        if not name:
            name = login
    except:
        #pwd failed
        pass
    if type(name) == str:
        name = name.decode('utf-8')
    return name


def mkdir_p(path):
    '''
      Enables mkdir -p functionality (until python 3.2 is able to use
      the mode argument to do the same).
    '''
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise    os.mkdir(os.path.join(path, 'src', 'main', 'java'))


def validate_path(path):
    '''
      Validates that there isn't a gradle project in the specified path.
      We use this when creating an android repo/package.

      @param path : path where you wish to create the repository/package.
      @type str
      @raise RuntimeError
      @return path : validated (exists) absolute pathname
    '''
    if not os.path.isabs(path):
        absolute_path = os.path.join(os.getcwd(), path)
    else:
        absolute_path = path
    if not os.path.exists(absolute_path):
        os.mkdir(absolute_path)
    else:
        if os.path.isfile(os.path.join(path, 'build.gradle')):
            raise ValueError("Error: a gradle project already resides in this location [%s]" % absolute_path)
    return absolute_path