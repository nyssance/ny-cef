"""Generate the CEF downloader index from the published platform manifests."""

import json
import sys
from pathlib import Path

index = {key: {"versions": []} for key in (
    "macosarm64", "macosx64", "windows64", "windowsarm64", "windows32",
    "linux64", "linuxarm64", "linuxarm",
)}
platforms = {"macos-arm64": "macosarm64", "windows-x64": "windows64"}
for name in sys.argv[1:]:
    manifest = json.loads(Path(name).read_text())
    key = platforms[manifest["platform"]]
    if index[key]["versions"]:
        raise ValueError(f"Duplicate platform: {key}")
    archive = manifest["archive"]
    index[key]["versions"].append({
        "channel": "stable",
        "cef_version": manifest["cef_version"],
        "files": [{"type": "minimal", "name": archive["name"], "sha1": archive["sha1"]}],
    })
print(json.dumps(index, indent=2))
