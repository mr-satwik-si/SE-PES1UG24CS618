"""Conference room and equipment scheduling utilities."""

import json
import logging
from pathlib import Path
from typing import Optional, Sequence

reservations = {}
equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
conflicts = []
NEXT_RESERVATION = 1


def schedule_room(
    room_id: str,
    time_slot: str,
    equipment_list: Optional[Sequence[str]] = None,
) -> int:
    """Book a room and reserve requested equipment."""
    if equipment_list is None:
        equipment_list = []

    for reservation in reservations.values():
        if reservation["room"] == room_id and reservation["slot"] == time_slot:
            conflicts.append(f"{room_id} double-booked at {time_slot}")

    for equipment in equipment_list:
        if equipment not in equipment_pool:
            raise ValueError(f"Unknown equipment: {equipment}")
        if equipment_pool[equipment] <= 0:
            raise ValueError(f"Equipment unavailable: {equipment}")

    for equipment in equipment_list:
        equipment_pool[equipment] -= 1

    reservation_id = max(reservations, default=0) + 1
    reservations[reservation_id] = {
        "room": room_id,
        "slot": time_slot,
        "equipment": list(equipment_list),
    }
    return reservation_id


def cancel_reservation(reservation_id: int) -> bool:
    """Cancel a reservation and return its equipment to the pool."""
    reservation = reservations.get(reservation_id)
    if reservation is None:
        return False

    for equipment in reservation["equipment"]:
        equipment_pool[equipment] += 1
    del reservations[reservation_id]
    return True


def slot_hours(time_slot: str) -> int:
    """Return the duration of a time slot formatted as 'start-end'."""
    try:
        start_text, end_text = time_slot.split("-", maxsplit=1)
        start, end = int(start_text), int(end_text)

    except (AttributeError, TypeError, ValueError) as exc:
        message = (
            "Time slot must be formatted as 'start-end', e.g. '09-11'."
        )
        raise ValueError(message) from exc
    if not (0 <= start <= 23 and 0 <= end <= 24):
        raise ValueError("Time values must be within the 24-hour clock.")
    if end <= start:
        raise ValueError("End time must be later than start time.")
    return end - start


def export_schedule(file: str = "schedule.json") -> None:
    """Export current reservations as JSON."""
    output_path = Path(file)
    with output_path.open("w", encoding="utf-8") as schedule_file:
        json.dump(reservations, schedule_file, indent=2)


def log_conflicts(file: str = "conflicts.log") -> None:
    """Append recorded reservation conflicts to a log file."""
    if not conflicts:
        return

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    logger = logging.getLogger("room_scheduler")
    output_path = Path(file)
    with output_path.open("a", encoding="utf-8") as log_file:
        for conflict in conflicts:
            log_file.write(f"{conflict}\n")
            logger.info("%s", conflict)


def main() -> None:
    """Run a small demonstration of the scheduler."""
    first = schedule_room("Board-1", "09-11")
    schedule_room("Board-1", "09-11")
    second = schedule_room("Huddle-3", "10-12")
    slot_length = slot_hours(reservations[second]["slot"])
    print("Slot length for second reservation:", slot_length)
    print("Cancellation of missing reservation:", cancel_reservation(77))

    slot = (
        input("Slot for Board-2, like 10-12 (Enter for 10-12): ").strip()
        or "10-12"
    )
    slot_hours(slot)
    schedule_room("Board-2", slot, ["projector", "webcam"])
    export_schedule()
    log_conflicts()
    print("Equipment left:", equipment_pool)
    print("Reservations:", reservations)
    print("First reservation ID:", first)


if __name__ == "__main__":
    main()
