from django import template
import re

register = template.Library()

def substr(value):
    m = re.search("\d", value)
    ind = value.find('/', m.start())
    if ind != -1:
        return value[m.start(): ind]
    else:
        return value[m.start(): ]

register.filter('substr', substr)
