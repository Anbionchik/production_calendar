from django.shortcuts import render
from django.utils.safestring import mark_safe
import calendar


def main_view(request):
    year = calendar.HTMLCalendar(firstweekday=0)
    htmlcalendarik = year.formatyear(2020, width=3)
    context = {
        'calendarik': mark_safe(htmlcalendarik),
    }
    return render(request, 'index.html', context)

