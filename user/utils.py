import uuid


def generate_resident_id(name, resident_ids):
    name = name.replace(" ", "").lower()
    r_id = name
    while r_id in resident_ids:
        r_id = name + f"{uuid.uuid4()}"[:8]
        

    return r_id