document.addEventListener("DOMContentLoaded", loadTasks);

function loadTasks() {
    fetch("/api/tasks")
        .then(res => res.json())
        .then(tasks => {
            const list = document.getElementById("taskList");
            list.innerHTML = "";
            tasks.forEach(task => {
                const li = createTaskElement(task);
                list.appendChild(li);
            });
        });
}

function addTask() {
    const input = document.getElementById("taskInput");
    const title = input.value;

    if (!title) return;

    fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title })
    })
    .then(res => res.json())
    .then(() => {
        input.value = "";
        loadTasks();
    });
}

function toggleTask(id, completed) {
    fetch(`/api/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ completed: !completed })
    })
    .then(() => loadTasks());
}

function deleteTask(id) {
    fetch(`/api/tasks/${id}`, {
        method: "DELETE"
    })
    .then(() => loadTasks());
}

function createTaskElement(task) {
    const li = document.createElement("li");
    li.className = task.completed ? "completed" : "";

    li.innerHTML = `
        <span onclick="toggleTask(${task.id}, ${task.completed})">
            ${task.title}
        </span>
        <button onclick="deleteTask(${task.id})">X</button>
    `;

    return li;
}
