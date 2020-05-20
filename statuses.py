
class Status:
    code = None
    display = None
    color = None
    show = None
    blink = None

    def __init__(self, code, display, color, show=True, blink=False):
        self.code = code
        self.display = display
        self.color = color
        self.show = show
        self.blink = blink

statuses = [
    Status("BUSY", "Busy", "#930000"),
    Status("WORKING", "Working", "#c07c00"),
    Status("AVAILABLE", "Available", "#007600"),
    Status("ATTENTION", "Attention", "#003a76", blink=True)
]

# You can override these statuses by defining a
# custom_statuses array in config.py.
def set_custom_statuses(custom_statuses):
    global statuses
    if custom_statuses:
        print('Overriding statuses')
        statuses = custom_statuses
    else:
        print('No custom statuses')

def get_statuses():
    global statuses
    return statuses

def get_visible_count():
    global statuses
    return len(list(filter(lambda s: s.show, statuses)))