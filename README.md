# 火影忍者P5风格图鉴

一个前后端分离的Web应用，展示火影忍者角色和剧情信息。

## 技术栈

- **后端**: Python Flask + SQLAlchemy
- **前端**: Vue 3 + Vite
- **数据库**: MySQL

## 数据库配置

数据库连接配置在 `backend/app.py` 中：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://normal:4152630@localhost:3306/game'
```

- 用户名: normal
- 密码: 4152630
- 主机: localhost
- 端口: 3306
- 数据库: game

## 安装步骤

### 1. 创建MySQL数据库

```sql
CREATE DATABASE game CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 迁移数据（从JSON到MySQL）

```bash
cd backend
python migrate_data.py
```

### 4. 启动后端服务

```bash
cd backend
python app.py
```

后端将在 http://localhost:5000 启动

### 5. 安装前端依赖并构建

```bash
cd frontend
npm install
npm run build
```

## API接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/characters | 获取所有角色 |
| POST | /api/characters | 添加新角色 |
| DELETE | /api/characters/:id | 删除角色 |
| GET | /api/events | 获取所有剧情事件 |

## 数据库表结构

### characters 表
- id: 角色ID (主键)
- name: 角色名称
- name_en: 英文名称
- role: 角色身份
- image: 头像图片路径
- summary: 角色简介
- tags: 标签 (JSON格式)
- quotes: 经典台词

### events 表
- id: 事件ID (主键)
- title: 篇章标题
- period: 时期
- summary: 篇章简介

### event_children 表
- id: 子事件ID (主键)
- event_id: 关联的事件ID (外键)
- title: 子事件标题
- detail: 详细描述

## 访问应用

启动后端服务后，访问 http://localhost:5000 即可查看应用。
