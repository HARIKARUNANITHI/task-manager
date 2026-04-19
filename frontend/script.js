let token = "";

const BASE_URL = "http://localhost:8000";

// REGISTER
async function register() {
    let res = await fetch(`${BASE_URL}/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: document.getElementById("reg_email").value,
            password: document.getElementById("reg_password").value
        })
    });

    let data = await res.json();
    alert(data.detail || "Registered successfully");
}

// LOGIN
async function login() {
    let res = await fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: document.getElementById("login_email").value,
            password: document.getElementById("login_password").value
        })
    });

    let data = await res.json();

    if (data.access_token) {
        token = data.access_token;
        alert("Login successful");
    } else {
        alert("Login failed");
    }
}

// CREATE TASK
async function createTask() {
    if (!token) {
        alert("Please login first");
        return;
    }

    await fetch(`${BASE_URL}/tasks?title=${title.value}&description=${desc.value}&token=${token}`, {
        method: "POST"
    });

    alert("Task created");
}

// GET TASKS
async function getTasks() {
    if (!token) {
        alert("Please login first");
        return;
    }

    let res = await fetch(`${BASE_URL}/tasks?token=${token}`);
    let data = await res.json();

    let list = document.getElementById("taskList");
    list.innerHTML = "";

    data.forEach(task => {
        let li = document.createElement("li");

        li.innerText = "ID: " + task.id + " - " + task.title;

        if (task.completed) {
            li.classList.add("completed");
        }

        let btnGroup = document.createElement("div");

        let done = document.createElement("button");
        done.innerText = "Complete";
        done.style.background = "green";
        done.onclick = () => completeTask(task.id);

        let del = document.createElement("button");
        del.innerText = "Delete";
        del.style.background = "red";
        del.onclick = () => deleteTask(task.id);

        btnGroup.appendChild(done);
        btnGroup.appendChild(del);

        li.appendChild(btnGroup);
        list.appendChild(li);
    });
}

// DELETE
async function deleteTask(id) {
    await fetch(`${BASE_URL}/tasks/${id}?token=${token}`, {
        method: "DELETE"
    });
    getTasks();
}

// COMPLETE
async function completeTask(id) {
    await fetch(`${BASE_URL}/tasks/${id}?completed=true&token=${token}`, {
        method: "PUT"
    });
    getTasks();
}


async function getSingleTask() {
    if (!token) {
        alert("Please login first");
        return;
    }

    let id = document.getElementById("task_id_input").value;

    let res = await fetch(`${BASE_URL}/tasks/${id}?token=${token}`);
    let data = await res.json();

    let result = document.getElementById("singleTaskResult");

    if (data.error) {
        result.innerText = "Task not found";
        result.style.color = "red";
    } else {
        result.innerText = data.title + (data.completed ? " ✅ Completed" : " ❌ Not Done");
        result.style.color = "green";
    }
}