# vim: set fileencoding=utf-8 :
from __future__ import absolute_import

import urwid
import urwid.raw_display
import urwid.web_display

from entry import get_command_and_last_arg
from man import help_me_man


def edit_handler(dest, widget, newtext):
    """Handler called whenever the edit box changes"""
    cmd, arg = get_command_and_last_arg(newtext)
    help_text = help_me_man(cmd, arg)
    dest.set_text(help_text)


def main():
    text_header = (
        u"F1 exits. Up/Down arrow to change focus, Pg Up/Down to scroll")
    man_output = urwid.Text(
        u"Start typing shell command, e.g. cat. "
        u"This will recognize arguments like -h, --help.")

    edit = urwid.Edit('>>> ')

    # impt: connect changes in the edit line to man output
    key = urwid.connect_signal(
        edit, 'change', edit_handler, weak_args=[man_output])

    footer = urwid.AttrWrap(urwid.Text(text_header), 'footer')
    listbox = urwid.ListBox(urwid.SimpleListWalker([man_output]))
    body = urwid.Pile([
         ('fixed', 2, urwid.Filler(edit)),
         ('weight', 70, listbox),
        ])
    frame = urwid.Frame(urwid.AttrWrap(body, 'body'), footer=footer)

    palette = [
        ('editfc','white', 'dark blue', 'bold'),
        ('editbx','light gray', 'dark blue'),
        ('editcp','black','light gray', 'standout'),
        ('footer','white','dark red', 'bold'),
    ]

    screen = urwid.raw_display.Screen()

    def unhandled(key):
        if key in ['f1']:
            raise urwid.ExitMainLoop()

    urwid.MainLoop(frame, palette, screen,
        unhandled_input=unhandled).run()

if __name__ == '__main__':
    main()
