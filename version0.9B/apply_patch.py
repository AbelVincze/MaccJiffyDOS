import struct
import hashlib
import argparse
import sys


input_md5 = "be09394f0576cf81fa8bacf634daf9a2"
patch_md5 = "1c76120a56d45648adbe819473d571be"
output_md5 = "a0b33a60e38b6795682319a520b039d9"

def read_file(path):
    with open(path, "rb") as f:
        return bytearray(f.read())


def md5_hash(data):
    return hashlib.md5(data).hexdigest()


def apply_patch(original, diff_path):
    with open(diff_path, "rb") as f:
        while True:
            addr_bytes = f.read(2)
            if not addr_bytes:
                break

            start = struct.unpack(">H", addr_bytes)[0]
            length = struct.unpack("B", f.read(1))[0]
            data = f.read(length)

            original[start:start + length] = data

    return original

def bye():
    print("Patch not applied.")
    exit()

def checkBinary(data, check, name):
    data_md5 = md5_hash(data)
    if data_md5 != check:
        print(f"{name} MD5 missmatch: {data_md5} should be {check}")
        bye()

    print(f"{name} MD5 checksum: {data_md5} - pass")   

def main():
    parser = argparse.ArgumentParser(
        description="Apply MaccPatch to JiffyDOS6.01",
        usage="python apply_patch.py <jiffydos6.01.rom> <maccpatch_v0.9b.bin> <maccjiffy.rom>"
    )

    parser.add_argument("original", nargs='?')
    parser.add_argument("diff", nargs='?')
    parser.add_argument("output", nargs='?')

    args = parser.parse_args()

    if not args.original or not args.diff or not args.output:
        parser.print_help()
        sys.exit(1)

    original = read_file(args.original)
    checkBinary(original, input_md5, "JiffyDOS")

    patchdata = read_file(args.diff)
    checkBinary(patchdata, patch_md5, "PatchData")

    patched = apply_patch(original, args.diff)
    checkBinary(patched, output_md5, "MaccJiffy")

    with open(args.output, "wb") as f:
        f.write(patched)

    print("Patch applied successfully.")


if __name__ == "__main__":
    main()