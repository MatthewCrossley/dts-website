export default function Task({ task }) {
  return (
    <a href={`/task/${task.id}`}>
      <div class="task">
        <h3>{task.title}</h3>
        <p>{task.description}</p>
        <p>Due: {new Date(task.due).toLocaleString()}</p>
      </div>
    </a>
  );
}
