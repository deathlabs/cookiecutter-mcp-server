RECORDS = {
    "observation-001": "Autobots: more than meets the eye-roll.",
    "observation-002": "Optimus Prime? More like Optimus Past His Prime.",
    "observation-003": "The Autobots' strategy has a few loose Screws.",
    "observation-004": "Bumblebee talks a big game for someone who needs subtitles.",
    "observation-005": "Autobots, roll out—preferably off a cliff.",
    "observation-006": "The Maximals call it evolution; we call it a beast of a mistake.",
    "observation-007": "Optimus Primal is going bananas under pressure.",
    "observation-008": "The Maximals' battle plan is all roar and no bite.",
    "observation-009": "Rhinox charges ahead without thinking it through.",
    "observation-010": "Even a Cheetor can't outrun a bad decision.",
}


def list_records() -> dict[str, str]:
    """List records stored by this MCP server."""
    return RECORDS.copy()


def get_record(record_id: str) -> str:
    """Read a record stored by this MCP server."""
    if record_id not in RECORDS:
        raise ValueError(f"Record {record_id!r} does not exist.")

    return RECORDS[record_id]


def delete_record(record_id: str) -> str:
    """Permanently delete a record stored by this MCP server."""
    if record_id not in RECORDS:
        raise ValueError(f"Record {record_id!r} does not exist.")

    del RECORDS[record_id]
    return f"Deleted record {record_id!r}."
