"""
Progress bar
"""


def progress_bar(prefix, total, complete):
    pct = (complete / total) * 100
    p = int(pct/4)
    c_markers = "#" * p
    i_markers = "-" * int(25 - p)
    print("\r%s... [%s%s] %i%%" % (prefix, c_markers, i_markers, pct), end='')
