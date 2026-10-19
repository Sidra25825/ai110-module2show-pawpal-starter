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

st.subheader("Today's Schedule")
schedule = Scheduler(owner).get_todays_schedule()
if schedule:
    st.table(
        [
            {"Time": t.time, "Task": t.title, "Pet": t.pet_name, "Type": t.type, "Done": t.completed}
            for t in schedule
        ]
    )
else:
    st.info("No tasks yet. Add one above.")
