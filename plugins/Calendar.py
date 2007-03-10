import calendar, copy
from cherrypy import expose
from datetime import date
from FileCabinet import get_entries_by_date
from utils import configMap

class Calendar(object):
    def __init__(self, parent):
        self.now = date.today()
        self.monthname = self.now.strftime('%B')
        self.cal = calendar.monthcalendar(self.now.year, self.now.month)
        self.parent = parent

    @expose
    def index(self):
        cal = copy.deepcopy(self.cal)
        cal = self.get_entry_dates(self.now.month, self.now.year, cal)
        return self.render_calendar(self.monthname, self.now.month, self.now.year, cal)

    def get_entry_dates(self, month, year, cal):
        entryDays = set()
        entries = get_entries_by_date(year, month)
        for e in get_entries_by_date(year, month):
            entryDays.add(e.time_tuple[2])
        for week in cal:
            for i in range(0, 7):
                #days are a tuple of (day #, hasEntry?)
                if week[i] in entryDays:
                    week[i] = (week[i], True)
                else:
                    week[i] = (week[i], False)
        return cal

    #Add the rendered calendar to the template variables
    #def cb_add_data(self):
    #    if configMap.get('calendar') and configMap['calendar'].get('show'):
    #        cal = copy.deepcopy(self.cal)
    #        cal = self.get_entry_dates(self.now.month, self.now.year, cal)
            

    def render_calendar(self, monthname, month, year, calendar):
        conf = configMap['cherryblossom'].copy()
        conf.update({'monthname': monthname,
            'month': month,
            'year': year,
            'cal': calendar})
        return [('head', conf),
            ('browse', conf),
            ('foot', conf)]

    def default(self):
        pass
