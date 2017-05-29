import re


def fix_episode_seasonal(episode):
    return_value = episode
    pattern_string = r"(?:s|\[)(\d{1,2})(?:e|x)(\d{1,2})"
    pattern = re.compile(pattern_string, flags=re.IGNORECASE)
    match = pattern.search(episode)
    if match:
        season_num, episode_num = match.groups()
        season_num = season_num.zfill(2)
        return_value = "[{}x{}]".format(season_num, episode_num)
    else:
        raise ValueError
    return return_value


def fix_episode_daily(episode):
    return_value = episode
    pattern_string = r".*?(\d{4}).+?(\d{2}).+?(\d{2}).*?$"
    pattern = re.compile(pattern_string)
    match = pattern.search(episode)
    if match:
        year, month, day = match.groups()
        month = month.zfill(2)
        day = day.zfill(2)
        return_value = "[{}-{}-{}]".format(year, month, day)
    else:
        raise ValueError
    return return_value


def fix_episode(episode):
    return_value = episode
    pattern_string_seasonal = r"(?:s|\[)(\d{1,2})(?:e|x)(\d{1,2})"
    pattern_seasonal = re.compile(pattern_string_seasonal, flags=re.IGNORECASE)
    match_seasonal = pattern_seasonal.search(return_value)
    pattern_string_daily = r".*?(\d{4}).+?(\d{2}).+?(\d{2}).*?$"
    pattern_daily = re.compile(pattern_string_daily)
    match_daily = pattern_daily.search(return_value)
    if match_seasonal:
        return_value = fix_episode_seasonal(return_value)
    elif match_daily:
        return_value = fix_episode_daily(return_value)
    return return_value


def fix_title(showname, shownames_dict):
    return_value = showname
    return_value = re.sub(r'\W+', '', return_value)
    return_value = return_value.lower()
    return_value = shownames_dict[return_value]
    return return_value


def tvregex(filename, shownames_dict):
    return_value = filename
    pattern_string = (
        r"(.+)\." +
        "((?:s\d{2}e\d{2})|(?:\d{4}\.\d{2}\.\d{2}))" +
        ".+\.(.+)"
    )
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
