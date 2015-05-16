# vim: set fileencoding=utf-8 :
from itertools import dropwhile, takewhile
import subprocess


def memoize(func):
    _table = {}
    def wrapped(*args, **kwargs):
        if args not in _table:
            _table[args] = func(*args, **kwargs)
        return _table[args]
    return wrapped


@memoize
def man(cmd):
    """Get man page as a chunk of utf-8 text"""
    try:
        return subprocess.check_output(['man', cmd]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return ''


def capture_paragraph_from_lines(lines):
    blank = lambda line: line.strip() == ''
    not_blank = lambda line: not blank(line)
    return takewhile(not_blank, dropwhile(blank, lines))


def get_para_of_option(option, man):
    """
    >>> option = '-a'
    >>> man = '''-a
        stuff, description
    '''
    >>> get_para_of_option(option, man)
    ['-a', '   stuff, description']
    """
    lines = man.split('\n')
    begins_with = lambda l: l.strip().startswith(option)
    irrelevant = lambda l: not begins_with(l)
    return capture_paragraph_from_lines(dropwhile(irrelevant, lines))


def help_me_man(cmd, option):
    if not cmd:
        return ''

    man_page = man(cmd)
    if not man_page:
        return ''

    if not option:
        return man_page

    para = get_para_of_option(option, man_page)
    return '\n'.join(para)
