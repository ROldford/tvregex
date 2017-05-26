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
        # TODO: Enter raw filenames
        raw_filenames = [
            "",  # Daily Show
            "",  # @midnight
            "",  # Better Call Saul
            "",  # Something else
        ]
        silent = True
        # TODO: Enter matching correct filenames
        correct_filenames = [
            "",  # Daily Show
            "",  # @midnight
            "",  # Better Call Saul
            "",  # Something else
        ]
        for i in range(len(raw_filenames)):
            raw_filename = raw_filenames[i]
            correct_filename = correct_filenames[i]
            result = tvr.tvregex(raw_filename, silent)
            self.assertEqual(correct_filename, result)


if __name__ == '__main__':
    unittest.main()
