# vim: set fileencoding=utf-8 :
from itertools import dropwhile, takewhile

is_dash = lambda c: c == '-'
is_blank = lambda c: c == ' '
not_blank = lambda c: not is_blank(c)
incomplete = lambda c: is_dash(c) or is_blank(c)

def current_command(line):
    """
    >>> current_command('man abc')
    'man'
    >>> current_command('  man abc')
    'man'
    """
    return ''.join(takewhile(not_blank, line.lstrip()))

def current_argument(line):
    """
    >>> current_argument('man')
    ''
    >>> current_argument('man -c')
    '-c'
    >>> current_argument('man -c asdf')
    '-c'
    >>> current_argument('man --ch')
    '--ch'
    >>> current_argument('man --ch -')
    '--ch'
    """
    def drop_arg_and_shorten(line, arg=''):
        return ''.join(dropwhile(incomplete, line[len(arg):]))

    def get_arg(line):
        if not line:
            return ''
        arg = ''.join(takewhile(not_blank, line))
        if arg.endswith('-'):
            # since it was reversed, undo that reverse to make it right
            return arg[::-1]
        else:
            return get_arg(drop_arg_and_shorten(line, arg))

    # takes care of incomplete arguments, e.g. trailing spaces, dashes
    # NOTE that string is reverse!
    return get_arg(drop_arg_and_shorten(line[::-1]))


def get_command_and_last_arg(line):
    if not line:
        return '', ''

    cmd = current_command(line)
    arg = current_argument(line)
    return cmd, arg


if __name__ == "__main__":
    import doctest
    doctest.testmod()
