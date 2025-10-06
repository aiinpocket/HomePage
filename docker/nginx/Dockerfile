FROM nginx:alpine

# 複製前端靜態文件
WORKDIR /usr/share/nginx/html
COPY frontend/ /usr/share/nginx/html/

# 複製 Nginx 配置
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 啟動 Nginx
CMD ["nginx", "-g", "daemon off;"]
