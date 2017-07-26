import argparse


def main():
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
    print("Silent flag = {}".format(silent))
    print("File inputs:")
    for filepath in all_filepaths:
        print(filepath)


if __name__ == '__main__':
    main()
