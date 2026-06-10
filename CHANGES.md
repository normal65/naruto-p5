# 数据库迁移改动说明

## 概述

将项目从JSON文件存储迁移到MySQL数据库，使用Flask-SQLAlchemy作为ORM。

## 新增文件

### 1. `backend/models.py`
数据库模型定义文件，包含三个模型：

- **Character**: 角色模型
  - id, name, name_en, role, image, summary, tags(JSON), quotes

- **Event**: 剧情事件模型
  - id, title, period, summary

- **EventChild**: 子事件模型
  - id, event_id(外键), title, detail

### 2. `backend/migrate_data.py`
数据迁移脚本，将JSON数据导入MySQL。

### 3. `backend/test_db.py`
数据库连接测试脚本。

### 4. `backend/requirements.txt`
Python依赖包列表。

### 5. `README.md`
项目说明文档。

### 6. `SETUP.md`
数据库迁移设置指南。

## 修改文件

### `backend/app.py`

主要改动：

1. **导入数据库模块**
   ```python
   from models import db, Character, Event, EventChild
   ```

2. **添加MySQL配置**
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://normal:4152630@localhost:3306/game'
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   ```

3. **初始化数据库**
   ```python
   db.init_app(app)
   ```

4. **修改API接口**
   - `get_events()`: 从读取JSON改为查询数据库
   - `get_characters()`: 从读取JSON改为查询数据库
   - `add_character()`: 从写入JSON改为插入数据库
   - `delete_character()`: 从修改JSON改为删除数据库记录

5. **启动时创建表**
   ```python
   with app.app_context():
       db.create_all()
   ```

## 数据库配置

- **用户名**: normal
- **密码**: 4152630
- **主机**: localhost
- **端口**: 3306
- **数据库**: game

## 使用步骤

1. 创建MySQL数据库 `game`
2. 安装依赖: `pip install -r requirements.txt`
3. 测试连接: `python test_db.py`
4. 迁移数据: `python migrate_data.py`
5. 启动应用: `python app.py`

## 优势

1. **数据持久化**: 数据存储在MySQL中，更可靠
2. **查询性能**: 支持索引和复杂查询
3. **并发支持**: 支持多用户同时访问
4. **数据完整性**: 支持事务和外键约束
5. **易于扩展**: 可以方便地添加新功能

## 注意事项

1. 确保MySQL服务已启动
2. 确保normal用户有game数据库的访问权限
3. 首次运行会自动创建表结构
4. JSON文件仍保留作为备份
