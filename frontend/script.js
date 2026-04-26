const tasksList = document.getElementById('tasks');
const newTaskInput = document.getElementById('new-task');
const addTaskButton = document.getElementById('add-task');

async function fetchTasks() {
  const response = await fetch('/tasks');
  const tasks = await response.json();
  renderTasks(tasks);
}

function renderTasks(tasks) {
  tasksList.innerHTML = '';

  if (!tasks.length) {
    const message = document.createElement('li');
    message.className = 'empty-state';
    message.textContent = 'No tasks yet. Add one to get started.';
    tasksList.appendChild(message);
    return;
  }

  tasks.forEach(task => {
    const item = document.createElement('li');
    item.className = 'task-item';

    const label = document.createElement('span');
    label.textContent = task.text;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.addEventListener('click', () => removeTask(task.id));

    item.append(label, deleteButton);
    tasksList.appendChild(item);
  });
}

async function addTask() {
  const text = newTaskInput.value.trim();
  if (!text) {
    return;
  }

  await fetch('/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });

  newTaskInput.value = '';
  fetchTasks();
}

async function removeTask(id) {
  await fetch(`/tasks/${id}`, { method: 'DELETE' });
  fetchTasks();
}

addTaskButton.addEventListener('click', addTask);
newTaskInput.addEventListener('keypress', event => {
  if (event.key === 'Enter') {
    addTask();
  }
});

fetchTasks();
