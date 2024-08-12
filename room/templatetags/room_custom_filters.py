from django import template

register = template.Library()

FLOORS = {
    "1": "First",
    "2": "Second",
    "3": "Third",
    "4": "Fourth",
}

TYPE = {
    "1": "Single",
    "2": "Double",
    "3": "Triple",
}


@register.filter
def parse_floor(floor):
    return FLOORS.get(floor, floor)


@register.filter
def parse_type(type):
    return TYPE.get(type, type)