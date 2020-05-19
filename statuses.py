
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

def get_statuses():
    return statuses

def get_visible_count():
    return len(list(filter(lambda s: s.show, statuses)))