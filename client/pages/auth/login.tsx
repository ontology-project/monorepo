import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

interface Credentials {
  username: string;
  password: string;
}

export default function Login() {
  const [credentials, setCredentials] = useState<Credentials>({ username: '', password: '' });
  const router = useRouter();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/auth/jwt/create/', credentials);
      localStorage.setItem('authToken', response.data.access);
      router.push('/');
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed!');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Username:</label>
        <input type="text" name="username" value={credentials.username} onChange={handleChange} />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" name="password" value={credentials.password} onChange={handleChange} />
      </div>
      <button type="submit">Login</button>
    </form>
  );
}
