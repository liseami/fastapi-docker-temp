# 纯想手作版fastapi最小化docker

## 项目简介

本项目是一个基于 FastAPI 的最小化 Docker 项目，用于快速搭建和部署 API 服务。

## 目录

- [纯想手作版fastapi最小化docker](#纯想手作版fastapi最小化docker)
  - [项目简介](#项目简介)
  - [目录](#目录)
  - [技术栈](#技术栈)
  - [开始使用](#开始使用)
    - [前提条件](#前提条件)
    - [安装](#安装)
  - [本地开发](#本地开发)
    - [设置本地数据库](#设置本地数据库)
    - [配置环境变量](#配置环境变量)
    - [启动项目](#启动项目)
  - [数据库迁移](#数据库迁移)
  - [依赖管理](#依赖管理)
  - [API 文档](#api-文档)

## 技术栈

- 数据库映射: [SQLModel](https://sqlmodel.tiangolo.com/)
- 依赖管理: [Poetry](https://python-poetry.org/)
- API 框架: [FastAPI](https://fastapi.tiangolo.com/)
- 数据库迁移: [Alembic](https://alembic.sqlalchemy.org/)

## 开始使用

### 前提条件

- Python 3.10 
- (Docker 镜像已经迁移到国内 registry.cn-hangzhou.aliyuncs.com/mindbook/python:3.10 放心使用)
- Docker 和 Docker Compose
- PostgreSQL

### 安装

1. 克隆仓库：
git clone [仓库URL]
cd [项目目录]

 
在 VS Code 的终端中，您可以通过以下步骤在项目根目录创建虚拟环境：

1. 打开 VS Code 集成终端（快捷键：Ctrl+` 或 View > Terminal）

2. 确保您在项目根目录下，然后执行以下命令创建虚拟环境：

   ```
   python -m venv venv
   ```

   这会在当前目录下创建一个名为 `venv` 的虚拟环境。

3. 激活虚拟环境：

   - Windows:
     ```
     .\venv\Scripts\activate
     ```

   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. 激活后，您会看到终端提示符前面出现 `(venv)`，表示虚拟环境已激活。

5. 现在您可以在这个虚拟环境中安装项目依赖：

   使用 Poetry 安装所有依赖：

   ```
   poetry install
   ```


这些步骤将帮助您在 VS Code 中创建和使用虚拟环境。记得将 `venv` 添加到 `.gitignore` 文件中，以避免将虚拟环境文件提交到版本控制系统。
 
## 本地开发

### 设置本地数据库

使用 Homebrew 启动 PostgreSQL 服务：

   ```
   brew services start postgresql
   ```
 
或使用其他方式启动本地 PostgreSQL 服务。

### 配置环境变量

在项目根目录创建 `.env` 文件，并根据本地环境配置以下变量：
POSTGRES_SERVER=host.docker.internal

POSTGRES_PORT=5432

POSTGRES_USER=your_username

POSTGRES_PASSWORD=your_password

POSTGRES_DB=app
 
### 启动项目

使用 Docker Compose 启动项目：

   ```
   docker compose up -d
   ```

## 数据库迁移

当修改 `models/table.py` 文件后，需要执行以下步骤来更新数据库结构：

1. 进入后端容器：
   
   ```
   docker compose exec backend bash
   ```
 
1. 生成迁移版本：

   ```
   alembic revision --autogenerate -m "描述此次变更"
   ```
 
3. 退出容器，在项目根目录执行：

   ```
   alembic upgrade head
   ```

## 依赖管理

- 添加新依赖：
  
   ```
   poetry add [包名]
   ```
 
- 删除依赖：
  
   ```
   poetry remove [包名]
   ```
 

## API 文档

启动项目后，访问 API 文档：
http://localhost/docs