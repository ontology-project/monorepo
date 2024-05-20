import axios from 'axios';
import { BASE_URL } from './constants';

const instance = axios.create({
  baseURL: BASE_URL,
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

export const imageApiPost = async (path: string, data: any) => {
  try {
    let formData = new FormData();
    formData.append('file', data);
    console.log(formData);
    const response = await instance.post(path, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(`Error: ${error.response.data.error}`);
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
};

export const apiGet = async (path: string, params: any = {}) => {
  try {
    const response = await instance.get(path, { params });
    console.log('resss', response.data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(`Error: ${error.response.data.error}`);
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
};
