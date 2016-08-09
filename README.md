# WebTemplate
a web site template built with Django + Mysql

# 开发步骤
## 安装Django
下载Django-1.10，解压在任何目录，在该目录下运行`python setup.py install`
## 安装Mysql
1. 并新建用户test，密码test 
```mysql
insert into mysql.user(Host,User,Password) values("localhost","test",password("test"));
flush privileges;
```
2. 新建数据库test。
```mysql
create database test;
grant all privileges on test.* to test@localhost identified by 'test';
flush privileges;
```
3. 切换到test.
```mysql
 #退出mysql命令行
 mysql -utest -ptest
 use test;
```
## 生成站点目录
```python
django-admin startproject webapp
```
## 修改站点设置（setting.py）
```
# 使用Mysql数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
# 使用中文,该版本的zh-cn已经被zh-hans取代，具体见Django安装目录下的contrib/humanize/local文件夹，里面有所有支持的语言
LANGUAGE_CODE = 'zh-hans'
# 使用上海时区
TIME_ZONE = 'Asia/Shanghai'
```
## 启动服务
```python
# 有文件新增需要重启
python manage.py runserver
```
## 创建app(一个站点可以有多个app，一个app也可以属于多个站点)
```python
python manage.py startapp polls
```
运行后的目录结构如下：
polls/
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
## 写第一个view
 ```python
 # polls/views.py
 from django.http import HttpResponse
 
 def index(request):
     return HttpResponse("Hello, world. You're at the polls index.")
 ```

## 移植数据库及已安装的模块
运行`python manage.py migrate`将会安装`settings.py`下的`INSTALLED_APPS`中的模块，还会在数据库中新建相关的表。
mysql> show tables;
+----------------------------+
| Tables_in_test             |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
+----------------------------+
## 写第一个model
以下代码定义了一个Question表，表中有两个字段：问题及发布日期；一个选项Choice表，该表有三个字段：与Question相关的外键、选项描述及选票数。`CharField`等定义了数据类型
 ```python
 # polls/models.py
 from django.db import models
 
 class Question(models.Model):
     question_text = models.CharField(max_length=200)
     pub_date = models.DateTimeField('date published')
 
 class Choice(models.Model):
     question = models.ForeignKey(Question, on_delete=models.CASCADE)
     choice_text = models.CharField(max_length=200)
     votes = models.IntegerField(default=0)
 ```

## 在webapp中安装polls
1. 在setting.py文件中的`INSTALLED_APPS`中添加`'polls.apps.PollsConfig'`
2. 运行命令`python manage.py makemigrations polls`更新model,输出如下信息：
 Migrations for 'polls':
   polls/migrations/0001_initial.py:
     - Create model Choice
     - Create model Question
     - Add field question to choice
3. 将更新同步到数据库中：`python manage.py sqlmigrate polls 0001`，输出如下信息：
```mysql
BEGIN;
--
-- Create model Choice
--
CREATE TABLE `polls_choice` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `choice_text` varchar(200) NOT NULL, `votes` integer NOT NULL);
--
-- Create model Question
--
CREATE TABLE `polls_question` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `question_text` varchar(200) NOT NULL, `pub_date` datetime(6) NOT NULL);
--
-- Add field question to choice
--
ALTER TABLE `polls_choice` ADD COLUMN `question_id` integer NOT NULL;
ALTER TABLE `polls_choice` ALTER COLUMN `question_id` DROP DEFAULT;
CREATE INDEX `polls_choice_7aa0f6ee` ON `polls_choice` (`question_id`);
ALTER TABLE `polls_choice` ADD CONSTRAINT `polls_choice_question_id_c5b4b260_fk_polls_question_id` FOREIGN KEY (`question_id`) REFERENCES `polls_question` (`id`);
COMMIT;
```

使用命令`python manage.py migrate`即可在数据库中创建表，同步这些信息。

## 尝试Django API
运行`python manage.py shell`,交互模式探索Django API的使用方法

## 使用后台管理
1. 创建超级用户
 运行`python manage.py createsuperuser`，输入用户名，邮箱及密码（用户名test,密码1TeSt23!，邮箱：starqiu@qq.com）
2. 启动服务并登陆
 启动服务`python manage.py runserver`,在浏览器中访问localhost:8000/admin,此时只能对用户及用户组做操作，还不能对我们刚刚新建的model做操作
3. 后台管理自定义的model
 * 在`polls/admin.py`中注册需要被管理的model
 ```python
 #polls/admin.py
 from django.contrib import admin
 
 from .models import Question
 
 admin.site.register(Question)
 ```
 
## 更丰富的视图及模板
1. 创建视图
  ```python
  #polls/views.py
  from django.http import HttpResponse
  from django.template import loader
  from .models import Question
  
  def index(request):
      latest_question_list = Question.objects.order_by('-pub_date')[:5]
      template = loader.get_template('polls/index.html')
      context = {'latest_question_list': latest_question_list}
      return HttpResponse(template.render(context, request))
  ```
  
  此处我们导入了一个模板`polls/index.html`（下一步创建），指定模板使用一个上下文（字典）和request来渲染
  
 2. 新建模板。在app目录（polls）新建`templates/polls`目录（两级），再新建一个模板文件index.html
```python
 {% if lastest_question_list %}
    <ul>
        {% for question in latest_question_list %}
            <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
        {% endfor %}
    </ul>
 {% else %}
    <p>No polls are available.</p>
 {% endif %}
```
3. 访问页面
 启动服务后即可访问页面
