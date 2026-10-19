from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date
owner = Owner("Momen")
adam = Pet("Adam", 6, "cockatiel")
owner.add_pet(adam)
bella = Pet("Bella", 1, "cockatiel")
owner.add_pet(bella)

task1 = Task("feeding", "08:00", "Feed Adam", "Seeds and fresh water", "daily", "Adam", date.today())
adam.add_task(task1)

task2 = Task("walk", "13:00", "Free flight time", "Outside in the garden", "daily", "Adam", date.today())
adam.add_task(task2)

task3 = Task("medication", "19:00", "Give Bella medicine", "One drop in water", "daily", "Bella", date.today())
bella.add_task(task3)

scheduler = Scheduler(owner)

schedule = scheduler.get_todays_schedule()
print("Today's Schedule")
for task in schedule:
    print(task.time, task.title, task.pet_name)