#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from distutils.core import setup

LONG_DESC ='''When running certain commands from the shell, e.g. grep, it can be pretty hard to remember what a certain argument does. (how does the --exclude option for grep work?)

One way is to fire up man, look for the argument, exit the pager, and continue typing. That's just distracting.

Another way is to fire up a tmux pane at the side, look up the argument, switch back to your original pane, and continue. This is slightly better, but when you need to look up multiple arguments it can be quite a hassle switching panes constantly.'''

setup(
    name='helpmeman',
    version='0.0.1',
    description='Run commands with instant lookup of what arguments mean from the man pages',
    long_description=LONG_DESC,
    author='Ng Zhi An',
    author_email='ngzhian@gmail.com',
    url='https://github.com/ngzhian/help-me-man',
    packages=['helpmeman'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Documentation',
    ],
    entry_points='''
    [console_scripts]
    helpmeman=helpmeman.helpmeman:main
    ''',
)
