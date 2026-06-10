# 数据库迁移设置指南

## 前置条件

1. 已安装MySQL数据库
2. 已创建用户名为 `normal`，密码为 `3306` 的MySQL用户
3. 已安装Python和pip

## 步骤一：创建数据库

登录MySQL并创建数据库：

```bash
mysql -u normal -p
```

输入密码 `4152630` 后执行：

```sql
CREATE DATABASE game CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

## 步骤二：安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

## 步骤三：测试数据库连接

```bash
cd backend
python test_db.py
```

如果显示"数据库连接成功"，则继续下一步。

## 步骤四：迁移数据

```bash
cd backend
python migrate_data.py
```

这将：
1. 创建数据库表（characters, events, event_children）
2. 将JSON数据导入MySQL

## 步骤五：启动应用

```bash
cd backend
python app.py
```

访问 http://localhost:5000 查看应用。

## 验证数据

登录MySQL查看数据：

```bash
mysql -u normal -p game
```

```sql
SELECT * FROM characters;
SELECT * FROM events;
SELECT * FROM event_children;
```

## 故障排除

### 连接失败

如果遇到连接错误，检查：
1. MySQL服务是否启动
2. 用户名密码是否正确
3. 数据库game是否已创建

### 权限问题

如果normal用户没有权限，使用root用户授权：

```sql
GRANT ALL PRIVILEGES ON game.* TO 'normal'@'localhost';
FLUSH PRIVILEGES;
```

### 字符编码问题

确保MySQL配置文件（my.ini或my.cnf）包含：

```ini
[mysqld]
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
```
