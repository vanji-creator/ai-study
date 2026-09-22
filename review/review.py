# Spaced repetition for this repository.
#
# Run it at the start of every session:
#
#     python3 review/review.py
#
# It shows only the cards that are due today. You answer OUT LOUD first, then press
# Enter to see the answer, then say honestly whether you got it.
#
# Useful flags:
#     --stats          how many cards are due, and where they sit. No prompting.
#     --limit 10       stop after ten cards.
#     --block 1        only cards from Block 1.
#     --all            ignore due dates and show everything (a cold re-run).
#
# To test the scheduling without waiting for days to pass:
#     REVIEW_TODAY=2026-10-05 python3 review/review.py --stats
#
# No libraries. Standard library only, so it runs anywhere Python 3 runs.

import argparse
import datetime
import json
import os
import sys

REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS_PATH = os.path.join(REPOSITORY_ROOT, "review", "cards.md")
SCHEDULE_PATH = os.path.join(REPOSITORY_ROOT, "review", "schedule.json")

# Leitner boxes. A card in box 1 comes back tomorrow; a card in box 6 comes back in a
# month. Getting a card right moves it one box up. Getting it wrong sends it to box 1,
# no matter how high it had climbed.
BOX_INTERVAL_DAYS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32}
HIGHEST_BOX = max(BOX_INTERVAL_DAYS)


def today():
    """The date to treat as 'now'. REVIEW_TODAY overrides it, which makes testing possible."""
    override = os.environ.get("REVIEW_TODAY")
    if override:
        return datetime.date.fromisoformat(override)
    return datetime.date.today()


def read_cards(cards_path):
    """Parse review/cards.md into a list of dictionaries.

    The file is plain markdown. A card starts at a line beginning '### id:'.
    'Q:' and 'A:' may both run over several lines.
    """
    if not os.path.exists(cards_path):
        print(f"No card file at {cards_path}")
        sys.exit(1)

    cards = []
    current_card = None
    current_field = None          # which of Q or A we are currently adding lines to

    for raw_line in open(cards_path, encoding="utf-8"):
        line = raw_line.rstrip("\n")

        if line.startswith("### id:"):
            if current_card:
                cards.append(current_card)
            current_card = {"id": line.split("### id:", 1)[1].strip(),
                            "block": "?", "question": "", "answer": ""}
            current_field = None

        elif current_card is None:
            continue              # anything before the first card is a comment

        elif line.startswith("block:"):
            current_card["block"] = line.split("block:", 1)[1].strip()
            current_field = None

        elif line.startswith("Q:"):
            current_card["question"] = line.split("Q:", 1)[1].strip()
            current_field = "question"

        elif line.startswith("A:"):
            current_card["answer"] = line.split("A:", 1)[1].strip()
            current_field = "answer"

        elif current_field and line.strip():
            # a continuation line for whichever field we are inside
            current_card[current_field] += " " + line.strip()

    if current_card:
        cards.append(current_card)

    return cards


def read_schedule(schedule_path):
    if not os.path.exists(schedule_path):
        return {}
    with open(schedule_path, encoding="utf-8") as schedule_file:
        return json.load(schedule_file)


def write_schedule(schedule_path, schedule):
    with open(schedule_path, "w", encoding="utf-8") as schedule_file:
        json.dump(schedule, schedule_file, indent=2, sort_keys=True)
        schedule_file.write("\n")


def entry_for_card(schedule, card_id, todays_date):
    """A card not seen before starts in box 1 and is due immediately."""
    if card_id not in schedule:
        schedule[card_id] = {"box": 1,
                             "due": todays_date.isoformat(),
                             "last_seen": None,
                             "misses": 0}
    return schedule[card_id]


def cards_due(cards, schedule, todays_date, show_everything=False):
    due = []
    for card in cards:
        entry = entry_for_card(schedule, card["id"], todays_date)
        if show_everything or datetime.date.fromisoformat(entry["due"]) <= todays_date:
            due.append(card)
    # oldest due date first, so the most overdue cards come back first
    due.sort(key=lambda card: schedule[card["id"]]["due"])
    return due


