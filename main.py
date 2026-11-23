import hashlib
import os
import shutil
import sys


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_dir, "entry.txt")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

    try:
        with open(source, "r", encoding="utf-8") as handle:
            text = handle.read()
    except UnicodeDecodeError:
        print("error: entry.txt is not valid UTF-8", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: cannot read entry.txt: {exc}", file=sys.stderr)
        return 1

    line = text.strip()
    if not line:
        print("error: entry.txt is empty or whitespace-only", file=sys.stderr)
        return 1
    if not 1 <= len(line) <= 200:
        print(
            f"error: entry must be 1-200 characters, got {len(line)}",
            file=sys.stderr,
        )
        return 1

    os.makedirs(output_dir, exist_ok=True)
    if not os.access(output_dir, os.W_OK):
        print(
            f"error: output directory is not writable: {output_dir}",
            file=sys.stderr,
        )
        return 1
    destination = os.path.join(output_dir, "entry.txt")

    try:
        shutil.copyfile(source, destination)
    except shutil.SameFileError:
        print("error: source and destination are the same file", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: cannot copy entry.txt: {exc}", file=sys.stderr)
        return 1

    if sha256_file(source) != sha256_file(destination):
        print("error: copy failed sha256 verification", file=sys.stderr)
        return 1

    print(f"ok: entry.txt ({len(line)} characters) copied to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
