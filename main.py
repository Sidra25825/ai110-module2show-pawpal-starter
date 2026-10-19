from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date
owner = Owner("Momen")
adam = Pet("Adam", 6, "cockatiel")
owner.add_pet(adam)
bella = Pet("Bella", 1, "cockatiel")
owner.add_pet(bella)

# Tasks are added out of order on purpose to show sorting
task3 = Task("medication", "19:00", "Give Bella medicine", "One drop in water", "daily", "Bella", date.today())
bella.add_task(task3)

task2 = Task("walk", "13:00", "Free flight time", "Outside in the garden", "daily", "Adam", date.today())
adam.add_task(task2)

task1 = Task("feeding", "08:00", "Feed Adam", "Seeds and fresh water", "daily", "Adam", date.today())
adam.add_task(task1)

task4 = Task("grooming", "10:30", "Bath time", "Shallow dish of water", "weekly", "Bella", date.today())
bella.add_task(task4)

scheduler = Scheduler(owner)

print("Tasks in the order they were added")
for task in owner.get_all_tasks():
    print(task.time, task.title, task.pet_name)

print("\nSorted by time")
for task in scheduler.sort_by_time():
    print(task.time, task.title, task.pet_name)

print("\nFiltered: Adam's tasks")
for task in scheduler.filter_tasks(pet_name="Adam"):
    print(task.time, task.title, task.pet_name)

# Two tasks at the same time to trigger a conflict
task5 = Task("feeding", "08:00", "Feed Bella", "Seeds and fresh water", "daily", "Bella", date.today())
bella.add_task(task5)

print("\nConflict check")
for warning in scheduler.detect_conflicts():
    print(warning)

print("\nMarking 'Feed Adam' complete")
next_task = scheduler.mark_task_complete(task1)
print("Next occurrence:", next_task.title, next_task.time, next_task.due_date, "completed:", next_task.completed)

print("\nFiltered: completed tasks")
for task in scheduler.filter_tasks(completed=True):
    print(task.due_date, task.time, task.title, task.pet_name)

print("\nFiltered: incomplete tasks for Adam")
for task in scheduler.filter_tasks(pet_name="Adam", completed=False):
    print(task.due_date, task.time, task.title, task.pet_name)
