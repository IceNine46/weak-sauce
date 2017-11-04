"""
Progress bar
"""


def progress_bar(prefix, total, complete, elapsed):
    try:
        pct = (complete / total) * 100
    except ZeroDivisionError:
        print("Invalid total of zero passed.")
        return

    p = int(pct/4)
    c_markers = "#" * p
    i_markers = "-" * int(25 - p)
    print("\r%s [%s%s] %i%% - %is" % (prefix, c_markers, i_markers, pct, elapsed), end='')
