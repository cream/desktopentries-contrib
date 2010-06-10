import os
import re
from operator import attrgetter, itemgetter
from subprocess import Popen
from collections import defaultdict

import gtk
import gobject

KICK = re.compile('%[ifFuUck]')
ICON_SIZE = 16

def activate_entry(widget, entry):
    exec_ = KICK.sub('', entry.exec_)
    if entry.terminal:
        term = os.environ.get('TERM', 'xterm')
        exec_ = '%s -e "%s"' % (term, exec_.encode('string-escape'))
    proc = Popen(exec_, shell=True)

def lookup_icon(stuff, size=ICON_SIZE): # I'd be so happy to use gtk.ICON_SIZE_MENU here, but it returns empty pixbufs sometimes.
    if os.path.isfile(stuff):
        return gtk.gdk.pixbuf_new_from_file_at_size(stuff, ICON_SIZE, ICON_SIZE) # TODO
    try:
        theme = gtk.icon_theme_get_default()
        return theme.load_icon(stuff, size, 0).copy()
    except gobject.GError:
        print stuff
        return None

def to_gtk(entries):
    tree = defaultdict(gtk.Menu)
    for entry in sorted(entries, key=attrgetter('name')):
        category = entry.recommended_category
        if not category:
            continue
        item = None
        if entry.icon:
            icon = lookup_icon(entry.icon)
            if icon is not None:
                item = gtk.ImageMenuItem()
                item.set_image(gtk.image_new_from_pixbuf(icon))
                item.set_label(entry.name)
        if item is None:
            item = gtk.MenuItem(entry.name)
        item.connect('activate', activate_entry, entry)
        item.show()
        tree[category].append(item)
    menu = gtk.Menu()
    for category, submenu in sorted(tree.iteritems(), key=itemgetter(0)):
        item = gtk.MenuItem(category)
        item.set_submenu(submenu)
        item.show()
        menu.append(item)
    menu.show()
    return menu
