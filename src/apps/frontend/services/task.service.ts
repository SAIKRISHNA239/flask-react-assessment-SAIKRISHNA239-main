import APIService from 'frontend/services/api.service';

// Define types locally or in types/task.ts
export interface Task {
  id: string;
  account_id: string;
  title: string;
  description: string;
  active: boolean;
}

export interface TaskListResponse {
  items: Task[];
  total_count: number;
  page: number;
  size: number;
}

export default class TaskService extends APIService {
  async getTasks(accountId: string, page = 1, size = 10): Promise<TaskListResponse> {
    const response = await this.apiClient.get<TaskListResponse>(
      `/accounts/${accountId}/tasks`,
      { params: { page, size } }
    );
    return response.data;
  }

  async createTask(accountId: string, data: { title: string; description: string }): Promise<Task> {
    const response = await this.apiClient.post<Task>(
      `/accounts/${accountId}/tasks`,
      data
    );
    return response.data;
  }

  async updateTask(accountId: string, taskId: string, data: { title: string; description: string }): Promise<Task> {
    const response = await this.apiClient.patch<Task>(
      `/accounts/${accountId}/tasks/${taskId}`,
      data
    );
    return response.data;
  }

  async deleteTask(accountId: string, taskId: string): Promise<void> {
    await this.apiClient.delete(`/accounts/${accountId}/tasks/${taskId}`);
  }
}