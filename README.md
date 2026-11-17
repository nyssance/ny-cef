# NY CEF

The Chromium Embedded Framework as built by NY ([github.com/nyssance](https://github.com/nyssance)),
with the SurfaceEmbed interfaces for embedding live browser surfaces in an application's own window.
This repository publishes the binary distributions; the bindings at
[nyssance/cef-rs](https://github.com/nyssance/cef-rs) (branch `alwith/surface-embed`) download them
when they are built with the `surface-embed` feature.

Each release holds one version: an `index.json` in the format of the CEF builds index and a minimal
distribution per platform. The bindings of a version take the release tagged `v<version>` and verify
the archive by its checksum; nothing needs to be downloaded by hand.

| Release | Chromium | Platforms |
| --- | --- | --- |
| v158.0.25 | 158.0.8127.0 | macOS arm64 |
| v158.0.21 | 158.0.8127.0 | macOS arm64 |

A build names itself where the people using an application can see it: `chrome://version` says
NY CEF and links here, and Chromium's built-in error page carries a line with this address. The
framework's `Info.plist` says the same.

These are binaries only; the source of the changes they contain is not published. The changes
are the copyright of their author, all rights reserved. The Chromium Embedded Framework they are
built from is the work of its authors under the BSD licence in `LICENSE.txt`, and Chromium and the
third-party components it includes are under the licences in `CREDITS.html` inside each
distribution. They are not stock CEF builds and are not interchangeable with them: an application
must use the bindings of the same version.

## Media build candidate

The optional `h264-aac` Release variant is described in [build/README.md](build/README.md).
Its source identity and validation status are recorded in [build/h264-aac.json](build/h264-aac.json).
It is a candidate, not an additional published release in the table above.
