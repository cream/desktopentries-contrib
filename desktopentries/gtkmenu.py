import gtk

import os
import re
from operator import attrgetter, itemgetter
from subprocess import Popen
from collections import defaultdict

KICK = re.compile('%[ifFuUck]')

def activate_entry(widget, entry):
    exec_ = KICK.sub('', entry.exec_)
    if entry.terminal:
        term = os.environ.get('TERM', 'xterm')
        exec_ = '%s -e "%s"' % (term, exec_.encode('string-escape'))
    proc = Popen(exec_, shell=True)

def to_gtk(entries):
    tree = defaultdict(gtk.Menu)
    for entry in sorted(entries, key=attrgetter('name')):
        category = entry.recommended_category
        if not category:
            continue
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
