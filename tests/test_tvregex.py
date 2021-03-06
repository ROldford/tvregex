"""Test suite for TVRegex
"""
import unittest
from tvregex import tvregex



# Program will take command line arguments:
# -> File (required)
# -> -s / --silent = Fail silently if matching fails
# ----> Normal behaviour is to ask for show name
# Program uses regex to parse file name
# Program finds match for show name
# -> Needs some kind of writeable config file (JSON?)
# Program renames file with show name and episode number
# -> Can do date based if needed (i.e. Daily Show)


class TestFixEpisode(unittest.TestCase):
    """Tests for fix_episode
    """
    def test_correctly_fixes_mixed_episodes(self):
        """Function should be able to rename both formats
        """
        raw_data = [
            [("03","19"), tvregex.SHOWNAME_STYLE_SXXEXX], 
            [("08","08"), tvregex.SHOWNAME_STYLE_SXXEXX], 
            [("03","19"), tvregex.SHOWNAME_STYLE_XXXX], 
            [("08","08"), tvregex.SHOWNAME_STYLE_XXXX], 
            [("2017", "03", "13"), tvregex.SHOWNAME_STYLE_DAILY], 
            [("2017", "02", "14"), tvregex.SHOWNAME_STYLE_DAILY]
        ]
        correct_episodes = [
            "[03x19]", "[08x08]", 
            "[03x19]", "[08x08]", 
            "[2017-03-13]", "[2017-02-14]"
        ]
        for i in range(len(raw_data)):
            this_data = raw_data[i]
            episode = this_data[0]
            style_enum = this_data[1]
            correct_episode = correct_episodes[i]
            result = tvregex.fix_episode(episode, style_enum)
            self.assertEqual(correct_episode, result)

    def test_raises_exception_on_bad_episode(self):
        bad_episodes = [
            [("??","??"), tvregex.SHOWNAME_STYLE_SXXEXX], 
            [("??","??"), tvregex.SHOWNAME_STYLE_XXXX], 
            [("????", "??", "??"), tvregex.SHOWNAME_STYLE_DAILY], 
            [("03","19"), "not a valid enum"], 
        ]
        for bad_episode in bad_episodes:
            self.assertRaises(
                ValueError, 
                tvregex.fix_episode, 
                bad_episode[0], 
                bad_episode[1]
            )


class TestFixTitle(unittest.TestCase):
    """Tests for fix_title
    """
    def test_correctly_fixes_title(self):
        raw_shownames = [
            "lip.sync.battle", # Dots, lowercase
            "[pseudo] rick and morty", # Spaces, lowercase
            "Rick.and.Morty", # Dots, uppercase
            "[snahp.it]rick.and.morty.", # Prefix, dots, lowercase
            ".lip.sync.battle.", # Dots, lowercase, extra padding characters
            " lip sync battle " # Dots, lowercase, extra padding characters
        ]
        shownames_dict = {
            "lipsyncbattle": "Lip Sync Battle",
            "rickandmorty": "Rick and Morty"
        }
        correct_shownames = [
            "Lip Sync Battle",
            "Rick and Morty",
            "Rick and Morty",
            "Rick and Morty",
            "Lip Sync Battle",
            "Lip Sync Battle"
        ]
        for i in range(len(raw_shownames)):
            raw_showname = raw_shownames[i]
            correct_showname = correct_shownames[i]
            result = tvregex.fix_title(raw_showname, shownames_dict)
            self.assertEqual(correct_showname, result)

    def test_raises_exception_on_unknown_title(self):
        bad_showname = "Better.Call.Saul"
        shownames_dict = {
            "lipsyncbattle": "Lip Sync Battle",
            "archer2009": "Archer (2009)"
        }
        self.assertRaises(
            KeyError,
            tvregex.fix_title,
            bad_showname,
            shownames_dict
        )


class TestFixExtension(unittest.TestCase):
    """Tests for fix_extension
    """
    def test_correctly_gets_extension(self):
        raw_name_ends = [
            "- Pilot [1080p] [h.265].mkv",
            ".720p.hdtv.x265-Snahp.mkv", 
            " - Pilot [1080p] [h.265].avi", 
            ".720p.hdtv.x265-Snahp.avi", 
            " - Pilot [1080p] [h.265].mov", 
            ".720p.hdtv.x265-Snahp.mov", 
            " - Pilot [1080p] [h.265].mp4", 
            ".720p.hdtv.x265-Snahp.mp4"
        ]
        correct_extensions = [
            "mkv", 
            "mkv", 
            "avi", 
            "avi", 
            "mov", 
            "mov", 
            "mp4", 
            "mp4"
        ]
        for i in range(len(raw_name_ends)):
            raw_name_end = raw_name_ends[i]
            correct_extension = correct_extensions[i]
            result = tvregex.fix_extension(raw_name_end)
            self.assertEqual(correct_extension, result)

    def test_raisess_exception_on_bad_extension(self):
        bad_ends = [
            " - Pilot [1080p] [h.265].???", 
            " - Pilot [1080p] [h.265].", 
            " - Pilot [1080p] [h.265]"
        ]
        for i in range(len(bad_ends)):
            self.assertRaises(
                ValueError,
                tvregex.fix_extension,
                bad_ends[i]
            )

