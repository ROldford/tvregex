import re


def fix_episode_seasonal(episode):
    return_value = episode
    pattern_string = r".??(\d{1,2}).??(\d{1,2})"
    pattern = re.compile(pattern_string, flags=re.IGNORECASE)
    match = pattern.search(episode)
    if match:
        season_num, episode_num = match.groups()
        season_num = season_num.zfill(2)
        return_value = "[{}x{}]".format(season_num, episode_num)
    else:
        raise ValueError
    return return_value


def fix_episode(episode):
    return fix_episode_seasonal(episode)


def fix_title(showname, shownames_dict):
    return_value = showname
    return_value = re.sub(r'\W+', '', return_value)
    return_value = return_value.lower()
    return_value = shownames_dict[return_value]
    return return_value


def tvregex(filename, shownames_dict):
    return_value = filename
    pattern_string = r"(.+)\.(s\d{2}e\d{2}).+\.(.+)"
    pattern = re.compile(pattern_string, flags=re.IGNORECASE)
    match = pattern.search(filename)
    showname, episode, extension = match.groups()
    showname = fix_title(showname, shownames_dict)
    episode = fix_episode(episode)
    return_value = "{} - {}.{}".format(showname, episode, extension)
    return return_value


def main():
    # Set up arguments
    # Parse arguments
    # Call tvregex
    pass


if __name__ == '__main__':
    main()
