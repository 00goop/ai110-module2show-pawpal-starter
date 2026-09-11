# PawPal+ — care scheduling in Python

**PawPal+** is a smart pet care management system that helps owners keep their furry friends happy and healthy. It tracks daily routines — feedings, walks, medications, and appointments — while using algorithmic logic to organize and prioritize tasks.

CodePath AI110 coursework. Session state persists only within the running Streamlit session; this is not a medical decision system or a durable account database.

Run `python -m pytest -q` for the scheduling tests; CI runs without external services.

## Features

- **Multi-Pet Management** — Add multiple pets (dogs, cats, birds, etc.) and manage their care schedules independently.
- **Task Scheduling** — Create care tasks with a description, time (HH:MM), and frequency (once, daily, weekly).
- **Sorting by Time** — View all tasks across all pets in chronological order using a lambda-based sort on HH:MM strings.
- **Conflict Detection** — Automatically warns when two tasks are scheduled at the exact same time.
- **Recurring Tasks** — Daily and weekly tasks auto-generate their next occurrence when marked complete, using Python's `timedelta`.
- **Filtering** — Filter tasks by pet name or completion status to focus on what matters.
- **Streamlit UI** — A clean, interactive web interface with `st.session_state` persistence, forms for adding pets/tasks, and real-time conflict warnings.

## Smarter Scheduling

The `Scheduler` class is the algorithmic brain of PawPal+:

- **Sorting:** Uses Python's `sorted()` with a `lambda` key to sort tasks by their `"HH:MM"` time string, producing a chronological daily schedule.
- **Conflict Warnings:** Iterates through the sorted task list and flags adjacent tasks with matching times, returning human-readable warning strings rather than crashing.
- **Recurring Tasks:** When a daily or weekly task is marked complete, `mark_complete()` uses `datetime.strptime` + `timedelta` to auto-create the next occurrence with the same time and frequency.
- **Filtering:** List comprehensions filter the flattened task list by `is_complete` status or `pet_name`, enabling focused views.

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the CLI Demo

```bash
python main.py
```

### Run the Streamlit App

```bash
streamlit run app.py
```

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Category | Tests |
|---|---|
| **Core Behaviors** | Task completion changes status, adding tasks increases count, `pet_name` is stamped, `get_all_tasks()` flattens across pets |
| **Sorting** | Tasks returned in chronological HH:MM order |
| **Recurrence** | Daily tasks create next-day occurrence, weekly tasks create next-week occurrence, one-time tasks return `None` |
| **Conflict Detection** | Same-time tasks are flagged, different-time tasks produce no warnings |
| **Filtering** | Filter by completion status, filter by pet name |
| **Edge Cases** | Pet with no tasks, scheduler with empty owner |

**Confidence Level:** 4/5 stars — 14 tests covering happy paths and edge cases. Future improvements would test invalid time formats, duplicate completions, and large task lists.

## Architecture

The system uses four Python dataclasses:

- **Task** — A single care activity (description, time, frequency, completion status)
- **Pet** — An individual animal with its own task list
- **Owner** — Manages multiple pets; provides `get_all_tasks()` to flatten all pet tasks
- **Scheduler** — The brain that sorts, filters, detects conflicts, and handles recurrence

```
Owner "1" *-- "0..*" Pet : owns
Pet "1" *-- "0..*" Task : has
Scheduler "1" --> "1" Owner : manages
```

## Suggested Workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
