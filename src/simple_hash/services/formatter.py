from datetime import datetime


def format_report(report: dict) -> str:
    metadata = report["metadata"]

    date = datetime.fromisoformat(metadata["date"])
    recursive = "Yes" if metadata["recursive"] else "No"

    lines = []

    # Header
    lines.extend(
        [
            '<span style="font-size: 10pt;">',
            f'<b>Simple Hash {metadata["version"]}</b>',
            "</span>",
            "<br>",
        ]
    )

    # Metadata
    lines.append(f"""
        <table cellspacing="0" cellpadding="">
            <tr>
                <td width="100" style="padding-bottom: 4px;"><b>Date:</b></td>
                <td style="padding-bottom: 4px;">{date}</td>
            </tr>
            <tr>
                <td style="padding-bottom: 4px;"><b>Algorithm:</b></td>
                <td style="padding-bottom: 4px;">{metadata["algorithm"]}</td>
            </tr>
            <tr>
                <td style="padding-bottom: 4px;"><b>Recursive:</b></td>
                <td style="padding-bottom: 4px;">{recursive}</td>
            </tr>
        </table>
        """)

    lines.append("<br>")

    # Compared
    lines.extend(
        [
            "<b>Compared:</b><br>",
            f"&nbsp;&nbsp;{metadata['manifest_1']}<br>",
            f"&nbsp;&nbsp;{metadata['manifest_2']}<br>",
            "<br>",
        ]
    )

    # Result
    lines.append("<b>Result:</b><br>")

    if not metadata["has_issues"]:
        lines.extend(
            [
                '<span style="color: #228B22;">',
                "&nbsp;&nbsp;<b>✓ No differences found.</b>",
                "</span>",
                "<br>",
            ]
        )

        return "\n".join(lines)

    lines.extend(
        [
            '<span style="color: #B22222;">',
            "&nbsp;&nbsp;<b>! Differences found.</b>",
            "</span>",
            "<br><br><br>",
        ]
    )

    # Missing folders
    if report["missing_folders"]:
        count = len(report["missing_folders"])

        lines.append(f"<b>Missing folders ({count})</b><br>")

        for entry in report["missing_folders"]:
            lines.extend(
                [
                    f"&nbsp;&nbsp;• {entry['folder']}<br>",
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Missing from: {entry['reference']}<br>",
                ]
            )

        lines.append("<br>")

    # Missing files
    if report["missing_files"]:
        count = len(report["missing_files"])

        lines.append(f"<b>Missing files ({count})</b><br>")

        for entry in report["missing_files"]:
            lines.extend(
                [
                    f"&nbsp;&nbsp;• {entry['folder']}/{entry['file']}<br>",
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Missing from: {entry['reference']}<br>",
                ]
            )

        lines.append("<br>")

    # Hash mismatches
    if report["hash_mismatches"]:
        count = len(report["hash_mismatches"])

        lines.append(f"<b>Hash mismatches ({count})</b><br>")

        for entry in report["hash_mismatches"]:
            lines.append(
                f"&nbsp;&nbsp;• {entry['folder']}/{entry['file']}<br>",
            )

    return "\n".join(lines)
