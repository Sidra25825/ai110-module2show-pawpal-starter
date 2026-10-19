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
        self.completed = True


@dataclass
class Pet:
    name: str
    age: int
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_todays_schedule(self) -> list[Task]:
        return sorted(self.owner.get_all_tasks(), key=lambda task: task.time)
