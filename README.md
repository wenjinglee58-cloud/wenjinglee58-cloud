# iOS设备后台管理系统

这是一个基于Django的Web应用程序，用于管理和监控iOS设备的后台活动，包括电池状态、后台应用刷新、后台活动限制等功能。

## 功能特性

- **设备监控**：实时查看设备电池电量、内存使用率、存储空间、网络状态
- **后台应用刷新管理**：批量启用/禁用设备的后台应用刷新功能
- **后台活动限制**：限制设备在后台的网络请求和定位服务
- **策略管理**：创建和管理设备策略，如省电模式、网络限制等
- **MDM配置生成**：生成基本的移动设备管理配置文件
- **用户认证**：完整的用户注册、登录、权限管理系统
- **响应式界面**：基于Bootstrap 5的现代化仪表板

## 技术栈

- **后端**：Django 6.0.2 + SQLite
- **前端**：Bootstrap 5 + Font Awesome
- **模板引擎**：Django Templates
- **认证系统**：Django内置认证

## 安装与运行

### 前提条件
- Python 3.8+
- pip包管理器

### 步骤

1. 克隆或下载项目代码
2. 进入项目目录
3. 创建并激活虚拟环境：
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
4. 安装依赖：
   ```bash
   pip install django
   ```
5. 运行数据库迁移：
   ```bash
   python manage.py migrate
   ```
6. 创建超级用户：
   ```bash
   python manage.py createsuperuser
   ```
7. 生成模拟数据（可选）：
   ```bash
   python manage.py seed_devices --count 10 --user admin
   python manage.py seed_policies --count 5
   ```
8. 启动开发服务器：
   ```bash
   python manage.py runserver
   ```
9. 在浏览器中访问：http://127.0.0.1:8000/

## 使用说明

### 初始登录
- 使用创建的超级用户账号登录
- 或注册新用户账户

### 主要功能页面

1. **仪表板** (`/dashboard/`)
   - 设备概览统计
   - 最近设备状态
   - 活跃策略列表

2. **设备管理** (`/devices/`)
   - 查看所有设备
   - 设备详细信息
   - 快速操作按钮

3. **后台刷新管理** (`/devices/background-refresh-management/`)
   - 批量启用/禁用后台应用刷新
   - 单个设备状态切换
   - 实时状态更新

4. **后台活动限制** (`/devices/background-activity-management/`)
   - 限制设备后台活动
   - 批量操作功能

5. **策略管理** (`/policies/`)
   - 查看和管理设备策略
   - 策略类型说明

6. **MDM配置下载** (`/devices/generate-mdm-profile/`)
   - 下载.mobileconfig配置文件
   - 基础MDM配置

7. **后台管理** (`/admin/`)
   - Django管理后台
   - 完整的数据管理功能

### 模拟数据
项目包含管理命令用于生成测试数据：
- `seed_devices`：创建设备模拟数据
- `seed_policies`：创建策略模拟数据

## 项目结构

```
ios_control/
├── devices/              # 设备管理应用
│   ├── management/commands/
│   │   └── seed_devices.py
│   ├── models.py        # 设备模型
│   ├── views.py         # 设备相关视图
│   ├── urls.py          # 设备URL配置
│   └── templates/devices/ # 设备相关模板
├── dashboard/           # 仪表板应用
│   ├── views.py         # 主视图
│   ├── urls.py          # 仪表板URL
│   └── templates/       # 主模板
├── policies/            # 策略管理应用
│   ├── management/commands/
│   │   └── seed_policies.py
│   └── models.py        # 策略模型
├── ios_control/         # 项目配置
│   ├── settings.py      # 项目设置
│   ├── urls.py          # 根URL配置
│   └── wsgi.py
├── manage.py
├── db.sqlite3           # 数据库文件（运行后生成）
└── README.md
```

## 重要注意事项

1. **生产环境**：此项目为演示版本，不适合直接用于生产环境
2. **安全性**：生产环境需要配置HTTPS、强化数据库、设置安全头等
3. **MDM集成**：当前MDM配置为示例，真实MDM需要苹果企业开发者账号和服务器配置
4. **设备通信**：实际设备控制需要通过苹果MDM协议或设备注册实现
5. **数据模拟**：设备状态数据为模拟生成，真实系统需要设备端代理

## 开发与扩展

### 添加新功能
1. 创建新的Django应用：`python manage.py startapp app_name`
2. 在`settings.py`的`INSTALLED_APPS`中添加应用
3. 设计模型、视图、URL和模板
4. 运行迁移命令更新数据库

### 集成真实MDM
1. 获取苹果企业开发者账号
2. 配置APNs证书和MDM服务器
3. 实现完整的MDM协议
4. 集成设备注册和命令队列

### 样式自定义
- 修改`dashboard/templates/dashboard/base.html`中的CSS
- 使用自定义静态文件替换Bootstrap CDN
- 添加JavaScript交互功能

## 故障排除

### 常见问题

1. **端口占用**：更改运行端口 `python manage.py runserver 8080`
2. **数据库错误**：删除`db.sqlite3`并重新运行迁移
3. **静态文件404**：运行 `python manage.py collectstatic`
4. **模板未找到**：检查`TEMPLATES`设置中的`APP_DIRS`是否为`True`

### 获取帮助
- 查看Django官方文档：https://docs.djangoproject.com/
- 检查终端错误输出
- 使用Django调试工具

## 许可证

本项目仅供学习和演示使用。实际部署需要遵守相关法律法规和苹果开发者协议。

---

**注意**：此系统为概念验证，实际iOS设备管理需要苹果官方MDM解决方案和相应的开发者授权。