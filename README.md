# 邮书局（YouShuJu）

面向校园场景的二手教材信息发布平台后端。项目使用 FastAPI 构建，目标是让教材信息能够按课程、版本、校区和在售状态被结构化地发布与查询，而不是淹没在校园墙的信息流中。

> 当前处于 MVP 开发阶段。已完成项目基础设施、用户注册、登录和 JWT 签发；教材发布、权限校验、筛选和图片上传仍在开发中。

## 当前已实现

- FastAPI 应用与健康检查接口
- 异步 SQLAlchemy + MySQL 数据库连接
- `User` 与 `BookListing` 一对多 ORM 模型
- 用户注册与用户名唯一性校验
- Argon2 密码哈希存储，不保存明文密码
- 用户登录与 JWT Access Token 签发
- Pydantic 请求/响应模型校验
- `uv` 管理依赖、虚拟环境与锁定版本

## 技术栈

- Python 3.13
- FastAPI + Uvicorn
- Pydantic / pydantic-settings
- SQLAlchemy Async + aiomysql
- MySQL
- pwdlib（Argon2）
- PyJWT
- uv

## 项目结构

```text
you-shu-ju/
├── routers/
│   └── auth.py          # 注册、登录路由
├── config.py            # 从 .env 读取运行配置
├── database.py          # 异步引擎、Session 与数据库依赖
├── main.py              # FastAPI 应用入口与生命周期
├── models.py            # SQLAlchemy ORM 模型
├── schemas.py           # Pydantic 请求/响应模型
├── security.py          # 密码哈希与 JWT 签发
├── pyproject.toml       # 项目依赖声明
└── uv.lock              # 精确依赖版本锁定
```

## 数据模型

```text
User 1 ─── N BookListing
```

- `User`：用户账号、密码哈希、昵称、创建/更新时间
- `BookListing`：教材书名、作者、版次、课程、价格、成色、取书校区、联系方式、图片和在售状态

`seller_id` 是 `BookListing` 关联到 `User` 的外键。后续发布教材时，后端会从当前登录用户的 Token 中获取该字段，不允许客户端自行指定。

## 本地运行

### 1. 前置条件

- Python 3.13
- uv
- 本地 MySQL 服务

创建数据库：

```sql
CREATE DATABASE you_shu_ju
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件。该文件包含密钥，已被 Git 忽略，不能提交。

```env
DATABASE_URL=mysql+aiomysql://用户名:密码@127.0.0.1:3306/you_shu_ju?charset=utf8mb4
JWT_SECRET_KEY=请替换为随机长字符串
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 3. 安装依赖并启动

```bash
uv sync
uv run fastapi dev main.py --port 8002
```

启动后访问：

- Swagger 文档：`http://127.0.0.1:8002/docs`
- 健康检查：`http://127.0.0.1:8002/health`

应用启动时会检查并创建尚不存在的 `users`、`book_listings` 表。

## 当前接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/health` | 健康检查 |
| POST | `/api/v1/auth/register` | 用户注册 |
| POST | `/api/v1/auth/login` | 用户登录并获取 JWT Token |

注册请求示例：

```json
{
  "username": "chen_01",
  "password": "123456",
  "nickname": "书虫小陈"
}
```

## 后续计划

- JWT Token 验证与 `get_current_user` 依赖
- 教材发布、列表、详情、修改、删除
- 资源归属校验：只能修改和删除自己的教材帖
- 关键词、课程、校区、价格、状态筛选与分页
- 单图上传与文件校验
- pytest 接口测试与 Alembic 数据库迁移
- Docker Compose、Redis 缓存和 Linux 部署
- 教材封面 OCR / 多模态信息提取等 AI 扩展

## 安全说明

- 不提交 `.env`、`.venv/`、`.idea/` 和用户上传文件
- 密码仅保存 Argon2 哈希值
- JWT 密钥只保存在本地或部署环境的环境变量中
