"""Normalize an existing SDK archive without changing its file contents."""

import argparse
import hashlib
import json
import tarfile
from pathlib import Path, PurePosixPath


def repack(source: Path, destination: Path) -> None:
    if not destination.name.endswith(".tar.bz2"):
        raise ValueError("SDK archives must use .tar.bz2")
    root = destination.name.removesuffix(".tar.bz2")
    destination.parent.mkdir(parents=True, exist_ok=True)
    original_root = None
    files = {}
    with tarfile.open(source, "r|*") as incoming, tarfile.open(destination, "w|bz2") as outgoing:
        for member in incoming:
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"Unsafe archive path: {member.name}")
            if not path.parts:
                continue
            # Finder metadata is not part of the SDK and can add a second archive root.
            if any(part.startswith("._") or part == "__MACOSX" for part in path.parts):
                continue
            if original_root is None:
                original_root = path.parts[0]
            if path.parts[0] != original_root:
                raise ValueError("SDK archive must contain one top-level directory")
            relative = PurePosixPath(*path.parts[1:])
            member.name = str(PurePosixPath(root) / relative)
            if member.linkname.startswith(original_root + "/"):
                member.linkname = root + member.linkname[len(original_root):]
            if member.isfile():
                stream = incoming.extractfile(member)
                digest = hashlib.sha256()

                class Reader:
                    def read(self, size=-1):
                        chunk = stream.read(size)
                        digest.update(chunk)
                        return chunk

                outgoing.addfile(member, Reader())
                files[str(relative)] = digest.hexdigest()
            else:
                outgoing.addfile(member)

    # Verify every file after recompression, not only the archive's metadata.
    actual = {}
    with tarfile.open(destination, "r|bz2") as archive:
        for member in archive:
            if member.isfile():
                digest = hashlib.sha256()
                stream = archive.extractfile(member)
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
                actual[str(PurePosixPath(member.name).relative_to(root))] = digest.hexdigest()
    if actual != files:
        raise ValueError("SDK contents changed during repackaging")
    hashes = {name: hashlib.new(name) for name in ("sha1", "sha256")}
    with destination.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            for digest in hashes.values():
                digest.update(chunk)
    result = {"name": destination.name, "bytes": destination.stat().st_size,
              "files_verified": len(files), **{name: digest.hexdigest() for name, digest in hashes.items()}}
    destination.with_suffix(destination.suffix + ".json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    repack(args.source, args.destination)
