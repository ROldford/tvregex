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
        pass


class TestIntegration(unittest.TestCase):

    def test_integration_silent(self):
        # TODO: Change test method name, remove "silent"
        raw_filenames = [
            "lip.sync.battle.s03e19.hdtv.x264-w4f.mkv",  # Lip Sync Battle
            "Archer.2009.S08E08.REPACK.HDTV.x264-SVA.mkv",  # Archer
            "The.Daily.Show.2017.03.13.Lee.Daniels." +
            "720p.CC.WEBRip.AAC2.0.x264-BTW.mkv",  # Daily Show
            "at.midnight.2017.02.14.hdtv.x264-crooks.mkv"  # @midnight
        ]
        shownames = {
            "lipsyncbattle": "Lip Sync Battle",
            "archer2009": "Archer (2009)",
            "thedailyshow": "The Daily Show",
            "atmidnight": "@midnight"
        }
        correct_filenames = [
            "Lip Sync Battle - [03x19].mkv",  # Lip Sync Battle
            "Archer (2009) - [08x08].mkv",  # Archer
            "The Daily Show - [2017-03-13].mkv",  # Daily Show
            "@midnight - [2017-02-14].mkv",  # @midnight
        ]
        for i in range(len(raw_filenames)):
            raw_filename = raw_filenames[i]
            correct_filename = correct_filenames[i]
            result = tvr.tvregex(raw_filename, shownames)
            self.assertEqual(correct_filename, result)


if __name__ == '__main__':
    unittest.main()
