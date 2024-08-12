from django import template

register = template.Library()

BOOKING_STATUS_CHOICES = {
    "0": "In Process",
    "1": "Confirmed",
    "2": "Canceled",
}

VERIFICATION_STATUS_CHOICES = {
    "0": "In Process",
    "1": "Verified",
    "2": "Canceled",
}

ID_TYPE_CHOICES = {
    "1": "Institutional ID",
    "2": "Aadhar Number",
    "3": "Voter ID",
    "4": "Driving License",
    "5": "Passport",
}


@register.filter
def parse_booking_status(status):
    return BOOKING_STATUS_CHOICES.get(status, status)


@register.filter
def parse_verification_status(status):
    return VERIFICATION_STATUS_CHOICES.get(status, status)


@register.filter
def parse_id_type(id_type):
    return ID_TYPE_CHOICES.get(id_type, id_type)