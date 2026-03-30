"""PawPal+ Streamlit UI - connected to the backend logic layer."""

import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Page config ---
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart Pet Care Management System")

# --- Session state: persist Owner across refreshes ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")
if "setup_done" not in st.session_state:
    st.session_state.setup_done = False

owner: Owner = st.session_state.owner

# --- Owner Setup ---
if not st.session_state.setup_done:
    st.subheader("Welcome! Let's get started.")
    owner_name = st.text_input("Your name", value="Jordan")
    if st.button("Start PawPal+"):
        st.session_state.owner = Owner(name=owner_name)
        st.session_state.setup_done = True
        st.rerun()
    st.stop()

owner = st.session_state.owner
scheduler = Scheduler(owner=owner)

st.success(f"Logged in as **{owner.name}**")

# --- Sidebar: Add a Pet ---
with st.sidebar:
    st.header("Add a Pet")
    with st.form("add_pet_form", clear_on_submit=True):
        pet_name = st.text_input("Pet name")
        species = st.selectbox("Species", ["dog", "cat", "bird", "fish", "other"])
        submitted_pet = st.form_submit_button("Add Pet")
        if submitted_pet and pet_name:
            owner.add_pet(Pet(name=pet_name, species=species))
            st.rerun()

    if owner.get_all_pets():
        st.divider()
        st.header("Your Pets")
        for pet in owner.get_all_pets():
            st.write(f"**{pet.name}** ({pet.species}) — {len(pet.get_tasks())} tasks")

# --- Main area: Schedule a Task ---
st.subheader("Schedule a Task")

if not owner.get_all_pets():
    st.info("Add a pet in the sidebar to get started.")
    st.stop()

pet_names = [p.name for p in owner.get_all_pets()]

with st.form("add_task_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        task_desc = st.text_input("Task description", placeholder="Morning walk")
        task_time = st.time_input("Scheduled time")
    with col2:
        selected_pet = st.selectbox("Assign to pet", pet_names)
        task_freq = st.selectbox("Frequency", ["once", "daily", "weekly"])
    submitted_task = st.form_submit_button("Add Task")
    if submitted_task and task_desc:
        time_str = task_time.strftime("%H:%M")
        new_task = Task(description=task_desc, time=time_str, frequency=task_freq)
        for pet in owner.get_all_pets():
            if pet.name == selected_pet:
                pet.add_task(new_task)
                break
        st.rerun()

# --- Conflict Warnings ---
conflicts = scheduler.check_conflicts()
if conflicts:
    for warning in conflicts:
        st.warning(f"⚠️ {warning}")

# --- Today's Schedule ---
st.subheader("Today's Schedule")

sorted_tasks = scheduler.sort_by_time()
if not sorted_tasks:
    st.info("No tasks scheduled yet. Add one above!")
else:
    # Build table data
    table_data = []
    for task in sorted_tasks:
        table_data.append({
            "Time": task.time,
            "Pet": task.pet_name,
            "Task": task.description,
            "Frequency": task.frequency,
            "Status": "✅ Done" if task.is_complete else "⏳ Pending",
        })
    st.table(table_data)

# --- Mark Tasks Complete ---
st.subheader("Complete a Task")
pending_tasks = scheduler.filter_by_status(complete=False)
if pending_tasks:
    task_labels = [f"{t.time} - {t.description} ({t.pet_name})" for t in pending_tasks]
    selected_label = st.selectbox("Select a task to mark complete", task_labels)
    if st.button("Mark Complete"):
        idx = task_labels.index(selected_label)
        task_to_complete = pending_tasks[idx]
        next_task = scheduler.mark_task_complete(task_to_complete)
        if next_task:
            for pet in owner.get_all_pets():
                if pet.name == next_task.pet_name:
                    pet.add_task(next_task)
                    break
            st.success(f"Completed '{task_to_complete.description}' — next occurrence scheduled at {next_task.time}")
        else:
            st.success(f"Completed '{task_to_complete.description}'")
        st.rerun()
else:
    st.info("All tasks are complete! 🎉")

# --- Filter by Pet ---
st.subheader("Filter by Pet")
filter_pet = st.selectbox("Show tasks for", ["All"] + pet_names, key="filter_pet")
if filter_pet != "All":
    filtered = scheduler.filter_by_pet(filter_pet)
    if filtered:
        filter_data = []
        for task in filtered:
            filter_data.append({
                "Time": task.time,
                "Task": task.description,
                "Frequency": task.frequency,
                "Status": "✅ Done" if task.is_complete else "⏳ Pending",
            })
        st.table(filter_data)
    else:
        st.info(f"No tasks for {filter_pet}.")
