# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## ✨ Features

- **Sorting by time**: tasks are shown in order of their `HH:MM` time, no matter what order they were added in.
- **Filtering by pet and status**: show only one pet's tasks, only completed tasks, only open tasks, or a combination.
- **Conflict warnings**: when two tasks share the same date and time, the app shows a warning instead of failing.
- **Daily and weekly recurrence**: marking a daily or weekly task complete automatically adds its next occurrence (+1 day or +7 days) to the same pet.

## 🖥️ Sample Output

```
Today's Schedule
08:00 Feed Adam Adam
13:00 Free flight time Adam
19:00 Give Bella medicine Bella
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The tests in `tests/test_pawpal.py` cover:

- **Sorting**: tasks added out of order come back in chronological order.
- **Recurrence**: completing a daily task creates a new, incomplete task due the next day.
- **Conflict detection**: two tasks on the same date and time produce a warning.
- **Pet with no tasks**: sorting, filtering, and conflict detection return empty lists without errors.

They also check that a task can be marked complete and that adding a task increases the pet's task count.

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\sidra\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 6 items

tests\test_pawpal.py ......                                              [100%]

============================== 6 passed in 0.03s ==============================
```

**Confidence:** ⭐⭐⭐⭐☆ (4/5). The main scheduling behaviors are tested and pass. Weekly recurrence, filtering by completion status, and overlapping task durations are not tested yet.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time` | Orders tasks by their `HH:MM` time. Sorts all of the owner's tasks unless given a list. |
| Filtering | `Scheduler.filter_tasks` | Filters by `pet_name`, `completed`, or both. A filter left as `None` is skipped. |
| Conflict handling | `Scheduler.detect_conflicts` | Returns a warning string for each pair of tasks with the same `due_date` and `time`. Never raises an error. |
| Recurring tasks | `Scheduler.mark_task_complete` | Marks a task done. For daily (+1 day) or weekly (+7 days) tasks, it adds the next occurrence to the same pet. |

## 📸 Demo Walkthrough

### Main UI features

Start the app with `streamlit run app.py`. The page has four parts:

- **Owner**: set the owner's name.
- **Add a Pet**: enter a name, age, and species.
- **Schedule a Task**: pick a pet and enter a title, type, frequency (once, daily, or weekly), time, due date, and details.
- **Schedule**: a table of tasks sorted by time, with filters for pet and status, conflict warnings above it, and a "Mark complete" button below it.

### Example workflow

1. Under **Add a Pet**, enter "Mochi", age 3, species "dog", and click **Add pet**. A success message confirms it.
2. Under **Schedule a Task**, choose Mochi, enter "Breakfast", set the frequency to "daily", pick 08:00 and today's date, and click **Add task**. A success message confirms it.
3. Add a second task for Mochi at 08:00 on the same date. The **Schedule** section now shows a yellow conflict warning naming both tasks.
4. View today's schedule in the **Schedule** table, sorted by time. Use **Filter by pet** and **Filter by status** to narrow it down.
5. Under **Mark a Task Complete**, choose "Breakfast" and click **Mark complete**. The table shows Breakfast as done and a new Breakfast task due tomorrow.

### Key Scheduler behaviors

`python main.py` runs the same logic without the UI. It adds tasks out of order, then sorts them, filters them, detects a conflict, and completes a daily task:

```
Tasks in the order they were added
13:00 Free flight time Adam
08:00 Feed Adam Adam
19:00 Give Bella medicine Bella
10:30 Bath time Bella

Sorted by time
08:00 Feed Adam Adam
10:30 Bath time Bella
13:00 Free flight time Adam
19:00 Give Bella medicine Bella

Filtered: Adam's tasks
13:00 Free flight time Adam
08:00 Feed Adam Adam

Conflict check
Warning: 'Feed Adam' (Adam) and 'Feed Bella' (Bella) are both scheduled for 2026-10-19 at 08:00

Marking 'Feed Adam' complete
Next occurrence: Feed Adam 08:00 2026-10-20 completed: False

Filtered: completed tasks
2026-10-19 08:00 Feed Adam Adam

Filtered: incomplete tasks for Adam
2026-10-19 13:00 Free flight time Adam
2026-10-20 08:00 Feed Adam Adam
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

## Implementation Summary

PawPal+ models an owner's pets and their care tasks, and builds a daily schedule from them. The logic lives in `pawpal_system.py` and has four classes:

- **Task**: one care activity (type, time, title, details, frequency, pet name, due date). `mark_complete()` marks it done.
- **Pet**: a pet's name, age, and species, plus its list of tasks. `add_task()` adds a task to that list.
- **Owner**: the owner's name and list of pets. `add_pet()` adds a pet, and `get_all_tasks()` gathers the tasks from every pet into one list.
- **Scheduler**: takes an `Owner`. `get_todays_schedule()` collects all of that owner's tasks and returns them sorted by time.

An Owner has Pets, each Pet has Tasks, and the Scheduler reads through the Owner to build the schedule. The class diagram is in `diagrams/uml_draft.mmd`, and tests are in `tests/test_pawpal.py`.
