from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_sort_by_time_returns_chronological_order():
    owner = Owner("Sam")
    pet = Pet("Rex", 3, "dog")
    owner.add_pet(pet)
    pet.add_task(Task("walk", "18:00", "Evening walk", "", "daily", "Rex", date.today()))
    pet.add_task(Task("feed", "08:00", "Breakfast", "", "daily", "Rex", date.today()))
    pet.add_task(Task("play", "12:30", "Fetch", "", "daily", "Rex", date.today()))

    times = [task.time for task in Scheduler(owner).sort_by_time()]
    assert times == ["08:00", "12:30", "18:00"]


def test_completing_daily_task_creates_next_day_task():
    owner = Owner("Sam")
    pet = Pet("Rex", 3, "dog")
    owner.add_pet(pet)
    task = make_task()
    pet.add_task(task)

    next_task = Scheduler(owner).mark_task_complete(task)

    assert task.completed is True
    assert next_task.due_date == task.due_date + timedelta(days=1)
    assert next_task.completed is False
    assert len(pet.tasks) == 2


def test_same_date_and_time_produces_conflict_warning():
    owner = Owner("Sam")
    pet = Pet("Rex", 3, "dog")
    owner.add_pet(pet)
    pet.add_task(Task("feed", "08:00", "Breakfast", "", "daily", "Rex", date.today()))
    pet.add_task(Task("meds", "08:00", "Pill", "", "daily", "Rex", date.today()))

    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1


def test_pet_with_no_tasks():
    owner = Owner("Sam")
    owner.add_pet(Pet("Rex", 3, "dog"))
    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time() == []
    assert scheduler.filter_tasks(pet_name="Rex") == []
    assert scheduler.detect_conflicts() == []
