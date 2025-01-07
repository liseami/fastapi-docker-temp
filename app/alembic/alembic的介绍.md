# Alembic 和 PostgreSQL 开发指南

## PostgreSQL 本地开发环境设置

### 使用 Homebrew 安装和管理 PostgreSQL

1. 安装 PostgreSQL
```bash
brew install postgresql@14
```

2. 启动 PostgreSQL 服务
```bash
brew services start postgresql@14
```

3. 验证 PostgreSQL 服务状态
```bash
brew services list
```

4. 创建数据库（示例）
```bash
createdb your_database_name
```

5. 停止 PostgreSQL 服务
```bash
brew services stop postgresql@14
```

### PostgreSQL 常用命令

- 进入 PostgreSQL 命令行：`psql`
- 列出所有数据库：`\l`
- 连接到特定数据库：`\c database_name`
- 列出当前数据库的所有表：`\dt`
- 查看表结构：`\d table_name`

## Alembic 数据库迁移工具

### 什么是 Alembic？

Alembic 是 SQLAlchemy 作者开发的数据库迁移工具，它可以：
- 追踪数据库模式变更
- 提供数据库版本控制
- 支持升级和降级操作
- 自动生成迁移脚本

### Alembic 项目结构

```
alembic/
├── env.py           # 主要配置文件
├── README          # 说明文件
├── script.py.mako  # 迁移脚本模板
└── versions/       # 存放迁移脚本的目录
```

### Alembic 常用命令

1. 初始化 Alembic
```bash
alembic init alembic
```

2. 创建新的迁移
```bash
alembic revision --autogenerate -m "描述信息"
```

3. 升级到最新版本
```bash
alembic upgrade head
```

4. 降级到上一个版本
```bash
alembic downgrade -1
```

5. 查看当前版本
```bash
alembic current
```

6. 查看迁移历史
```bash
alembic history
```

7. 升级到指定版本
```bash
alembic upgrade <revision_id>
```

8. 降级到指定版本
```bash
alembic downgrade <revision_id>
```

### 最佳实践

1. **命名规范**
   - 使用有意义的迁移描述
   - 遵循一致的命名约定

2. **版本控制**
   - 将迁移脚本纳入版本控制
   - 不要修改已提交的迁移脚本

3. **测试**
   - 在应用迁移前先在测试环境验证
   - 确保 upgrade 和 downgrade 都能正常工作

4. **备份**
   - 在执行重要迁移前备份数据库
   - 保持定期备份习惯

## 常见问题解决

1. **数据库连接问题**
   - 检查数据库服务是否运行
   - 验证连接字符串是否正确
   - 确认用户权限

2. **迁移冲突**
   - 确保团队成员同步迁移历史
   - 解决合并冲突时需谨慎

3. **性能考虑**
   - 大型迁移考虑分批执行
   - 避免在高峰期执行迁移

## 环境变量配置

在本地开发中，需要设置以下环境变量：

```bash
export POSTGRES_USER="your_username"
export POSTGRES_PASSWORD="your_password"
export POSTGRES_DB="your_database"
export POSTGRES_PORT="5432"
```

## 参考资料

- [Alembic 官方文档](https://alembic.sqlalchemy.org/)
- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/) 