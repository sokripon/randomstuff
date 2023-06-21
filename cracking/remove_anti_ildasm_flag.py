# Tested and ran with Python 3.10
import argparse
import mmap

"""
This script removes the 'SuppressIldasmAttribute' attribute from a .NET assembly by replacing it with an alternative name.
This makes the file readable by ILDASM without the error "Protected module -- cannot disassemble".
"""

name = "SuppressIldasmAttribute"
# as hex bytes
name_bytes = name.encode("utf-8").hex()
alternative_name = "SuppressIldasmAttributd"
# as hex bytes
alternative_name_bytes = alternative_name.encode("utf-8").hex()


def replace_attribute(file_name: str):
    # open file in read+write mode
    with open(file_name, "r+b") as f:
        print(f"Searching for '{name}' in '{file_name}'")
        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(), 0)
        # find first occurrence of name_bytes
        index = mm.find(bytes.fromhex(name_bytes))
        if index == -1:
            print(f"Could not find '{name}' in '{file_name}'")
            raise Exception(f"Could not find '{name}' in '{file_name}'")
        print(f"Found '{name}' at {index}")
        # replace
        mm[index: index + len(bytes.fromhex(alternative_name_bytes))] = bytes.fromhex(alternative_name_bytes)
        print(f"Replaced '{name}' with '{alternative_name}'")
        mm.close()
        print(f"Closed '{file_name}'")


def main(file_name: str):
    replace_attribute(file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="input file name", nargs="?", default="")
    args = parser.parse_args()
    if args.file_input:
        _file_name = args.file_name
    else:
        _file_name = input("Enter file name: ")

    print(f"'{name}' will be replaced with '{alternative_name}' to bypass the ILDASM check")
    main(_file_name)
    print(f"Succesfully replaced '{name}' with '{alternative_name}' in '{_file_name}' "
          f"making the assembly readable by ILDASM")
