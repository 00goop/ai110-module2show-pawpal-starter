"""PawPal+ test suite - verifies core behaviors and algorithmic logic."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


# --- Phase 2: Core behavior tests ---

def test_task_completion_changes_status():
    """Verify that mark_complete() sets is_complete to True."""
    task = Task(description="Walk", time="08:00")
    assert task.is_complete is False
    task.mark_complete()
    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    """Verify that adding a task increases the pet's task list length."""
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(description="Walk", time="08:00"))
    assert len(pet.get_tasks()) == 1
    pet.add_task(Task(description="Feed", time="12:00"))
    assert len(pet.get_tasks()) == 2


def test_add_task_sets_pet_name():
    """Verify that add_task stamps the pet's name onto the task."""
    pet = Pet(name="Whiskers", species="cat")
    task = Task(description="Feed", time="09:00")
    pet.add_task(task)
    assert task.pet_name == "Whiskers"


def test_owner_get_all_tasks_flattens():
    """Verify that get_all_tasks returns tasks from all pets."""
    owner = Owner(name="Jordan")
    p1 = Pet(name="Mochi", species="dog")
    p2 = Pet(name="Whiskers", species="cat")
    p1.add_task(Task(description="Walk", time="07:00"))
    p2.add_task(Task(description="Feed", time="08:00"))
    owner.add_pet(p1)
    owner.add_pet(p2)
    assert len(owner.get_all_tasks()) == 2


# --- Phase 4/5: Algorithmic tests ---

def test_sort_by_time_returns_chronological_order():
    """Verify tasks are sorted by HH:MM time string."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Evening walk", time="18:00"))
    pet.add_task(Task(description="Morning walk", time="07:30"))
    pet.add_task(Task(description="Lunch feed", time="12:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == ["07:30", "12:00", "18:00"]


def test_recurrence_daily_creates_next_task():
    """Verify that completing a daily task returns a new task for the next day."""
    task = Task(description="Walk", time="08:00", frequency="daily", pet_name="Mochi")
    next_task = task.mark_complete()
    assert task.is_complete is True
    assert next_task is not None
    assert next_task.frequency == "daily"
    assert next_task.is_complete is False
    assert next_task.pet_name == "Mochi"


def test_recurrence_weekly_creates_next_task():
    """Verify that completing a weekly task returns a new task."""
    task = Task(description="Grooming", time="10:00", frequency="weekly", pet_name="Mochi")
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.frequency == "weekly"
    assert next_task.is_complete is False


def test_once_task_returns_none_on_complete():
    """Verify that a one-time task returns None (no recurrence)."""
    task = Task(description="Vet visit", time="14:00", frequency="once")
    next_task = task.mark_complete()
    assert next_task is None


def test_conflict_detection_flags_same_time():
    """Verify the Scheduler detects tasks at the exact same time."""
    owner = Owner(name="Jordan")
    p1 = Pet(name="Mochi", species="dog")
    p2 = Pet(name="Whiskers", species="cat")
    p1.add_task(Task(description="Walk", time="08:00"))
    p2.add_task(Task(description="Feed", time="08:00"))
    owner.add_pet(p1)
    owner.add_pet(p2)
    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.check_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_no_conflicts_when_times_differ():
    """Verify no warnings when all task times are unique."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Walk", time="07:00"))
    pet.add_task(Task(description="Feed", time="12:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)
    assert scheduler.check_conflicts() == []


def test_filter_by_status():
    """Verify filtering separates complete from incomplete tasks."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    t1 = Task(description="Walk", time="07:00")
    t2 = Task(description="Feed", time="12:00")
    pet.add_task(t1)
    pet.add_task(t2)
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)
    t1.mark_complete()
    assert len(scheduler.filter_by_status(complete=True)) == 1
    assert len(scheduler.filter_by_status(complete=False)) == 1


def test_filter_by_pet():
    """Verify filtering returns only tasks for the named pet."""
    owner = Owner(name="Jordan")
    p1 = Pet(name="Mochi", species="dog")
    p2 = Pet(name="Whiskers", species="cat")
    p1.add_task(Task(description="Walk", time="07:00"))
    p2.add_task(Task(description="Feed", time="08:00"))
    p2.add_task(Task(description="Play", time="17:00"))
    owner.add_pet(p1)
    owner.add_pet(p2)
    scheduler = Scheduler(owner=owner)
    assert len(scheduler.filter_by_pet("Mochi")) == 1
    assert len(scheduler.filter_by_pet("Whiskers")) == 2


def test_pet_with_no_tasks():
    """Verify a pet with no tasks returns an empty list."""
    pet = Pet(name="Buddy", species="dog")
    assert pet.get_tasks() == []


def test_scheduler_with_empty_owner():
    """Verify the scheduler handles an owner with no pets gracefully."""
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner=owner)
    assert scheduler.sort_by_time() == []
    assert scheduler.check_conflicts() == []
