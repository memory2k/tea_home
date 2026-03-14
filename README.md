# 茶录

一个前后端分离的茶资料站：

- `frontend/`：Vue 3 + Vite 前端
- `backend/`：Django + Django Admin + REST API

## 目录结构

```text
tea/
├── frontend/   # Vue 前端
├── backend/    # Django 后端
└── data/       # 预留本地资料目录
```

## 环境要求

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+

## 后端启动

```bash
cd backend
python3 -m venv .tea_env
source .tea_env/bin/activate
pip3 install -r requirements.txt
```

复制环境变量模板：

```bash
cp .env.example .env
```

根据你的 PostgreSQL 实例修改 `.env` 中的这些变量：

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

执行迁移：

```bash
python3 manage.py migrate
```

创建后台管理员：

```bash
python3 manage.py createsuperuser
```

导入初始数据：

```bash
python3 manage.py import_tea_library
```

启动 Django：

```bash
python3 manage.py runserver
```

后台地址：

- [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端地址：

- [http://127.0.0.1:5173](http://127.0.0.1:5173)

## 测试与检查

后端检查：

```bash
cd backend
python3 manage.py check
DJANGO_USE_SQLITE_FOR_TESTS=1 python3 manage.py test
```

前端构建：

```bash
cd frontend
npm run build
```
