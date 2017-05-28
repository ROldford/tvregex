import re


def tvregex(filename, shownames):
    return_value = filename
    pattern_string = r"(.+)\.(s\d{2}e\d{2}).+\.(.+)"
    pattern = re.compile(pattern_string, flags=re.IGNORECASE)
    match = pattern.search(filename)
    showname, episode, extension = match.groups()
    return_value = showname
    return return_value


def main():
    # Set up arguments
    # Parse arguments
    # Call tvregex
    pass


if __name__ == '__main__':
    main()
