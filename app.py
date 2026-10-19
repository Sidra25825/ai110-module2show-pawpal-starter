import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    age = st.number_input("Age", min_value=0, max_value=50, value=3)
with col3:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, int(age), species))
    st.success(f"Added {pet_name}.")

st.subheader("Schedule a Task")
if not owner.pets:
    st.info("Add a pet first.")
else:
    pet_index = st.selectbox(
        "Pet", range(len(owner.pets)), format_func=lambda i: owner.pets[i].name
    )
    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        task_type = st.selectbox("Type", ["walk", "feed", "meds", "grooming", "enrichment", "other"])
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    with col2:
        task_time = st.time_input("Time")
        due_date = st.date_input("Due date")
        details = st.text_input("Details", value="")

    if st.button("Add task"):
        pet = owner.pets[pet_index]
        pet.add_task(
            Task(task_type, task_time.strftime("%H:%M"), task_title, details, frequency, pet.name, due_date)
        )
        st.success(f"Added '{task_title}' for {pet.name}.")

st.divider()

st.subheader("Schedule")
scheduler = Scheduler(owner)

for warning in scheduler.detect_conflicts():
    st.warning(warning)

col1, col2 = st.columns(2)
with col1:
    pet_filter = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets], key="pet_filter")
with col2:
    status_filter = st.selectbox("Filter by status", ["All", "Not done", "Done"], key="status_filter")

completed = {"All": None, "Not done": False, "Done": True}[status_filter]
tasks = scheduler.filter_tasks(pet_name=None if pet_filter == "All" else pet_filter, completed=completed)
schedule = scheduler.sort_by_time(tasks)

if schedule:
    st.table(
        [
            {
                "Date": str(t.due_date),
                "Time": t.time,
                "Task": t.title,
                "Pet": t.pet_name,
                "Type": t.type,
                "Frequency": t.frequency,
                "Done": t.completed,
            }
            for t in schedule
        ]
    )
else:
    st.info("No tasks match. Add one above or change the filters.")

st.subheader("Mark a Task Complete")
if "complete_message" in st.session_state:
    st.success(st.session_state.pop("complete_message"))

open_tasks = scheduler.sort_by_time(scheduler.filter_tasks(completed=False))
if not open_tasks:
    st.info("No open tasks.")
else:
    task_index = st.selectbox(
        "Task",
        range(len(open_tasks)),
        format_func=lambda i: f"{open_tasks[i].due_date} {open_tasks[i].time} - {open_tasks[i].title} ({open_tasks[i].pet_name})",
        key="complete_task",
    )
    if st.button("Mark complete"):
        task = open_tasks[task_index]
        next_task = scheduler.mark_task_complete(task)
        message = f"Completed '{task.title}'."
        if next_task:
            message += f" Next {task.frequency} occurrence added for {next_task.due_date}."
        st.session_state.complete_message = message
        st.rerun()
