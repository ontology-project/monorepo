import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000/',
});

export const apiPost = async (path: string, data: any) => {
  try {
    const response = await instance.post(path, data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(`Error: ${error.response.data.error}`);
    } else {
      throw new Error('An unexpected error occurred.'); 
    }
  }
};

