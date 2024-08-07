def parse_segments(segment_list):
    """
    Parse a list of segment strings into a list of tuples.
    """
    parsed_segments = []
    for segment in segment_list:
        start, end = map(int, segment.split(','))
        parsed_segments.append((start, end))
    return parsed_segments

def intersect_segments(segment_lists):
    """
    Find the intersection of multiple lists of segments.
    """
    # Convert all segment strings to tuples of integers
    parsed_segment_lists = [parse_segments(segment_list) for segment_list in segment_lists]

    # Find the intersection
    # Start with the intersection as the full range
    intersection = None

    for segments in parsed_segment_lists:
        for start, end in segments:
            if intersection is None:
                intersection = (start, end)
            else:
                # Update the intersection to be the overlap of the current segment and the current intersection
                intersection = (max(intersection[0], start), min(intersection[1], end))

            # If the intersection becomes invalid, there's no common overlap
            if intersection[0] > intersection[1]:
                return None

    return intersection
