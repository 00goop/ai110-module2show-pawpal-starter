"""PawPal+ CLI Demo — verifies backend logic in the terminal."""

from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    # --- Create Owner ---
    owner = Owner(name="Jordan")

    # --- Create Pets ---
    mochi = Pet(name="Mochi", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    # --- Add Tasks (intentionally out of order) ---
    mochi.add_task(Task(description="Morning walk", time="07:30", frequency="daily"))
    mochi.add_task(Task(description="Breakfast", time="08:00", frequency="daily"))
    mochi.add_task(Task(description="Vet appointment", time="14:00"))
    whiskers.add_task(Task(description="Litter box clean", time="08:00", frequency="daily"))
    whiskers.add_task(Task(description="Play session", time="17:00"))
    whiskers.add_task(Task(description="Evening feeding", time="18:30", frequency="daily"))

    # --- Build Scheduler ---
    scheduler = Scheduler(owner=owner)

    # --- Print Today's Schedule (sorted) ---
    print(f"\n{'='*50}")
    print(f"  PawPal+ — Today's Schedule for {owner.name}")
    print(f"{'='*50}\n")

    for task in scheduler.sort_by_time():
        status = "Done" if task.is_complete else "Pending"
        print(f"  {task.time}  |  {task.pet_name:<10}  |  {task.description:<20}  |  [{status}]")

    # --- Check Conflicts ---
    conflicts = scheduler.check_conflicts()
    if conflicts:
        print(f"\n  {'!'*40}")
        print("  SCHEDULING CONFLICTS DETECTED:")
        for warning in conflicts:
            print(f"    - {warning}")
        print(f"  {'!'*40}")

    # --- Mark a task complete and show recurrence ---
    print(f"\n{'='*50}")
    print("  Testing Recurrence: marking 'Morning walk' complete...")
    print(f"{'='*50}\n")

    walk_task = mochi.get_tasks()[0]
    next_task = scheduler.mark_task_complete(walk_task)
    print(f"  Original: '{walk_task.description}' at {walk_task.time} — Complete: {walk_task.is_complete}")
    if next_task:
        print(f"  Next occurrence auto-created: '{next_task.description}' at {next_task.time}")
        mochi.add_task(next_task)

    # --- Filter by pet ---
    print(f"\n{'='*50}")
    print("  Mochi's Tasks:")
    print(f"{'='*50}\n")

    for task in scheduler.filter_by_pet("Mochi"):
        status = "Done" if task.is_complete else "Pending"
        print(f"  {task.time}  |  {task.description:<20}  |  [{status}]")

    # --- Filter incomplete ---
    print(f"\n{'='*50}")
    print("  Remaining (incomplete) Tasks:")
    print(f"{'='*50}\n")

    for task in scheduler.filter_by_status(complete=False):
        print(f"  {task.time}  |  {task.pet_name:<10}  |  {task.description}")

    print()


if __name__ == "__main__":
    main()
