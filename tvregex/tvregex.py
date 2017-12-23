"""A simple TV show renamer, no TVDB required

Args:
    file (str): Path to the file you want to rename
    -s / --silent (bool): Program will run without any messages
        (except unknown exceptions).

Attributes:
    SHOWNAMES_DICT_FILEPATH (str): showname match dictionary JSON filepath
"""
import re
import argparse
import os
import json


SHOWNAMES_DICT_FILENAME = "shownames.json"
SHOWNAMES_DICT_FILEPATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), SHOWNAMES_DICT_FILENAME
)
# Enums
SHOWNAME_STYLE_SXXEXX = "showname_style_SxxExx"
SHOWNAME_STYLE_XXXX = "showname_style_xxxx"
SHOWNAME_STYLE_DAILY = "showname_style_daily"
# TODO: Pattern string dictionary
pattern_strings = {
    'styles': {
        'seasonal_SE': r"(?:s|\[)(\d{1,2})(?:e|x)(\d{1,2})",
        'seasonal_4_digit': r".+?\D(\d{1,2})(\d{2})\D.+",
        'daily': r".+?\W(\d{4})\W(\d{2})\W(\d{2})\W.+"
    }
}

def fix_episode(episode):
    """Processes episode section of filename

    Args:
        episode (str): Episode section of filename

    Returns:
        str: Processed episode (daily/seasonal as appropriate)

    Raises:
        ValueError: on invalid episode string
    """
    return_value = episode
    # Scan for numbering system (SxxExx, xxxx, or daily)
    # If seasonal, scan as follows:
        # Prefix (optional, bracketed, no capture)
        # Name (may use dots)
        # Season and episode number (SxxExx or xxxx)
        # Suffix (do not capture)
        # File extension
    # If daily, scan as before but...
        # Date of show (yyyy.mm.dd, may replace . by other punctuation)
    pattern_string_seasonal_SE_style = r"(?:s|\[)(\d{1,2})(?:e|x)(\d{1,2})"
    pattern_seasonal_SE_style = re.compile(pattern_string_seasonal_SE_style,
        flags=re.IGNORECASE)
    match_seasonal_SE_style = pattern_seasonal_SE_style.search(return_value)
    # pattern_string_seasonal_4_digit_style = r""
    # pattern_seasonal_4_digit_style = re.compile(
    #     pattern_string_seasonal_4_digit_style, flags=re.IGNORECASE)
    # match_seasonal_4_digit_style = pattern_seasonal_4_digit_style.search(
    #     return_value)
    pattern_string_daily = r".*?(\d{4}).+?(\d{2}).+?(\d{2}).*?$"
    pattern_daily = re.compile(pattern_string_daily)
    match_daily = pattern_daily.search(return_value)
    if match_seasonal_SE_style: # || match_seasonal_4_digit_style:
        season_num, episode_num = match_seasonal_SE_style.groups()
        season_num = season_num.zfill(2)
        return_value = "[{}x{}]".format(season_num, episode_num)
    # elif match_seasonal_4_digit_style:
        # season_num, episode_num = match_seasonal_SE_style.groups()
        # season_num = season_num.zfill(2)
        # return_value = "[{}x{}]".format(season_num, episode_num)
    elif match_daily:
        year, month, day = match_daily.groups()
        month = month.zfill(2)
        day = day.zfill(2)
        return_value = "[{}-{}-{}]".format(year, month, day)
    else:
        raise ValueError
    return return_value


def fix_title(showname, shownames_dict):
    """Processes showname section of filename

    Args:
        showname (str): Showname section of filename
        shownames_dict (dict): Matches raw showname to real showname

    Returns:
        str: Processed showname
    """
    return_value = showname
    return_value = re.sub(r'\W+', '', return_value)
    return_value = return_value.lower()
    return_value = shownames_dict[return_value]
    return return_value


