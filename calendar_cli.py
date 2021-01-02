import calendar
import time
import numpy as np
from os import system, name
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from pynput.keyboard import Listener, Key
from rich import box
from rich.console import Console
from rich.table import Table
from keyboard_watcher import on_key_press, on_key_release


def clear():
    system('cls' if name == 'nt' else 'clear')


def last_day_of_month(curr_year, curr_month):
    d_last = calendar.monthrange(curr_year, curr_month)[-1]
    return date(curr_year, curr_month, d_last)


def get_last_days_of_prev_month(target_first_datetime, amount):
    result = []
    last_date = (target_first_datetime - timedelta(days=1)).day
    for val in range(amount):
        result.append(last_date)
        last_date -= 1
    return result


def get_first_days_of_next_month(last_weekday):
    return [i for i in range(last_weekday, 7)]


def get_next_month_begin_start(np_dates, last_day):
    last_day_idx = np.where(np_dates == last_day)[0].item(0)
    week_idx = last_day_idx[0].item(0)
    last_day_idx = last_day_idx[1].item(0)

    if last_day_idx == 6:
        return None

    return week_idx, last_day_idx + 1


def assemble_calendar():
    selected_year = selected_date.year
    selected_month = selected_date.month
    now = datetime.now()
    day_now = now.day if now.month == selected_month and now.year == selected_year else None

    calendar.setfirstweekday(0)
    month_dates = np.array(calendar.monthcalendar(selected_year, selected_month)).flatten()
    colors = np.zeros(month_dates.size)
    if day_now is not None:
        day_now_idx = np.where(month_dates == day_now)[0].item(0)
        np.put(colors, day_now_idx, 1)

    # append days from the next month
    last_day_date = last_day_of_month(selected_year, selected_month)
    last_day_idx = np.where(month_dates == last_day_date.day)[0].item(0)
    next_day = 1
    for idx in range(last_day_idx + 1, month_dates.size):
        month_dates[idx] = next_day
        colors[idx] = -1
        next_day += 1

    # prepend days from the previous month
    first_day_date = datetime(selected_year, selected_month, 1)
    prepend_days = get_last_days_of_prev_month(first_day_date, first_day_date.weekday())
    for idx, day in enumerate(prepend_days):
        month_dates[idx] = day
        colors[idx] = -1

    weeks_qty = int(month_dates.size / 7)
    month_dates = month_dates.reshape((weeks_qty, 7))
    colors = colors.reshape((weeks_qty, 7))

    return month_dates, colors


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


def output_result(arr):
    for el in arr:
        print(el)


def add_color(colours_arr, r_idx, c_idx, val):
    color_name = num_to_color(colours_arr[r_idx, c_idx])
    return f'[{color_name}]{val}'


def num_to_color(num):
    if num == -1:
        return 'grey39'
    elif num == 0:
        return 'grey100'
    else:
        return 'red1'


def show_calendar():
    console = Console()

    current_date_label = Table.grid()
    current_date_label.add_column(justify='center', style='grey35')
    current_date_label.add_row(f'{selected_date.strftime("%b, %Y"):^32}')

    num_rows, _ = month.shape
    list_of_days = [day for day in calendar.day_abbr]

    table = Table(show_lines=True, box=box.SIMPLE)

    for header_el in list_of_days:
        table.add_column(header_el, justify="center", no_wrap=True)

    for row_idx in range(num_rows):
        data = [add_color(color, row_idx, idx, x) for idx, x in enumerate(month[row_idx])]
        table.add_row(*data)

    controls = Table.grid()
    controls.add_column(justify='left', style='green', no_wrap=True)
    controls.add_column(justify='center', style='red', no_wrap=True)
    controls.add_column(justify='right', style='green', no_wrap=True)
    controls.add_row('<-- prev' + ' ' * 8, 'ESQ exit', ' ' * 8 + 'next -->')

    console.print(current_date_label)
    console.print(table)
    console.print(controls)


@on_key_press('left', 'right')
def on_press(key):
    global selected_date, month, color
    if key == Key.left:
        selected_date -= relativedelta(months=1)
    elif key == Key.right:
        selected_date += relativedelta(months=1)

    clear()
    month, color = assemble_calendar()
    show_calendar()


@on_key_release('esc')
def on_release(key):
    return False


selected_date = datetime.now()
month, color = assemble_calendar()

if __name__ == '__main__':
    show_logo()
    show_calendar()


with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()