# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
1. Add a pet
2. Schedule a task
3. See today's tasks
- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design has four classes. An Owner has many Pets, and each Pet has many Tasks. The Scheduler uses the Owner to see all the tasks.

- Pet: stores the pet's name, age, species, and its list of tasks. It can add a task.
- Task: stores one care activity (type, time, title, details, frequency, pet name, due date) and whether it is completed. It can mark itself complete.
- Owner: stores the owner's name and their pets. It can add a pet and collect the tasks of all pets together.
- Scheduler: the "brain" that asks the Owner for all tasks and builds today's schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed after Claude reviewed my skeleton. I noticed two problems. First, a Task did not know which pet it belonged to, so once the Owner collected all the tasks together, I could not tell whose task was whose. I added a pet_name field to Task. Second, a Task had no date, so the Scheduler could not know which day a task is due. I also saw that a repeating task marked complete today would look complete for every day. I added a due_date field to Task, so each task has its own completion state and a new task can be created for the next occurrence.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers the time of day (HH:MM), the due date, the frequency (once, daily, or weekly), and which pet the task belongs to. I decided time and date mattered most because a schedule must know when each task happens. I did not add priority or duration yet.

**b. Tradeoffs**

My scheduler only detects conflicts when two tasks have exactly the same date and time. It does not check overlapping durations, for example a 30-minute bath at 10:30 and a feeding at 10:45. I chose this because it is simple and easy to test, and tasks in my design do not have a duration yet.

---

## 3. AI Collaboration

**a. How you used AI**

The most effective feature was agent mode in VS Code, where Claude edited my files directly. It saved time, and asking it to "show me what you changed" let me check every edit.

One suggestion I modified: Claude suggested several changes after reviewing my skeleton, such as an Enum for frequency and remove methods. I kept only pet_name and due_date and postponed the rest, because I wanted to keep the design simple. I also told Claude not to edit my files without asking me first.

As the lead architect, I learned that I decide the design and the AI writes the code. For example, I noticed on my own that a repeating task needs its own completed state, and I checked results by running main.py and pytest.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

Claude suggested adding pet_name and due_date to Task after it reviewed my skeleton. I accepted both, because a task needs to know which pet it belongs to and which day it is due. Claude also suggested other changes, like using an Enum for frequency and adding remove methods. I did not add those yet, because I wanted to keep the design simple for now.

I also noticed on my own that a repeating task should have its own completed state, so finishing it today does not make it look complete on every day.

I let Claude write the logic for the four classes, and then I read each method to understand it. Claude warned me that the schedule includes all tasks, not only today's, and that times are sorted as text. I accepted that for now and kept times in HH:MM format.

I checked the code in two ways. I ran main.py and saw a schedule sorted by time with tasks from two pets. I also ran python -m pytest and all six tests passed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested sorting tasks by time, creating the next task when a daily task is completed, warning about two tasks at the same date and time, a pet with no tasks, marking a task complete, and adding a task to a pet. These tests matter because they cover the main behaviors of the scheduler.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident, about 4 out of 5, because all six tests pass and I also ran main.py and the Streamlit app. Next I would test weekly recurrence, filtering by completion status, overlapping task durations, and times written without a leading zero, like "9:00".

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied that the schedule works for several pets at once, because the Scheduler asks the Owner for all tasks. I am also happy that the Streamlit app keeps its data with st.session_state and shows a yellow warning when two tasks conflict.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add a duration and a priority to each task, use an Enum for frequency, add remove methods for tasks and pets, and store times as real time values instead of text.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI can write code very fast, but I still have to design the system, read the code, and verify it by running it. Drawing the UML first helped me know what to ask for.
