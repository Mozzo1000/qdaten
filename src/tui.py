from prompt_toolkit.application import Application
from prompt_toolkit.widgets import (
    Box,
    Frame,
    Label,
    TextArea,
)
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout import ScrollablePane
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.key_binding import KeyBindings
import humanize
import datetime as dt
import time
from prettytable import from_db_cursor
import sqlite3
from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous

kb = KeyBindings()
style = Style.from_dict(
    {
        "status": "reverse",
        "shadow": "bg:#440044",
    }
)


class TUI:
    def __init__(self, args, db):
        self.args = args
        self.db = db
        self.input = TextArea(multiline=False, accept_handler=self.on_enter_input,focusable=True, focus_on_click=True)
        self.textarea = TextArea(text="", focusable=True, focus_on_click=True, scrollbar=True)
        self.statusbar_text_right = ""
        root_container = HSplit(
            [
                ScrollablePane(
                    HSplit(
                        [
                        Frame(
                            title=self.db.filename,
                            body=self.textarea,
                            height=D,
                        ),
                        ]
                    )
                ),
                Frame(
                    body=self.input,
                    height=3,
                ),
                VSplit(
                    [
                        Window(
                            FormattedTextControl(lambda: self.statusbar_text_right),
                            align=WindowAlign.RIGHT,
                            style="class:status.right",
                            height=1
                        )
                    ],
                )
            ]
        )

        kb.add("tab")(focus_next)
        kb.add("s-tab")(focus_previous)

        self.application = Application(
            layout=Layout(root_container, focused_element=self.input),
            key_bindings=kb,
            mouse_support=True,
            full_screen=True,
            style=style
        )
        if not args.no_default_query:
            self.show_first_table_contents()
    
    def run(self):
        self.application.run()

    def on_enter_input(self, buff):
        if buff.text:
            if self._builtin_commands(buff.text):
                self._builtin_commands(buff.text)
            else:
                try:
                    _start_execute_time = time.time()
                    self.db.cur.execute(buff.text)
                    table = from_db_cursor(self.db.cur)
                    self.textarea.text = table.get_string()
                    self.statusbar_text_right = f"Returned {len(table.rows)} row(s) in {self._exec_time_format(time.time() - _start_execute_time)}"
                except sqlite3.OperationalError as error:
                    self.textarea.text = f"Invalid SQL\n {error}"

    def show_first_table_contents(self):
        _start_execute_time = time.time()
        self.db.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        first_table = self.db.cur.fetchone()[0]
        self.db.cur.execute(f"SELECT * FROM {first_table}")
        table = from_db_cursor(self.db.cur)
        self.textarea.text = table.get_string()
        self.statusbar_text_right = f"Returned {len(table.rows)} row(s) in {self._exec_time_format(time.time() - _start_execute_time)}"


    @kb.add("c-c")
    def _(event):
        "Pressing Ctrl-C will exit the user interface."
        event.app.exit()
    
    def _exec_time_format(self, seconds):
        if seconds >= 60:
            return humanize.naturaldelta(dt.timedelta(seconds=seconds))
        else:
            return f"{round(seconds, 2)} seconds"

    def _builtin_commands(self, inp):
        if inp == "exit":
            get_app().exit()
        elif inp == ".tables":
            self.show_tables()
            return True
        elif inp == ".save":
            new_db = sqlite3.connect(f"{self.db.filename}.db")
            self.db.con.backup(new_db)
            new_db.close()
            self.statusbar_text_right = f"Saved to {self.db.filename}.db"
            return True
