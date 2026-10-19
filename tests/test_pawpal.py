from datetime import date

from pawpal_system import Pet, Task


def make_task():
    return Task("feed", "08:00", "Breakfast", "", "daily", "Rex", date.today())


def test_mark_complete_sets_completed_true():
    task = make_task()
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_task_count():
    pet = Pet("Rex", 3, "dog")
    before = len(pet.tasks)
    pet.add_task(make_task())
    assert len(pet.tasks) == before + 1
