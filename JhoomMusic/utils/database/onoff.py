# Maintenance / on-off mode

maintenance_mode = False

def is_maintenance() -> bool:
    return maintenance_mode

def set_maintenance(value: bool):
    global maintenance_mode
    maintenance_mode = value
