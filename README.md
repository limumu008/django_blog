1. 概述
    1. 包括博客、商城 demo、以及在线学习平台三个展示用项目。
    2. 主要使用 django、部分 django 第三方插件开发，使用 jquery 完成 ajax。
2. 准备
    1. 安装 pipenv

            pip install pipenv
    2. ```git clone git@github.com:StevenLianaL/django_blog.git```
    3. 创建虚拟环境并安装依赖：

           pipenv install
    4. 配置 settings.py
        1.配置数据库：简单起见，可修改为默认的 SQLite。
        2.配置邮箱：将邮箱改为自己的邮箱即可。
    5. migrate
    
            python manage.py makemigrations
            python manage.py migrate
    6. 静态文件
    
            python manage.py collectstatic
    7. 安装 Redis
    
            pip install reids 
3. 部署
    1. nginx
        1. 安装
            
                sudo apt-get install nginx
        2. 配置(/etc/nginx/sites-available/your-conf-name)

                server {
                    listen:80;
                    
                    server_name:your domain;
                    location / static {
                        alias /home/steven/sites/django.qinglanjun.com/django_blog/staticfiles; # your Django project's static files
                        
                    location /media {
                        alias /home/steven/sites/django.qinglanjun.com/django_blog/media;
                        
                    location / {
                        proxy_set_header Host $host;
                        proxy_pass http://unix:/tmp/www.qinglanjun.com.socket;
                }
        3. 创建链接
            
                sudo ln -s /etc/nginx/sites-available/your-conf-name /etc/nginx/sites-enabled/your-conf-name
        4. 启动
            
                sudo service nginx start
    2. gunicorn
        
            gunicorn --bind unix:/tmp/www.qinglanjun.com.socket django_blog.wsgi:application&
    3. celery
        
            celery -A django_blog worker  -l info
        
