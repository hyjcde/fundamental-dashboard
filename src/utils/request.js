import axios from "axios";
import { Message } from "element-ui";

// 创建axios实例
const service = axios.create({
  baseURL: "http://localhost:5000", // api的base_url
  timeout: 15000, // 请求超时时间
});

// response拦截器
service.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    Message({
      message: error.message,
      type: "error",
      duration: 5 * 1000,
    });
    return Promise.reject(error);
  }
);

export default service;