def record_answer(schedule, card_id, got_it, todays_date):
    """Move the card up one box, or all the way back to box 1 on a miss."""
    entry = schedule[card_id]
    if got_it:
        entry["box"] = min(entry["box"] + 1, HIGHEST_BOX)
    else:
        entry["box"] = 1
        entry["misses"] += 1

    interval_days = BOX_INTERVAL_DAYS[entry["box"]]
    entry["due"] = (todays_date + datetime.timedelta(days=interval_days)).isoformat()
    entry["last_seen"] = todays_date.isoformat()
    return interval_days


def print_stats(cards, schedule, todays_date):
    due_count = len(cards_due(cards, schedule, todays_date))
    print(f"date            : {todays_date.isoformat()}")
    print(f"cards in file   : {len(cards)}")
    print(f"due now         : {due_count}")
    print()

    cards_per_box = {box: 0 for box in BOX_INTERVAL_DAYS}
    for card in cards:
        cards_per_box[entry_for_card(schedule, card["id"], todays_date)["box"]] += 1

    print("box   next gap   cards")
    for box in sorted(BOX_INTERVAL_DAYS):
        print(f"  {box}   {BOX_INTERVAL_DAYS[box]:>3} days   "
              f"{'#' * cards_per_box[box]} {cards_per_box[box]}")

    struggling = [(card["id"], schedule[card["id"]]["misses"])
                  for card in cards if schedule[card["id"]]["misses"] >= 2]
    if struggling:
        print()
        print("missed twice or more:")
        for card_id, misses in sorted(struggling, key=lambda pair: -pair[1]):
            print(f"  {card_id:<12} {misses} misses")


def run_session(cards_to_review, schedule, todays_date, schedule_path):
    got_it_count = 0
    missed_count = 0

    print(f"{len(cards_to_review)} card(s) due. Answer out loud BEFORE pressing Enter.")
    print("Ctrl-C to stop; everything answered so far is already saved.\n")

    for position, card in enumerate(cards_to_review, start=1):
        print("=" * 70)
        print(f"[{position}/{len(cards_to_review)}]  block {card['block']}  ·  {card['id']}")
        print()
        print(f"  {card['question']}")
        print()
        try:
            input("  press Enter for the answer ")
        except (EOFError, KeyboardInterrupt):
            print("\nstopped.")
            break

        print()
        print(f"  {card['answer']}")
        print()

        answer = ""
        while answer not in ("y", "n"):
            try:
                answer = input("  did you get it? (y/n) ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nstopped.")
                write_schedule(schedule_path, schedule)
                return got_it_count, missed_count

        got_it = answer == "y"
        interval_days = record_answer(schedule, card["id"], got_it, todays_date)
        if got_it:
            got_it_count += 1
            print(f"  -> box {schedule[card['id']]['box']}, back in {interval_days} day(s)\n")
        else:
            missed_count += 1
            print(f"  -> back to box 1, again tomorrow\n")

        write_schedule(schedule_path, schedule)   # save after every card

    return got_it_count, missed_count


def main():
    parser = argparse.ArgumentParser(description="Spaced repetition for the study repository.")
    parser.add_argument("--stats", action="store_true", help="show what is due, then exit")
    parser.add_argument("--limit", type=int, default=0, help="review at most this many cards")
    parser.add_argument("--block", default=None, help="only cards from this block")
    parser.add_argument("--all", action="store_true", help="ignore due dates, show everything")
    arguments = parser.parse_args()

    todays_date = today()
    cards = read_cards(CARDS_PATH)
    schedule = read_schedule(SCHEDULE_PATH)

    if arguments.block is not None:
        cards = [card for card in cards if card["block"] == arguments.block]

    if arguments.stats:
        print_stats(cards, schedule, todays_date)
        write_schedule(SCHEDULE_PATH, schedule)   # so new cards get an entry
        return

    cards_to_review = cards_due(cards, schedule, todays_date, show_everything=arguments.all)
    if arguments.limit:
        cards_to_review = cards_to_review[:arguments.limit]

    if not cards_to_review:
        print(f"Nothing due on {todays_date.isoformat()}. Next due date: "
              f"{min(schedule[card['id']]['due'] for card in cards)}")
        write_schedule(SCHEDULE_PATH, schedule)
        return

    got_it_count, missed_count = run_session(cards_to_review, schedule, todays_date, SCHEDULE_PATH)

    print("=" * 70)
    print(f"got it: {got_it_count}    missed: {missed_count}")
    if missed_count:
        print("The missed ones come back tomorrow. That is the point of them.")


if __name__ == "__main__":
    main()
