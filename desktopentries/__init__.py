import os
from glob import iglob
from future_builtins import map
from ConfigParser import ConfigParser
from functools import partial

SECTION = 'Desktop Entry'

class DesktopEntry(ConfigParser):
    def __init__(self, filename):
        ConfigParser.__init__(self)
        self.filename = filename
        self.read(filename)

    def __repr__(self):
        return '<DesktopEntry at 0x%x (%r)>' % (id(self), self.filename)

    @classmethod
    def get_all(cls, path='/usr/share/applications'):
        return map(DesktopEntry, iglob(os.path.join(path, '*.desktop')))

    def get_default(self, key):
        return ConfigParser.get(self, SECTION, key)

    def get_bool(self, key):
        return ConfigParser.getboolean(self, SECTION, key)

    def has_option(self, key):
        return ConfigParser.has_option(self, SECTION, key)

    def get_strings(self, key):
        return self.get_default(key).strip(';').split(';') # TODO: comma separated?

    def get_locale(self, key, locale=''):
        if not locale:
            return self.get_default(key)
        else:
            return self.get_default('%s[%s]' % key)

    type = property(partial(get_default, key='Type'))
    version = property(partial(get_default, key='Version'))
    name = property(partial(get_locale, key='Name'))
    generic_name = property(partial(get_locale, key='GenericName'))
    no_display = property(partial(get_bool, key='NoDisplay'))
    comment = property(partial(get_locale, key='Comment'))
    icon = property(partial(get_locale, key='Icon'))
    hidden = property(partial(get_bool, key='Hidden'))
    only_show_in = property(partial(get_strings, key='OnlyShowIn'))
    not_show_in = property(partial(get_strings, key='NotShowIn'))
    try_exec = property(partial(get_default, key='TryExec'))
    exec_ = property(partial(get_default, key='Exec'))
    path = property(partial(get_default, key='Path'))
    terminal = property(partial(get_bool, key='Terminal'))
    mime_type = property(partial(get_strings, key='MimeType'))
    categories = property(partial(get_strings, key='Categories'))
    startup_notify = property(partial(get_bool, key='StartupNotify'))
    startup_wmclass = property(partial(get_default, key='StartupWMClass'))
    url = property(partial(get_default, key='URL'))

if __name__ == '__main__':
    for de in DesktopEntry.get_all():
        print '*** %r ***' % de
        for attr in ['comment', 'not_show_in', 'startup_notify', 'get_bool', 'no_display', 'generic_name', 'terminal', 'version', 'hidden', 'type', 'try_exec', 'mime_type', 'get_locale', 'get', 'get_strings', 'exec_', 'startup_wmclass', 'path', 'categories', 'icon', 'name', 'url', 'only_show_in']:
            if de.has_option(attr):
                print '%s: %r' % (attr, getattr(de, attr))

