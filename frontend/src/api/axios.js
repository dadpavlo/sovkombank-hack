import axios from 'axios';
const BASE_URL = 'http://192.168.0.8:8081/';

export default axios.create({
  baseURL: BASE_URL,
  withCredentials: true
});

export const axiosPrivate = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
});