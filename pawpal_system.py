from dataclasses import dataclass, field
from datetime import date


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
