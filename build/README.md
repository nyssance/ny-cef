# H.264/AAC Release build

This variant changes build arguments, not the HTML video implementation. Keep the existing NY CEF SurfaceEmbed sources and platform setup. The public repository does not contain the private source changes; cloning upstream CEF alone cannot reproduce NY CEF.

## Source identity

`h264-aac.json` records the current macOS candidate's CEF commit, Chromium base, depot_tools revision, and tracked Chromium patch digest. The patch digest includes applied CEF patches. It is a provenance check, not a downloadable patch. Windows is an unverified target until its own build and playback checks pass.

The build agent should inspect the repositories already present on the machine and find the Chromium `src` directory, its prepared `cef` checkout, and depot_tools. Verify the manifest's source revisions before building. Do not replace existing private patches with upstream source or silently use an older source bundle. If the required NY source revision is unavailable, report the missing revision rather than producing a stock CEF package under the NY name.

## Build

Use Visual Studio C++ tools, the Windows SDK required by the pinned Chromium checkout, and depot_tools on Windows. Use its supported Xcode toolchain on macOS. Follow the prepared checkout's dependency setup; do not modify global Git settings or download a second source tree unnecessarily.

Reuse the existing working Release output directory. Preserve the previous distributable and back up `args.gn` before changing arguments. Do not relocate the build directory or clear its cache: compiler modules and dependency records may be path-sensitive. Start with the existing working platform `args.gn`, then merge `h264-aac.gn` as overrides, with exactly one assignment per key. Set `target_cpu = "x64"` on Windows and `target_cpu = "arm64"` on macOS. Set `use_remoteexec = false` unless a working remote build service has explicitly been configured. Preserve all other required NY build arguments.

Run from Chromium `src`, with depot_tools on PATH:

```sh
gn gen out/Official_GN_arm64
# Use the native siso executable, siso.exe on Windows.
third_party/siso/cipd/siso ninja -C out/Official_GN_arm64 -local_jobs=10 -re_exec_enable=false cef_framework cefclient cef_sandbox
```

Choose local parallelism for the machine; ten jobs is the current 12-logical-core Mac setting, not a universal requirement. Resume with the same output directory and command. Do not clean caches on an interrupted build. Siso's direct `-j` option is unsupported; use `-local_jobs`.

The command above shows the existing macOS output directory. On Windows, use its existing Release output path and Windows distribution targets instead; the framework target above is macOS-specific. The abandoned macOS `out/TVMedia_GN_arm64` build is stopped and retained; the active media build now reuses `out/Official_GN_arm64`. A dry-run count can underestimate work caused by newly generated buildflag headers; verify the actual build graph after those headers are generated.

## Validate and package

Before publishing, use the matching NY bindings and an isolated application identity/profile to verify:

- MP4 with H.264 video and AAC audio loads through an ordinary HTML `video` element.
- Frames advance, audio is audible, seeking and repeated pause/resume work, and audio/video remain synchronized.
- Multiple canvas videos retain correct clipping, transforms, and stacking; hidden videos stop decoding when paused by the host.
- Record the actual decoder selected and whether hardware acceleration is active; `canPlayType` alone is insufficient.
- SurfaceEmbed remains functional. Test macOS ARM64 and Windows x64 separately; never report one platform's result for the other.

Create a complete minimal SDK using the checkout's existing distribution process, including headers, libraries, resources, license notices and CREDITS.html. The upstream distribution tool assumes particular output directory names: do not accidentally package an older default output directory. Verify that the packaged binary is the candidate that passed playback tests. Do not publish a framework/DLL alone as a complete SDK. Build the archive from a clean SDK directory, not a download cache. Reject nested SDK archives, versioned download directories, and duplicate framework binaries before uploading. Verify the packaged framework digest matches the tested binary and check the remote asset state and SHA-256 after upload.

Artifact names:

```text
ny-cef-158.0.25-h264-aac-macos-arm64.tar.bz2
ny-cef-158.0.25-h264-aac-windows-x64.tar.bz2
```

All SDK archives use `.tar.bz2`, with one top-level directory matching the archive basename. Repackage an existing SDK with `python3 build/repack.py SOURCE DESTINATION`; this verifies every SDK file after compression. Default builds have no `standard` suffix: `ny-cef-158.0.25-macos-arm64.tar.bz2` and `ny-cef-158.0.25-windows-x64.tar.bz2`. Record codec capabilities and SHA-256 checksums in the artifact manifest. Generate each release index from its manifests with `python3 build/index.py manifest-macos-arm64.json [manifest-windows-x64.json] > index.json`; omit unpublished platforms. Existing download clients use the CEF archive/index schema: each release has an `index.json` using the unified names. Use `@nyssance/cef-rs` 158.0.26 or newer for these names. Select the media build explicitly with `CEF_DOWNLOAD_URL=https://github.com/nyssance/ny-cef/releases/download/v158.0.25-h264-aac`; the default release remains unchanged in codec capability. A missing platform in that index is unsupported, not a request to download the standard build.

The variant name identifies enabled codecs, not a patent license. Preserve third-party notices and do not claim that this build grants downstream patent coverage. Publication follows platform validation and confirmation of the distributor's licensing position.
