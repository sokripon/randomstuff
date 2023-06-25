# Tested and ran with Python 3.10
import argparse
import mmap

"""
This script removes the 'SuppressIldasmAttribute' attribute from a .NET assembly by replacing it with an alternative name.
This makes the file readable by ILDASM without the error "Protected module -- cannot disassemble".
"""


def replace_attribute(file_name: str, to_replace_hex: str, replacement_hex: str):
    # open file in read+write mode
    with open(file_name, "r+b") as f:
        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(), 0)
        # find first occurrence of to_replace_hex
        print(f"Searching for '{to_replace_hex}' in '{file_name}'")
        index = mm.find(bytes.fromhex(to_replace_hex))
        if index == -1:
            raise Exception(f"Could not find '{to_replace_hex}' in '{file_name}'")
        # replace
        mm[index : index + len(bytes.fromhex(replacement_hex))] = bytes.fromhex(
            replacement_hex
        )
        mm.close()


def main(file_name: str, string_hex: str, altered_string_hex: str):
    replace_attribute(file_name, string_hex, altered_string_hex)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="input file name", nargs="?", default="")
    parser.add_argument(
        "--string", help="string to replace", default="SuppressIldasmAttribute"
    )
    parser.add_argument(
        "--altered_string",
        help="string to replace with",
        default="SuppressIldasmAttributd",
    )
    parser.add_argument(
        "--should_not_hex",
        help="whether to not call the hex() method on the string arguments",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()
    if args.file_name:
        _file_name = args.file_name
    else:
        _file_name = input("Enter file name: ")
    string = args.string
    altered_string = args.altered_string
    print(args.should_not_hex)
    if args.should_not_hex:
        s_ = string
        s_a_ = altered_string
    else:
        s_ = string.encode("utf-8").hex()
        s_a_ = altered_string.encode("utf-8").hex()

    print(
        f"'{string}' will be replaced with '{altered_string}' to bypass the ILDASM check"
    )
    main(_file_name, s_, s_a_)
    print(f"Succesfully replaced '{string}' with '{altered_string}' in '{_file_name}' ")
