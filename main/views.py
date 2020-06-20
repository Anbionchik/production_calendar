from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from django.utils.safestring import mark_safe
from main.calendar_files.files_handler import uploaded_file_check, rewrite
import calendar
from main.calendar_files.calendar_xml_handler import calendar_xml_handler
import pickle


def main_view(request):
    with open('C:/Users/Андрей/PycharmProjects/production_calendar/main/calendar_files/presented_years.txt', 'rb+') as file_with_years:
        v = pickle.load(file_with_years)
        context = {
            'years': v,
        }
    return render(request, 'index.html', context)


def show_year_view(request, pk):
    year = pk
    weekends_list = calendar_xml_handler(year)
    work_calendar = ProductionCalendar(firstweekday=0, weekends_list=weekends_list)
    htmlcalendarik = work_calendar.formatyear(year, width=3)
    context = {
        'calendarik': mark_safe(htmlcalendarik),
    }
    return render(request, 'year.html', context)


def upload_new_year_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            force_upload = request.POST.get('force')
            result = uploaded_file_check(request.FILES['file'], force_upload)
            if result:
                return HttpResponse(result)
        return HttpResponse("Успешно")
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})


class ProductionCalendar(calendar.HTMLCalendar):

    def __init__(self, weekends_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weekend_days = {}
        for _ in weekends_list:
            self.weekend_days[_.get('d')] = _.get('t')
        self.weekends_list = weekends_list

    def formatday(self, day, weekday, themonth):
        """
        Return a day as a table cell.
        """
        check = '%02i.%02i' % (themonth, day)
        if check in self.weekend_days:
            id_day = self.weekend_days[check]
        elif weekday in (5, 6):
            id_day = 4
        else:
            id_day = 0

        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            return '<td class="%s" id="%s">%d</td>' % (self.cssclasses[weekday], id_day, day)

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s" id="selectable">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, themonth))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatweek(self, theweek, themonth):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, themonth) for (d, wd) in theweek)
        return '<tr id="selectable">%s</tr>' % s
