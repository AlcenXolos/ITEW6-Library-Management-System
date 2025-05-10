import axios from 'axios';

const API = 'http://localhost:8000';

export function signupBorrower(data) {
  // POST /signup/ with {username,email,password,first_name,last_name}
  return axios.post(`${API}/signup/`, data).then(r => r.data);
}

export function login({ username, password }) {
  // POST /login/ with {username,password}
  return axios.post(`${API}/login/`, { username, password }).then(r => r.data);
}
