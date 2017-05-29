import unittest
import tvregex as tvr


# Program will take command line arguments:
# -> File (required)
# -> -s / --silent = Fail silently if matching fails
# ----> Normal behaviour is to ask for show name
# Program uses regex to parse file name
# Program finds match for show name
# -> Needs some kind of writeable config file (JSON?)
# Program renames file with show name and episode number
# -> Can do date based if needed (i.e. Daily Show)

class TestFixEpisodeSeasonal(unittest.TestCase):

    def test_correctly_fixes_episode_seasonal(self):
        raw_episodes = ["s03e19", "S08E08"]
        correct_episodes = ["[03x19]", "[08x08]"]
        for i in range(len(raw_episodes)):
            raw_episode = raw_episodes[i]
            correct_episode = correct_episodes[i]
            result = tvr.fix_episode_seasonal(raw_episode)
            self.assertEqual(correct_episode, result)

    def test_returns_exception_on_bad_episode(self):
        bad_episode = "S??E??"
        self.assertRaises(ValueError, tvr.fix_episode_seasonal, bad_episode)


class TestFixEpisodeDaily(unittest.TestCase):

    def test_correctly_fixes_episode_daily(self):
        raw_episodes = ["2017.03.13", "2017.02.14"]
        correct_episodes = ["[2017-03-13]", "[2017-02-14]"]
        for i in range(len(raw_episodes)):
            raw_episode = raw_episodes[i]
            correct_episode = correct_episodes[i]
            result = tvr.fix_episode_daily(raw_episode)
            self.assertEqual(correct_episode, result)

    def test_returns_exception_on_bad_episode(self):
        pass


class TestFixEpisode(unittest.TestCase):

    def test_correctly_fixes_mixed_episodes(self):
        raw_episodes = ["s03e19", "S08E08", "2017.03.13", "2017.02.14"]
        correct_episodes = [
            "[03x19]", "[08x08]",
            "[2017-03-13]", "[2017-02-14]"
        ]
        for i in range(len(raw_episodes)):
            raw_episode = raw_episodes[i]
            correct_episode = correct_episodes[i]
            result = tvr.fix_episode(raw_episode)
            self.assertEqual(correct_episode, result)


class TestFixTitle(unittest.TestCase):

    def test_correctly_fixes_title(self):
        raw_shownames = [
            "lip.sync.battle",  # Lip Sync Battle
            "Archer.2009"  # Archer
        ]
        shownames_dict = {
            "lipsyncbattle": "Lip Sync Battle",
            "archer2009": "Archer (2009)"
        }
        correct_shownames = [
            "Lip Sync Battle",  # Lip Sync Battle
            "Archer (2009)"  # Archer
        ]
        for i in range(len(raw_shownames)):
            raw_showname = raw_shownames[i]
            correct_showname = correct_shownames[i]
            result = tvr.fix_title(raw_showname, shownames_dict)
            self.assertEqual(correct_showname, result)

    def test_returns_exception_on_unknown_title(self):
        bad_showname = "Better.Call.Saul"
        shownames_dict = {
            "lipsyncbattle": "Lip Sync Battle",
            "archer2009": "Archer (2009)"
        }
        self.assertRaises(
            KeyError,
            tvr.fix_title,
            bad_showname,
            shownames_dict
        )


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.shownames_dict = {
            "lipsyncbattle": "Lip Sync Battle",
            "archer2009": "Archer (2009)",
            "thedailyshow": "The Daily Show",
            "atmidnight": "@midnight"
        }

    def test_integration_seasonal(self):
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
            result = tvr.tvregex(raw_filename, self.shownames_dict)
            self.assertEqual(correct_filename, result)

    def test_integration_daily(self):
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
            result = tvr.tvregex(raw_filename, self.shownames_dict)
            self.assertEqual(correct_filename, result)


if __name__ == '__main__':
    unittest.main()
