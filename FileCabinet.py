import os, time, datetime, re
import cherrypy as cpy
from Entry import Entry

ENTRIES = {}
SORTED_ENTRIES = []
NOW = datetime.datetime.now
LAST_UPDATE = NOW()

def get_most_recent(datadir, n=None, ignore_directories=(), offset=0):
    """returns the most recent n entries from the datadir"""
    global SORTED_ENTRIES, ENTRIES, LAST_UPDATE

    #Caching sucks right now! Turned off until I at least have an admin 
    #interface. Turned back on because it's severely slower on the front page.
    #
    #just for reference: on my localhost, removing the cache doubles the page 
    #build time as reported by cherrypy, but only from .008 to .016 (tested 
    #on /code.html)
    #Unfortunately, the front page goes from ~.01 to about .1
    if not ENTRIES or (NOW()-LAST_UPDATE).seconds > 1800:
    #if 1:
        ENTRIES, SORTED_ENTRIES = {}, {}
        scan_for_entries(datadir, ignore_directories, datadir)
        SORTED_ENTRIES = [entry[1] for entry in
                  reversed(sorted([(e.time, e) for e in ENTRIES.itervalues()]))]
        LAST_UPDATE = NOW()

    if not n:
        return SORTED_ENTRIES
    else:
        return SORTED_ENTRIES[offset:offset+n]

def scan_for_entries(curdir, ignore_dirs, basedir):
    """recursively scans directories for entries"""
    if os.path.isdir(curdir):
        for file in os.listdir(curdir):
            cpy.log("Scanned file %s" % file)
            f = os.path.join(curdir, file)
            if os.path.isdir(f) and not os.path.basename(f) in ignore_dirs:
                scan_for_entries(f, ignore_dirs, basedir)
            elif f.endswith('.txt'):
                e = Entry(f, basedir)
                ENTRIES[e.relpath] = e
    else:
        cpy.log("Entries dir not found: %s" % curdir)

def get_all(datadir):
    """returns all entries"""
    return get_most_recent(datadir)

def get_one(fname, datadir):
    """given a relative path, return the entry or none"""
    return ENTRIES.get(fname, None)

def get_entries_by_date(year, month='', day=''):
    """returns a list of entry objects"""
    cpy.log("date: %s %s %s" % (year, month, day))
    if not month and not day:
        res = [(e.time, e) for e in SORTED_ENTRIES if e.time_tuple[0] == year]
    elif not day:
        res = []
        for e in SORTED_ENTRIES:
            y, m = e.time_tuple[:2]
            if y == year and m == month:
                res.append((e.time, e))
    else:
        res = []
        for e in SORTED_ENTRIES:
            y, m, d = e.time_tuple[:3]
            if y == year and m == month and d == day:
                res.append((e.time, e))
    if not res:
        return self.error_page("No stories found at this date")
    return [r[1] for r in res]

def get_entries_by_meta(key):
    """return all entries which have key as a metadata key"""
    return [e for e in SORTED_ENTRIES if key in e.metadata]