class TestFindRawShownameStyle(unittest.TestCase):
    """Tests for find_raw_showname_style
    """
    def test_correctly_gets_style(self):
        raw_shownames = [
            "lip.sync.battle.s03e19.hdtv.x264-w4f.mkv", # SxxExx
            "Archer.2009.S08E08.REPACK.HDTV.x264-SVA.mkv", # SxxExx year in title
            "[pseudo] Rick and Morty S02E10" + 
            " The Wedding Squanchers [1080p] [h.265].mkv", # SxxExx no dots prefix
            "[snahp.it]rick.and.morty.s03e01.720p.hdtv.x265-Snahp.mkv", # SxxExx dots prefix
            "lip.sync.battle.0319.hdtv.x264-w4f.mkv", # xxxx
            "[pseudo] Rick and Morty 0210" + 
            " The Wedding Squanchers [1080p] [h.265].mkv", # xxxx no dots prefix
            "[snahp.it]rick.and.morty." + 
            "0301.720p.hdtv.x265-Snahp.mkv", # xxxx dots prefix
            "the.daily.show.2017.12.13." + 
            "satya.nadella.extended.web.x264-tbs.mkv", # daily
            "the.daily.show.2017-12-13" + 
            ".satya.nadella.extended.web.x264-tbs.mkv" # daily alt punctuation
        ]
        correct_styles = [
            tvregex.SHOWNAME_STYLE_SXXEXX, 
            tvregex.SHOWNAME_STYLE_SXXEXX, 
            tvregex.SHOWNAME_STYLE_SXXEXX, 
            tvregex.SHOWNAME_STYLE_SXXEXX, 
            tvregex.SHOWNAME_STYLE_XXXX, 
            tvregex.SHOWNAME_STYLE_XXXX, 
            tvregex.SHOWNAME_STYLE_XXXX, 
            tvregex.SHOWNAME_STYLE_DAILY,
            tvregex.SHOWNAME_STYLE_DAILY 
        ]
        for i in range(len(raw_shownames)):
            raw_showname = raw_shownames[i]
            correct_style = correct_styles[i]
            result = tvregex.find_raw_showname_style(raw_showname)
            self.assertEqual(correct_style, result)

    def test_raises_exception_on_unfindable_style(self):
        pass
        # setup bad showname
        bad_showname = "lip.sync.battle.abcde.12345.hdtv.mkv"
        # assertRaises
        self.assertRaises(
            ValueError,
            tvregex.find_raw_showname_style,
            bad_showname
        )


class TestIntegration(unittest.TestCase):
    """Integration tests for tvregex()
    """
    def setUp(self):
        self.shownames_dict = {
            "lipsyncbattle": "Lip Sync Battle",
            "archer2009": "Archer (2009)",
            "thedailyshow": "The Daily Show",
            "atmidnight": "@midnight"
        }

    def test_integration_seasonal(self):
        """Seasonal = episodes are part of seasons
        S01E01, s01e01, etc.
        """
        raw_filenames = [
            "lip.sync.battle.s03e19.hdtv.x264-w4f.mkv",  # Lip Sync Battle
            "Archer.2009.S08E08.REPACK.HDTV.x264-SVA.mkv"  # Archer
        ]
        correct_filenames = [
            "Lip Sync Battle - [03x19].mkv",  # Lip Sync Battle
            "Archer (2009) - [08x08].mkv"  # Archer
        ]
        for i in range(len(raw_filenames)):
            raw_filename = raw_filenames[i]
            correct_filename = correct_filenames[i]
            result = tvregex.tvregex(raw_filename, self.shownames_dict)
            self.assertEqual(correct_filename, result)

    def test_integration_daily(self):
        """Daily = episodes are numbered by date
        2017-01-01, etc.
        """
        raw_filenames = [
            "The.Daily.Show.2017.03.13.Lee.Daniels." +
            "720p.CC.WEBRip.AAC2.0.x264-BTW.mkv",  # Daily Show
            "at.midnight.2017.02.14.hdtv.x264-crooks.mkv"  # @midnight
        ]
        correct_filenames = [
            "The Daily Show - [2017-03-13].mkv",  # Daily Show
            "@midnight - [2017-02-14].mkv",  # @midnight
        ]
        for i in range(len(raw_filenames)):
            raw_filename = raw_filenames[i]
            correct_filename = correct_filenames[i]
            result = tvregex.tvregex(raw_filename, self.shownames_dict)
            self.assertEqual(correct_filename, result)


if __name__ == '__main__':
    unittest.main()
