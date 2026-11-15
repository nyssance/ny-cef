# CEF builds

Binary distributions of the Chromium Embedded Framework built with the SurfaceEmbed interfaces,
for the bindings at [nyssance/cef-rs](https://github.com/nyssance/cef-rs) (branch
`alwith/surface-embed`) to download when they are built with the `surface-embed` feature.

Each release holds one version: an `index.json` in the format of the CEF builds index and a minimal
distribution per platform. The bindings of a version take the release tagged `v<version>` and verify
the archive by its checksum; nothing needs to be downloaded by hand.

| Release | Chromium | Platforms |
| --- | --- | --- |
| v158.0.21 | 158.0.8127.0 | macOS arm64 |

These are binaries only. The Chromium Embedded Framework is distributed under the BSD licence in
`LICENSE.txt`; the licences of Chromium and of the third-party components it includes are in
`CREDITS.html` inside each distribution. They are not stock CEF builds and are not interchangeable
with them: an application must use the bindings of the same version.
