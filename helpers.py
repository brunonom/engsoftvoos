def minutesDiff(date1, date2):
    delay = date1 - date2
    seconds = delay.total_seconds()

    if seconds < 0:
        return 0

    return seconds / 60
