import curses

stdscr = curses.initscr()

curses.nocbreak()
stdscr.keypad(False)
curses.echo()

curses.endwin()
