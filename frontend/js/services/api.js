const API_URL = 'http://localhost:8000';

class ApiService {
    static async login(email, password) {
        const response = await fetch(`${API_URL}/users/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: email,
                password: password,
            }),
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        return data;
    }

    static async register(email, password, fullName) {
        const response = await fetch(`${API_URL}/users/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password,
                full_name: fullName
            }),
        });

        if (!response.ok) {
            throw new Error('Registration failed');
        }

        return response.json();
    }    static async getProjects() {
        const response = await this._authenticatedRequest('/projects');
        return response.json();
    }

    static async getProjectById(id) {
        const response = await this._authenticatedRequest(`/projects/${id}`);
        return response.json();
    }

    static async createProject(title, description) {
        const response = await this._authenticatedRequest('/projects', {
            method: 'POST',
            body: JSON.stringify({ title, description }),
        });
        return response.json();
    }

    static async deleteProject(id) {
        await this._authenticatedRequest(`/projects/${id}`, {
            method: 'DELETE',
        });
    }

    static async getTasks(filters = {}) {
        const queryParams = new URLSearchParams(filters).toString();
        const response = await this._authenticatedRequest(`/tasks?${queryParams}`);
        return response.json();
    }

    static async createTask(taskData) {
        const response = await this._authenticatedRequest('/tasks', {
            method: 'POST',
            body: JSON.stringify(taskData),
        });
        return response.json();
    }

    static async updateTask(taskId, taskData) {
        const response = await this._authenticatedRequest(`/tasks/${taskId}`, {
            method: 'PUT',
            body: JSON.stringify(taskData),
        });
        return response.json();
    }

    static async getCategories() {
        const response = await this._authenticatedRequest('/categories');
        return response.json();
    }

    static async _authenticatedRequest(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                ...options.headers,
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/pages/login.html';
            throw new Error('Authentication failed');
        }

        if (!response.ok) {
            throw new Error('Request failed');
        }

        return response;
    }
}