def find_raw_showname_style(filename):
    """something

    Args:
        filename (str): filename of show file

    Returns:
        str: style of showname (see enums above)
    """
    return_value = filename
    # create pattern strings
    pattern_string_style_seasonal_SE = r"(?:s|\[)(\d{1,2})(?:e|x)(\d{1,2})"
    pattern_string_style_seasonal_4_digit = r".+?\D(\d{1,2})(\d{2})\D.+"
    # pattern_string_style_daily = r".*?(\d{4}).+?(\d{2}).+?(\d{2}).*?$"
    pattern_string_style_daily = r".+?\W(\d{4})\W(\d{2})\W(\d{2})\W.+"
    # compile patterns
    pattern_style_seasonal_SE = re.compile(pattern_strings['styles']['seasonal_SE'],
        flags=re.IGNORECASE)
    pattern_style_seasonal_4_digit = re.compile(
        pattern_strings['styles']['seasonal_4_digit'], flags=re.IGNORECASE)
    pattern_style_daily = re.compile(pattern_strings['styles']['daily'])
    # find match
    match_style_seasonal_SE = pattern_style_seasonal_SE.search(return_value)
    match_style_seasonal_4_digit = pattern_style_seasonal_4_digit.search(
        return_value)
    match_style_daily = pattern_style_daily.search(return_value)
    # check matches and return style enum
    if match_style_seasonal_SE :
        return_value = SHOWNAME_STYLE_SXXEXX
    elif match_style_daily :
        return_value = SHOWNAME_STYLE_DAILY
    elif match_style_seasonal_4_digit :
        return_value = SHOWNAME_STYLE_XXXX
    else :
        raise ValueError
    return return_value


def tvregex(filename, shownames_dict):
    """Main program flow

    Args:
        filename (str): Path to the file you want to rename
        shownames_dict (dict): Matches raw showname to real showname

    Returns:
        str: Renamed filename
    """
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
    # raw_showname_style = find_raw_showname_style(filename)
    # if raw_showname_style ==  SHOWNAME_STYLE_SXXEXX :
    #     pass
    #     # something
    # elif raw_showname_style == SHOWNAME_STYLE_XXXX :
    #     pass
    #     # something
    # elif raw_showname_style == SHOWNAME_STYLE_DAILY :
    #     pass
    #     # something
    # else :
    #     raise ValueError
    return return_value



def attempt_rename(folder, old_filename, shownames_dict, silent):
    try:
        new_filename = tvregex(old_filename, shownames_dict)
        new_filepath = os.path.join(folder, new_filename)
        old_filepath = os.path.join(folder, old_filename)
        os.rename(old_filepath, new_filepath)
    except KeyError as ke:
        if not silent:
            raw_showname = ke.args[0]
            print(
                "The filename was processed to give {}".format(
                    raw_showname
                )
            )
            print("No show name match is known.")
            print("Type the show name that matches this")
            good_showname = input(
                "(or just press Enter if there's no match):"
            )
            if good_showname != "":

                shownames_dict[raw_showname] = good_showname
                with open(SHOWNAMES_DICT_FILEPATH, "w") as f:
                    json.dump(shownames_dict, f, indent=4)
                print("Thanks! Please run me again with this file!")
                # Can I just run main() again?
    except ValueError as ve:
        if not silent:
            print("Cannot read episode number or date for this file")
    except AttributeError as ae:
        if not silent:
            print("Cannot read file name as TV show")


def main():
    """Takes in args
    Passes to real main program flow in tvregex()
    Outputs to file system
    """
    shownames_dict = {}
    with open(SHOWNAMES_DICT_FILEPATH) as f:
        shownames_dict = json.load(f)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        help="Path to the file you want to rename",
        nargs="+"
    )
    parser.add_argument(
        "-s", "--silent",
        help="Program will run without any messages" +
        " (except unknown exceptions). " +
        "(If set, this won't ask for matches)",
        action="store_true"
    )
    program_args = parser.parse_args()
    silent = program_args.silent
    all_filepaths = program_args.file
    for filepath in all_filepaths:
        if os.path.isfile(filepath):
            folder = os.path.dirname(filepath)
            old_filename = os.path.basename(filepath)
            attempt_rename(
                folder, old_filename, shownames_dict, silent
            )
        elif os.path.isdir(filepath):
            # Get names of all files in folder, store to list
            files_list = [
                f for f in os.listdir(filepath) if os.path.isfile(
                    os.path.join(filepath, f)
                )
            ]
            # Iterate over list, run rename attempt on each
            for file in files_list:
                attempt_rename(filepath, file, shownames_dict, silent)
        else:
            if not silent:
                print("Nothing at file path")


if __name__ == '__main__':
    main()
