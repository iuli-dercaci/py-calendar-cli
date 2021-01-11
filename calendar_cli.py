import time
from os import system, name
from datetime import datetime
from pynput.keyboard import Listener, Key
from keyboard_watcher import on_key_press, on_key_release
from month_calendar import MonthCalendar


def clear():
    system('cls' if name == 'nt' else 'clear')


def show_logo():
    phrase = 'Calendar CLI'
    curr_phrase = ''
    for _, curr_char in enumerate(phrase):
        curr_phrase += curr_char
        clear()
        print(curr_phrase)
        time.sleep(0.03)
    time.sleep(0.5)
    clear()


@on_key_press('left', 'right')
def on_press(key):
    if key == Key.left:
        month_calendar.prev_month()
    elif key == Key.right:
        month_calendar.next_month()

    clear()
    month_calendar.show_calendar()


@on_key_release('esc')
def on_release(key):
    return False


with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


if __name__ == '__main__':
    selected_date = datetime.now()
    month_calendar = MonthCalendar(selected_date)
    month_calendar.show_calendar()
