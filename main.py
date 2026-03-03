import streamlit as st
import sqlite3 as sql


# reduce padding
def reduce_space():
    st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            padding-left: 3rem;
            padding-right: 5rem;
        }
    </style>
    """, unsafe_allow_html=True)

reduce_space()

st.set_page_config(
    page_title="Streamlit To-do App",
    layout="wide",
    page_icon="📝"
)


# Connect to the SQLite database
database = "database.db"

# Create the tasks table if it doesn't exist
def create_table():
    conn = sql.connect(database)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# call the function to create the table
create_table()

# Function to add a task to the database
def add_task(task):
    conn = sql.connect(database)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()


# Function to get all tasks from the database
def get_tasks():
    conn = sql.connect(database)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

# Function to delete a task from the database
def delete_task(task_id):
    conn = sql.connect(database)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

# Function to update a task in the database
def update_task(task_id, new_task):
    conn = sql.connect(database)
    c = conn.cursor()
    c.execute("UPDATE tasks SET task=? WHERE id=?", (new_task, task_id))
    conn.commit()
    conn.close()


# Streamlit UI for adding a new task or editing an existing task
@st.dialog(title="Add a new task", width="medium",on_dismiss="rerun")
def add_task_ui(task,task_id):
    task_input = st.text_input("Enter a new task", placeholder="e.g., Buy groceries", value=task)
    if st.button("Save", type="primary"):
        if task_input and task_id:
            update_task(task_id, task_input)
            st.success("Task updated successfully!")
            st.toast("Task updated successfully!")
        elif task_input and task_id is None:
            add_task(task_input)
            st.success("Task added successfully!")
            st.toast("Task added successfully!")
        else:
            st.toast("Please enter a task.")




# Streamlit UI
st.subheader(":material/book_5: Streamlit To-do App",divider="green")

# Search and Add Task Section
with st.container(border=True):
    st.write("##### Search / Add a new task")
    col1, col2 = st.columns([4, 1],vertical_alignment="top")

    with col1:
        search = st.text_input("Search tasks", 
                            placeholder="Type to search...",
                            label_visibility="collapsed",
                            icon=":material/search:")

    with col2:
        if st.button("Add Task",
                        icon=":material/add_notes:",
                        width="stretch",
                        type="primary"):
            task_input = add_task_ui(task=None,task_id=None)
        
with st.container(border=True):
    # Display existing tasks
    left,right = st.columns([3,.5],vertical_alignment="bottom")
    with left:
        st.subheader("Your Tasks")
    with right:
        layout_style = st.segmented_control(label="Layout Style",
                                            options=[":material/list:", ":material/grid_view:"],
                                            selection_mode="single",
                                            label_visibility="collapsed",
                                            default=":material/list:")
    
    # Filter tasks based on search query
    if search:
        tasks = get_tasks()
        filtered_tasks = [task for task in tasks if search.lower() in task[1].lower()]
    else:
        filtered_tasks = get_tasks()

    # Update the tasks variable to use the filtered tasks
    tasks = filtered_tasks

    # Display tasks 
    # list layout with task on left and edit and delete button on right
    if layout_style == ":material/list:":
        if tasks:
            for task in tasks:
                with st.container(border=True):
                    st.badge("Task ID: " + str(task[0]),color="green")
                    col1,div, col2 = st.columns([5,0.5,0.5],vertical_alignment="center")
                    with col1:
                        
                        st.write(f"{task[1]}")
                    with div:
                        if st.button(f":material/edit:", 
                                    key=f"edit_{task[0]}",
                                    width="stretch",
                                    type="secondary"):
                            task_input = add_task_ui(task=task[1],task_id=task[0])
                    with col2:
                        if st.button(f":material/delete:", 
                                    key=task[0],
                                    width="stretch",
                                    type="primary"):
                            delete_task(task[0])
                            st.toast("Task deleted successfully!", icon="✅")
                            st.rerun()
                    
        else:
            st.caption("No tasks found. Add a task to get started!")

    # grid layout with task on top and edit and delete button below
    if layout_style == ":material/grid_view:":
        if tasks:
            for i in range(0, len(tasks), 3):
                row_tasks = tasks[i:i+3]
                cols = st.columns(3)
                for j, task in enumerate(row_tasks):
                    with cols[j]:
                        with st.container(border=True):
                            st.badge("Task ID: " + str(task[0]),color="green")
                            st.write(f"{task[1]}")
                            c1,c2,c3 = st.columns([1,1,3],vertical_alignment="center")
                            with c1:
                                if st.button(f":material/edit:", 
                                            key=f"edit_{task[0]}",
                                            width="stretch",
                                            type="secondary"):
                                    task_input = add_task_ui(task=task[1],task_id=task[0])
                            with c2:
                                if st.button(f":material/delete:", 
                                            key=task[0],
                                            width="stretch",
                                            type="primary"):
                                    delete_task(task[0])
                                    st.toast("Task deleted successfully!", icon="✅")
                                    st.rerun()
                        
        else:
            st.caption("No tasks found. Add a task to get started!")
