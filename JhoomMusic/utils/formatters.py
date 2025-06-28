def seconds_to_min(seconds):
    if seconds is None:
        return "Unknown"
    
    if seconds == 0:
        return "Live Stream"
    
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    
    time_list.reverse()
    ping_time += ":".join(time_list)
    
    return ping_time


def convert_bytes(size):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"