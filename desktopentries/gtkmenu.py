import gtk

import re
from operator import attrgetter, itemgetter
from subprocess import Popen
from collections import defaultdict

KICK = re.compile('%[ifFuUck]')

def activate_entry(widget, exec_):
    exec_ = KICK.sub('', exec_)
    proc = Popen(exec_, shell=True)

def to_gtk(entries):
    tree = defaultdict(gtk.Menu)
    for entry in sorted(entries, key=attrgetter('name')):
        category = entry.recommended_category
        if not category:
            continue
        item = gtk.MenuItem(entry.name)
        item.connect('activate', activate_entry, entry.exec_)
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
