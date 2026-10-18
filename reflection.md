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
- Task: stores one care activity (type, time, title, details, frequency) and whether it is completed. It can mark itself complete.
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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
