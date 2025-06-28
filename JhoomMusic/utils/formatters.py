def seconds_to_min(seconds):
    """Convert seconds to MM:SS format"""
    if seconds is None:
        return "Unknown"
    
    if seconds == 0:
        return "Live Stream"
    
    try:
        seconds = int(seconds)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    except:
        return "Unknown"

def get_readable_time(seconds: int) -> str:
    """Convert seconds to human readable format"""
    if seconds is None:
        return "Unknown"
    
    try:
        seconds = int(seconds)
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
    except:
        return "Unknown"

def convert_bytes(size):
    """Convert bytes to human readable format"""
    if size is None:
        return "Unknown"
    
    try:
        size = int(size)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    except:
        return "Unknown"

def format_duration(duration_str):
    """Format duration string to seconds"""
    if not duration_str or duration_str == "Unknown":
        return 0
    
    try:
        # Handle different duration formats
        if ":" in duration_str:
            parts = duration_str.split(":")
            if len(parts) == 2:  # MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        else:
            return int(duration_str)
    except:
        return 0

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if not text:
        return "Unknown"
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def format_file_size(size_bytes):
    """Format file size in bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"