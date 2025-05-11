def map_range(value, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another. mapping hand coordinates to game window coordinates
    Equivalent to Processing's map() function.
    """
    # Clamp the input value within the expected range
    value = max(min(value, in_max), in_min)
    in_range = in_max - in_min
    out_range = out_max - out_min
    scaled_value = float(value - in_min) / float(in_range)
    return out_min + (scaled_value * out_range)


def smooth_value(current_value, previous_value, smoothing_factor=0.4):
    """
    Smooth the transition between previous and current values.
    smoothing_factor: 0 (no change) to 1 (instant jump)
    """
    return int(previous_value + smoothing_factor * (current_value - previous_value))

def clamp(value, min_value, max_value):
    """Restrict a value to be within the specified min and max range."""
    return max(min_value, min(value, max_value))