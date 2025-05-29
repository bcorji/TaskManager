class AuthService {
    static isAuthenticated() {
        return !!localStorage.getItem('token');
    }

    static logout() {
        localStorage.removeItem('token');
        window.location.href = '/pages/login.html';
    }

    static getToken() {
        return localStorage.getItem('token');
    }

    static checkAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '/pages/login.html';
            return false;
        }
        return true;
    }

    static redirectIfAuthenticated() {
        if (this.isAuthenticated()) {
            window.location.href = '/pages/dashboard.html';
            return true;
        }
        return false;
    }
}
