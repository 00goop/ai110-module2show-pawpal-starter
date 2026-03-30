"""PawPal+ - Smart Pet Care Management System (Logic Layer)."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    """A single pet care activity."""
    description: str
    time: str  # "HH:MM" format
    frequency: str = "once"  # "once", "daily", "weekly"
    is_complete: bool = False
    pet_name: str = ""

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task complete; return next occurrence if recurring."""
        self.is_complete = True
        if self.frequency in ("daily", "weekly"):
            delta = timedelta(days=1) if self.frequency == "daily" else timedelta(weeks=1)
            current = datetime.strptime(self.time, "%H:%M")
            next_time = current + delta
            return Task(
                description=self.description,
                time=next_time.strftime("%H:%M"),
                frequency=self.frequency,
                pet_name=self.pet_name,
            )
        return None


@dataclass
class Pet:
    """An individual pet with its own task list."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's schedule."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    """A pet owner who manages multiple pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def get_all_pets(self) -> List[Pet]:
        """Return all pets."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Flatten all tasks from all pets into a single list."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


@dataclass
class Scheduler:
    """The brain - retrieves, sorts, filters, and manages tasks."""
    owner: Owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks across all pets via the owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> List[Task]:
        """Return tasks sorted chronologically by HH:MM time string."""
        return sorted(self.get_all_tasks(), key=lambda t: t.time)

    def filter_by_status(self, complete: bool = False) -> List[Task]:
        """Filter tasks by completion status."""
        return [t for t in self.get_all_tasks() if t.is_complete == complete]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Filter tasks belonging to a specific pet."""
        return [t for t in self.get_all_tasks() if t.pet_name == pet_name]

    def check_conflicts(self) -> List[str]:
        """Detect tasks at the exact same time and return warning strings."""
        tasks = self.sort_by_time()
        warnings = []
        for i in range(len(tasks) - 1):
            if tasks[i].time == tasks[i + 1].time:
                warnings.append(
                    f"Conflict at {tasks[i].time}: "
                    f"'{tasks[i].description}' ({tasks[i].pet_name}) "
                    f"and '{tasks[i + 1].description}' ({tasks[i + 1].pet_name})"
                )
        return warnings

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and return the auto-generated next occurrence."""
        return task.mark_complete()
