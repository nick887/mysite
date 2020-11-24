# Nginx+uwsgi+Django部署全过程

1. Django项目中setting.py文件在ALLOWED_HOSTS加一个‘\*’
2. 安装uwsgi 
pip3 install uwsgi
3. 将uwsgi_params拷贝到项目目录下
该文件一般在/etc/nginx/下
4. 改变权限 sudo chmod 664 /root/mysite/uwsgi_params
5. 安装nginx
6. 在/ etc / nginx / sites-available /中创建mysite_nginx.conf的文件
文件样式
```
# mysite_nginx.conf

# the upstream component nginx needs to connect to
upstream django {
    server unix:///root/mysite/mysite/mysite.sock; # for a file socket
    #server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      8000;
    # the domain name it will serve for
    server_name 47.116.139.54; # substitute your machine's IP address or FQDN
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /root/mysite/mysite/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /root/mysite/mysite/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /root/mysite/mysite/uwsgi_params; # the uwsgi_params file you installed
    }
}
```

7. 从/ etc / nginx / sites-enabled到此文件的符号链接，以便nginx可以看到它：
sudo ln -s /etc/nginx/sites-available/mysite_nginx.conf /etc/nginx/sites-enabled/
8. 编辑mysite / settings.py并添加STATIC_ROOT = os.path.join(BASE_DIR, "static/")
9. 运行python manage.py collectstatic
10. 改变权限设置 vim /etc/nginx/nginx.conf把 user 用户名 改为 user root 或 其它有高权限的用户名称即可
11. 重启nginx
先进行检测，看之前的配置文件有无错误。
sudo /usr/sbin/nginx -t

重新加载nginx让软链接的luffy_nginx.conf生效。
sudo /usr/sbin/nginx -s reload

访问```http://luffy.tielemao.com:8000/media/princekin_fox.jpg```看能否正常访问到图片资源

12. 在项目目录中写入uwsgi_mysite.ini
```# mysite_uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /root/mysite/mysite
# Django's wsgi file
module          = mysite.wsgi


# the virtualenv (full path)
home            = /root/mysite/mysite/mysite/ll_env

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 10
# the socket (use the full path to be safe
socket          = /root/mysite/mysite/mysite.sock
# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true
```


13. 使用该文件运行uwsgi```uwsgi --ini mysite_uwsgi.ini```