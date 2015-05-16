#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
from __future__ import absolute_import
import shlex, subprocess

import urwid
import urwid.raw_display
import urwid.web_display

from helpmeman.entry import get_command_and_last_arg
from helpmeman.man import help_me_man


# we might want to use a custom walker to simplify the logic
# of scrolling to the line we want
class ManWalker(urwid.ListWalker):
    def __init__(self):
        self.man_page = ['asdf'] * 100
        self.focus = (0, 1)

    def _get_at_pos(self, pos):
        return urwid.Text(self.man_page[pos[1]]), pos

    def get_focus(self):
        return self._get_at_pos(self.focus)

    def set_focus(self, focus):
        self.focus = focus
        self._modified()

    def get_next(self, start_from):
        i, j = start_from
        focus = j , j + 1
        return self._get_at_pos(focus)

    def get_prev(self, start_from):
        i, j = start_from
        if i == 0:
            return None, None
        focus = i - 1, i
        return self._get_at_pos(focus)


class ManEditWidget(urwid.Edit):
    def __init__(self, *args, **kwargs):
        super(ManEditWidget, self).__init__(*args, **kwargs)

    def keypress(self, position, key):
        if key == 'enter':
            args = self.get_edit_text()
            subprocess.Popen(
                args,
                stdout=self._pipe,
                shell=True)
            return True
        else:
            return super(ManEditWidget, self).keypress(position, key)

    def set_pipe(self, fd):
        self._pipe = fd


def main():
    text_header = (
        u"F1 exits. Up/Down arrow to change focus, Pg Up/Down to scroll")
    man_output = urwid.Text(
        u"Start typing shell command, e.g. cat. "
        u"This will recognize arguments like -h, --help.")

    # edit = urwid.Edit(('editfc', '>>>'), '')
    edit = ManEditWidget(('editfc', '>>>'), '')

    footer = urwid.AttrWrap(urwid.Text(text_header), 'footer')
    listbox = urwid.ListBox(urwid.SimpleListWalker([man_output]))
    # listbox = urwid.ListBox(ManWalker())
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

    # potentially buggy implementation of scrolling
    def scroll_to_line(line):
        old_inside, total = listbox.inset_fraction
        new_inside = None
        c, r = screen.get_cols_rows()
        if line < old_inside:
            while line < old_inside and old_inside > 0:
                listbox.keypress((c, r), 'up')
                new_inside, total = listbox.inset_fraction
                old_inside = new_inside
        else:
            while old_inside < line - 1 and old_inside != new_inside:
                old_inside = new_inside
                listbox.keypress((c, r), 'down')
                new_inside, total = listbox.inset_fraction

    def edit_handler(dest, widget, newtext):
        """Handler called whenever the edit box changes"""
        cmd, arg = get_command_and_last_arg(newtext)
        # help_text = help_me_man(cmd, arg)
        lineno, man_page = help_me_man(cmd, arg)
        dest.set_text(man_page)
        scroll_to_line(lineno)

    # impt: connect changes in the edit line to man output
    urwid.connect_signal(
        edit, 'change', edit_handler, weak_args=[man_output])

    # this manages page up and page down when user is still typing
    def unhandled(key):
        c, r = screen.get_cols_rows()
        if key in ['f1']:
            raise urwid.ExitMainLoop()
        elif key in ['page up']:
            listbox.keypress((c, r), 'page up')
        elif key in ['page down']:
            listbox.keypress((c, r), 'page down')
        # elif key in ['enter']:
            # raise urwid.ExitMainLoop()

    loop = urwid.MainLoop(frame, palette, screen,
        unhandled_input=unhandled)

    def received_output(data):
        man_output.set_text(data)

    write_fd = loop.watch_pipe(received_output)
    edit.set_pipe(write_fd)

    loop.run()

if __name__ == '__main__':
    main()
