from dataclasses import dataclass, field, replace
from datetime import date, timedelta


@dataclass
class Task:
    type: str
    time: str
    title: str
    details: str
    frequency: str
    pet_name: str
    due_date: date
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    age: int
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)


class Owner:
    def __init__(self, name: str):
        """Create an owner with a name and no pets."""
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task from all of this owner's pets in one list."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        """Create a scheduler for the given owner."""
        self.owner = owner

    def get_todays_schedule(self) -> list[Task]:
        """Return all of the owner's tasks sorted by time."""
        return sorted(self.owner.get_all_tasks(), key=lambda task: task.time)

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Return tasks sorted by their HH:MM time.

        If no list is given, sorts all of the owner's tasks. Zero-padded
        HH:MM strings sort correctly as plain strings.
        """
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(self, pet_name: str | None = None, completed: bool | None = None) -> list[Task]:
        """Return the owner's tasks filtered by pet name and/or completion status.

        A filter left as None is not applied, so calling with no arguments
        returns every task.
        """
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet_name == pet_name]
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        return tasks

    def detect_conflicts(self) -> list[str]:
        """Return a warning string for each pair of tasks on the same date and time.

        Never raises; returns an empty list when there are no conflicts.
        """
        warnings = []
        seen: dict[tuple, Task] = {}
        for task in self.owner.get_all_tasks():
            key = (task.due_date, task.time)
            if key in seen:
                other = seen[key]
                warnings.append(
                    f"Warning: '{other.title}' ({other.pet_name}) and '{task.title}' "
                    f"({task.pet_name}) are both scheduled for {task.due_date} at {task.time}"
                )
            else:
                seen[key] = task
        return warnings

    def mark_task_complete(self, task: Task) -> Task | None:
        """Mark a task complete and schedule its next occurrence if it recurs.

        Daily tasks get a new task due 1 day later, weekly tasks 7 days later.
        The new task is added to the same pet and returned. Returns None for
        tasks that do not recur.
        """
        task.mark_complete()
        intervals = {"daily": timedelta(days=1), "weekly": timedelta(days=7)}
        interval = intervals.get(task.frequency.lower())
        if interval is None:
            return None

        next_task = replace(task, due_date=task.due_date + interval, completed=False)
        for pet in self.owner.pets:
            if any(t is task for t in pet.tasks):
                pet.add_task(next_task)
                break
        return next_task
