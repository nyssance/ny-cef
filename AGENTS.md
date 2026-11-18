# SDK releases

Publish one GitHub Release tagged `v<version>` per CEF version. Every release ships all four SDK archives together:

- `ny-cef-<version>-macos-arm64.tar.bz2`
- `ny-cef-<version>-windows-x64.tar.bz2`
- `ny-cef-<version>-h264-aac-macos-arm64.tar.bz2`
- `ny-cef-<version>-h264-aac-windows-x64.tar.bz2`

Use the same directory naming, compression, checksum scheme and validation criteria on both platforms. Verify each archive and publish SHA256SUMS covering all four. Keep variant selection with the consuming application. Preserve the standard downloader index when adding media archives. Do not split a codec variant or platform into its own release or mark an incomplete set as a finished release.
