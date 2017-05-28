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

class TestIntegration(unittest.TestCase):

    def test_integration_silent(self):
        raw_filenames = [
            "lip.sync.battle.s03e19.hdtv.x264-w4f.mkv",  # Lip Sync Battle
            "Archer.2009.S08E08.REPACK.HDTV.x264-SVA.mkv",  # Archer
            "The.Daily.Show.2017.03.13.Lee.Daniels.720p.CC.WEBRip.AAC2.0.x264-BTW.mkv",  # Daily Show
            "at.midnight.2017.02.14.hdtv.x264-crooks.mkv"  # @midnight
        ]
        silent = True
        correct_filenames = [
            "Lip Sync Battle - [03x19].mkv",  # Lip Sync Battle
            "Archer (2009) - [08x08].mkv",  # Archer
            "The Daily Show - [2017-03-13].mkv",  # Daily Show
            "@midnight - [2017-02-14].mkv",  # @midnight
        ]
        for i in range(len(raw_filenames)):
            raw_filename = raw_filenames[i]
            correct_filename = correct_filenames[i]
            result = tvr.tvregex(raw_filename, silent)
            self.assertEqual(correct_filename, result)


if __name__ == '__main__':
    unittest.main()
