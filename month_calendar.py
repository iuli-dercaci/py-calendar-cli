import calendar
import numpy as np
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from rich import box
from rich.console import Console
from rich.table import Table


class MonthCalendar:

    COLOR_DAYS_EXTRA = 'grey39'
    COLOR_DAYS_MAIN = 'grey100'
    COLOR_DAYS_CURRENT = 'red1'

    def __init__(self, selected_date):
        self.selected_date = selected_date
        self.month, self.colors = self.__assemble_calendar()

    def show_calendar(self):
        console = Console()

        current_date_label = Table.grid()
        current_date_label.add_column(justify='center', style='grey35')
        current_date_label.add_row(f'{self.selected_date.strftime("%b, %Y"):^32}')

        num_rows, _ = self.month.shape
        list_of_days = [day for day in calendar.day_abbr]

        table = Table(show_lines=True, box=box.SIMPLE)

        for header_el in list_of_days:
            table.add_column(header_el, justify="center", no_wrap=True)

        for row_idx in range(num_rows):
            data = [self.__add_color(self.colors, row_idx, idx, x) for idx, x in enumerate(self.month[row_idx])]
            table.add_row(*data)

        controls = Table.grid()
        controls.add_column(justify='left', style='green', no_wrap=True)
        controls.add_column(justify='center', style='red', no_wrap=True)
        controls.add_column(justify='right', style='green', no_wrap=True)
        controls.add_row('<-- prev' + ' ' * 9, 'ESQ exit', ' ' * 9 + 'next -->')

        console.print(current_date_label)
        console.print(table)
        console.print(controls)

    def __assemble_calendar(self):
        selected_year = self.selected_date.year
        selected_month = self.selected_date.month
        now = datetime.now()
        day_now = now.day if now.month == selected_month and now.year == selected_year else None

        calendar.setfirstweekday(0)
        month_dates = np.array(calendar.monthcalendar(selected_year, selected_month)).flatten()
        colors = np.zeros(month_dates.size)

        if day_now is not None:
            day_now_idx = np.where(month_dates == day_now)[0].item(0)
            np.put(colors, day_now_idx, 1)

        # append days from the next month
        last_day_date = self.__last_day_of_month(selected_year, selected_month)
        last_day_idx = np.where(month_dates == last_day_date.day)[0].item(0)
        next_day = 1
        for idx in range(last_day_idx + 1, month_dates.size):
            month_dates[idx] = next_day
            colors[idx] = -1
            next_day += 1

        # prepend days from the previous month
        first_day_date = datetime(selected_year, selected_month, 1)
        prepend_days = self.__get_last_days_of_prev_month(first_day_date, first_day_date.weekday())
        for idx, day in enumerate(prepend_days):
            month_dates[idx] = day
            colors[idx] = -1

        weeks_qty = int(month_dates.size / 7)
        month_dates = month_dates.reshape((weeks_qty, 7))
        colors = colors.reshape((weeks_qty, 7))

        return month_dates, colors

    def next_month(self):
        self.selected_date -= relativedelta(months=1)
        self.month, self.colors = self.__assemble_calendar()

    def prev_month(self):
        self.selected_date += relativedelta(months=1)
        self.month, self.colors = self.__assemble_calendar()

    def __last_day_of_month(self, curr_year, curr_month):
        d_last = calendar.monthrange(curr_year, curr_month)[-1]
        return date(curr_year, curr_month, d_last)

    def __get_last_days_of_prev_month(self, target_first_datetime, amount):
        result = []
        last_date = (target_first_datetime - timedelta(days=1)).day
        for val in range(amount):
            result.append(last_date)
            last_date -= 1
        return result

    def __add_color(self, colours_arr, r_idx, c_idx, val):
        num = colours_arr[r_idx, c_idx]

        if num == -1:
            color_name = self.COLOR_DAYS_EXTRA
        elif num == 0:
            color_name = self.COLOR_DAYS_MAIN
        else:
            color_name = self.COLOR_DAYS_CURRENT

        return f'[{color_name}]{val}'
