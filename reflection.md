# PawPal+ Project Reflection

## 1. System Design

**Core Actions:**
1. **Add a Pet:** A user should be able to create a profile for a new furry friend (name, species) and save it to their account.
2. **Schedule a Task:** A user should be able to create a new care activity (like a walk or feeding), set a time and frequency, and assign it to a specific pet.
3. **View Today's Schedule:** A user should be able to view a chronological, sorted list of all tasks across all of their pets for the day.

**a. Initial design**

- **Task:** A data container representing a single activity. It holds the description, scheduled time (HH:MM), frequency (once, daily, weekly), and a boolean for completion status.
- **Pet:** Represents an individual animal. It stores basic details (name, species) and maintains a list of `Task` objects specific to that pet.
- **Owner:** Represents the user. It manages a list of `Pet` objects and serves as the primary access point for retrieving pet data.
- **Scheduler:** The "brain" of the operation. It takes in an `Owner`, retrieves all tasks from all associated pets, and contains the algorithmic logic to sort tasks by time, filter them, and check for scheduling conflicts.

**b. Design changes**

- After reviewing the initial skeleton, I realized the `Scheduler` needed a more efficient way to pull tasks from the `Owner` without breaking encapsulation. I updated the `Owner` class to include a `get_all_tasks()` helper method that flattens all pet tasks into a single list before passing it to the `Scheduler` for sorting and conflict detection. I also added a `pet_name` field to `Task` so the Scheduler can trace which pet a task belongs to after flattening.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers **time** (HH:MM format) as the primary constraint for ordering tasks. It also considers **frequency** (once, daily, weekly) to determine whether a completed task should automatically generate its next occurrence. Time was the most important constraint because a pet owner's day revolves around when things need to happen — a medication at 08:00 can't wait until the afternoon.

**b. Tradeoffs**

- The conflict detection algorithm only checks for **exact time matches** (e.g., two tasks both at "08:00") rather than overlapping durations. This means a 30-minute walk at 07:45 and a feeding at 08:00 would not be flagged, even though they could overlap in practice. This tradeoff is reasonable because adding duration-based overlap detection would require tracking task length, which adds significant complexity for a scheduling assistant that is meant to give quick warnings rather than enforce strict constraints.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI (Claude Code in VS Code) across every phase: brainstorming the class design and UML diagram, generating Python dataclass skeletons, scaffolding the full implementation, writing the CLI demo script, generating pytest test cases, and wiring the Streamlit UI. The most helpful prompts were specific and scoped — for example, asking "How should the Scheduler retrieve tasks from the Owner without breaking encapsulation?" led to the `get_all_tasks()` flattening pattern, which became a key design decision. Asking for a Mermaid.js UML diagram with specific class names and relationships gave me a visual blueprint before writing any code.

**b. Judgment and verification**

- When AI initially generated the recurring task logic, it used `timedelta` to advance the time by 1 day for daily tasks. Since we store time as "HH:MM" strings (not full dates), adding `timedelta(days=1)` to a `datetime` parsed from just "08:00" effectively wraps back to the same "08:00" time. I reviewed this behavior and confirmed it was acceptable for our use case — the time string stays the same, which is actually the desired behavior for a daily recurring task (same time, next day). I verified this by running the CLI demo and checking the printed output.

---

## 4. Testing and Verification

**a. What you tested**

- **Core behaviors:** Task completion status changes, task addition increases pet's count, `pet_name` is stamped correctly, and `get_all_tasks()` flattens across pets.
- **Algorithmic logic:** Sorting returns chronological order, daily/weekly recurrence creates new tasks, one-time tasks return `None`, conflict detection flags same-time tasks, filters work by status and pet name.
- **Edge cases:** Pet with no tasks returns empty list, scheduler with an owner who has no pets handles gracefully.
- These tests are important because they verify the system's "brain" — if sorting or conflict detection is broken, the entire schedule is unreliable.

**b. Confidence**

- **Confidence Level: 4/5 stars.** All 14 tests pass, covering happy paths and key edge cases. If I had more time, I would test: tasks with identical descriptions but different pets, marking the same task complete twice, very large task lists for performance, and invalid time formats (e.g., "25:00").

---

## 5. Reflection

**a. What went well**

- The "CLI-first" workflow was the most satisfying part. By building and verifying all logic in `main.py` before touching the Streamlit UI, I caught design issues early (like the need for `pet_name` on Task objects) and had full confidence the backend was solid before wiring it to the frontend.

**b. What you would improve**

- I would add **task duration** as an attribute so conflict detection could flag overlapping time windows, not just exact matches. I would also add date tracking (not just HH:MM time) so the scheduler could manage multi-day views and properly advance recurring tasks to specific future dates.

**c. Key takeaway**

- The most important lesson was that AI is most effective when you treat it as a collaborator, not an autopilot. Acting as the "lead architect" — defining the class structure, reviewing AI-generated code for correctness, and making deliberate design decisions (like the `get_all_tasks()` encapsulation pattern) — produced a cleaner, more maintainable system than accepting every suggestion blindly.
