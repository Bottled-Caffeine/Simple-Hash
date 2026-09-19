# Simple Hash

A simple utility for saving and verifying file integrity.

## Overview

Simple Hash is a desktop utility for creating and comparing file hash manifests to verify file integrity. It recursively scans directories, records file hashes in a JSON manifest, and compares manifests to detect missing folders, missing or modified files.

## Features

- **Save**: Scan a directory, optionally recursively, and save file hashes and metadata to a JSON manifest, with files grouped by relative folder.

- **Compare**: Compare two hash manifests, generating a report of missing folders, missing files, and files with mismatched hashes.

- **Results**: Display previously generated comparison results in an easy-to-read table.

## Usage

Download the latest release from the Releases page.

## Building from Source

1. **Requirements**<br>
    Install the required dependencies using `pip`:
   
    ```bash
    pip install -r requirements.txt
    ```

    Note: PyQt6 requires Python version 3.10+<br>

2. **Build the executable**<br>
    Using PyInstaller:

    ```bash
    pyinstaller SimpleHash.spec
    ```

## Running from source

From the `src` directory, run:

```bash
python -m simple_hash
```

## Example

Structure of a saved hash manifest, files are stored by folder:

```json
{
    "metadata": {
        ...
    },
    "hashes":{
        ".": {
            "file_1": "file_1_hash",
            "file_2": "file_2_hash",
            ...
        },
        "subfolder": {
            "file_1": "file_1_hash",
            "file_2": "file_2_hash",
            ...
        },
        "subfolder/nested": {
            "file_1": "file_1_hash",
            "file_2": "file_2_hash",
            ...
        },
        ...
    }
}
```
Note: Here, "." represents the root directory.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0-only). See the [LICENSE](./LICENSE) file for details.

## Credits

See [CREDITS](./CREDITS.md) for third-party software, assets, and acknowledgements.
