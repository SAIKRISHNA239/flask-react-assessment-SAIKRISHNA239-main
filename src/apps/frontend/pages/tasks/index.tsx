import React, { useEffect, useState, useMemo } from 'react';
import toast from 'react-hot-toast';
import { useAccountContext } from 'frontend/contexts';
import TaskService, { Task } from 'frontend/services/task.service';
import Button from 'frontend/components/button';

// Simple Modal Component for Add/Edit
const TaskModal = ({ isOpen, onClose, onSubmit, initialData }: any) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title);
      setDescription(initialData.description);
    } else {
      setTitle('');
      setDescription('');
    }
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="w-full max-w-md rounded bg-white p-6 shadow-lg dark:bg-boxdark">
        <h2 className="mb-4 text-xl font-bold">{initialData ? 'Edit Task' : 'Create Task'}</h2>
        <div className="mb-4">
          <label className="mb-2 block text-sm font-bold">Title</label>
          <input
            className="w-full rounded border p-2 dark:bg-form-input"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label className="mb-2 block text-sm font-bold">Description</label>
          <textarea
            className="w-full rounded border p-2 dark:bg-form-input"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <div className="flex justify-end gap-2">
          {/* FIX 1: Removed invalid 'variant' prop */}
          <Button onClick={onClose}>Cancel</Button>
          <Button onClick={() => onSubmit({ title, description })}>Save</Button>
        </div>
      </div>
    </div>
  );
};

const TasksPage: React.FC = () => {
  // FIX 2: Cast context to 'any' to bypass missing 'account' type definition
  const { account } = useAccountContext() as any; 
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const taskService = useMemo(() => new TaskService(), []);

  const fetchTasks = async () => {
    if (!account) return;
    try {
      const data = await taskService.getTasks(account.id);
      setTasks(data.items);
    } catch (err: any) {
      toast.error('Failed to load tasks');
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [account]);

  const handleCreate = async (data: { title: string; description: string }) => {
    if (!account) return;
    try {
      await taskService.createTask(account.id, data);
      toast.success('Task created');
      setIsModalOpen(false);
      fetchTasks();
    } catch (err) {
      toast.error('Failed to create task');
    }
  };

  const handleUpdate = async (data: { title: string; description: string }) => {
    if (!account || !editingTask) return;
    try {
      await taskService.updateTask(account.id, editingTask.id, data);
      toast.success('Task updated');
      setIsModalOpen(false);
      setEditingTask(null);
      fetchTasks();
    } catch (err) {
      toast.error('Failed to update task');
    }
  };

  const handleDelete = async (taskId: string) => {
    if (!account) return;
    if (!window.confirm('Are you sure?')) return;
    try {
      await taskService.deleteTask(account.id, taskId);
      toast.success('Task deleted');
      fetchTasks();
    } catch (err) {
      toast.error('Failed to delete task');
    }
  };

  const openCreateModal = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const openEditModal = (task: Task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Tasks</h1>
        <Button onClick={openCreateModal}>+ Create Task</Button>
      </div>

      <div className="flex flex-col gap-4">
        {tasks.map((task) => (
          <div key={task.id} className="rounded border bg-white p-4 shadow dark:bg-boxdark dark:border-strokedark">
            <div className="flex justify-between">
              <h3 className="text-lg font-semibold">{task.title}</h3>
              <div className="flex gap-2">
                <button onClick={() => openEditModal(task)} className="text-primary hover:underline">Edit</button>
                <button onClick={() => handleDelete(task.id)} className="text-danger hover:underline">Delete</button>
              </div>
            </div>
            <p className="mt-2 text-gray-600 dark:text-gray-300">{task.description}</p>
          </div>
        ))}
        {tasks.length === 0 && <p>No tasks found.</p>}
      </div>

      <TaskModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={editingTask ? handleUpdate : handleCreate}
        initialData={editingTask}
      />
    </div>
  );
};

export default TasksPage;