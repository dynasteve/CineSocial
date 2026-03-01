This is a professionally formatted, comprehensive GitHub `README.md` for the **CineSocial Backend API**. It includes functional anchors for the Table of Contents, syntax-highlighted code blocks, and organized tables for API references.

```markdown
# CineSocial Backend API

CineSocial is a headless social platform designed for movie lovers. It provides a JSON REST API built with **Django REST Framework (DRF)**, secured with **JWT** authentication, and integrated with **TMDB** for film data and **NewsAPI** for entertainment headlines.

---

## 🛠 Technical Overview

| Feature | Specification |
| :--- | :--- |
| **Framework** | Django 5.2 + Django REST Framework |
| **Authentication** | JWT (SimpleJWT) — Access (15m) / Refresh (7d) |
| **Database** | SQLite (Dev) / Compatible with PostgreSQL (Prod) |
| **Cache** | In-memory (LocMemCache) |
| **Pagination** | Page-number pagination, 20 items per page |
| **Throttling** | Anon: 50 req/day · Auth: 1,000 req/day |
| **CORS** | Development: `CORS_ALLOW_ALL_ORIGINS = True` |

---

## 📋 Table of Contents
1. [Getting Started](#getting-started)
2. [Environment Variables](#environment-variables)
3. [Authentication](#authentication)
4. [Users & Profiles](#users--profiles)
5. [Social Feed](#social-feed)
6. [Movies](#movies)
7. [Messaging](#messaging)
8. [News](#news)
9. [Full Endpoint Summary](#full-endpoint-summary)
10. [Error Responses](#error-responses)
11. [Roadmap & Limitations](#roadmap--limitations)

---

## 🚀 Getting Started

### Requirements
* Python 3.10+
* [TMDB API Key](https://www.themoviedb.org/settings/api) (Free)
* [NewsAPI Key](https://newsapi.org/register) (Free)

### Installation
```bash
git clone <repository-url>
cd cinesocial
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate

pip install -r requirements.txt

```

### Database & Server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

```

*API Base URL: `http://127.0.0.1:8000/api/*`

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your_django_secret_key
TMDB_API_KEY=your_tmdb_api_key
NEWS_API_KEY=your_news_api_key

```

---

## 🔐 Authentication

CineSocial uses **JSON Web Tokens (JWT)**. Include the access token in the header of protected requests:
`Authorization: Bearer <access_token>`

### Endpoints

* **Register:** `POST /api/accounts/register/`
* **Login:** `POST /api/auth/login/` (Returns `access` and `refresh`)
* **Refresh:** `POST /api/auth/refresh/`

---

## 👤 Users & Profiles

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| GET | `/api/accounts/profiles/<username>/` | No | Get profile data & follower counts |
| POST | `/api/accounts/profiles/<username>/follow/` | Yes | Toggle follow/unfollow |

---

## 📱 Social Feed

Posts support text (max 500 chars), an optional image, and a `tmdb_id` link.

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| GET | `/api/feed/posts/` | Yes | Feed (followed users first) |
| POST | `/api/feed/posts/` | Yes | Create a new post |
| POST | `/api/feed/posts/<pk>/like/` | Yes | Toggle like |
| POST | `/api/feed/posts/<pk>/repost/` | Yes | Repost with optional content |
| POST | `/api/feed/posts/<id>/comment/` | Yes | Add a comment |

---

## 🎬 Movies

Movie data is sourced from TMDB and cached locally for one hour.

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| GET | `/api/movies/trending/` | No | Weekly trending movies |
| GET | `/api/movies/search/?query=<text>` | No | Search TMDB films |
| GET | `/api/movies/<tmdb_id>/` | No | Details + community rating |
| POST | `/api/movies/<tmdb_id>/review/` | Yes | Submit/Update review (1-10) |
| POST | `/api/movies/<tmdb_id>/list/` | Yes | Toggle Favorite/Watchlist |

---

## ✉️ Messaging

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| POST | `/api/messages/send/` | Yes | Send message via `receiver` ID |
| GET | `/api/messages/inbox/` | Yes | View all received messages |
| GET | `/api/messages/conversation/<user_id>/` | Yes | Full chat history |
| POST | `/api/messages/<pk>/read/` | Yes | Mark message as read |

---

## 📰 News

Returns entertainment news via NewsAPI. Filter by keyword using `?q=`.

| Method | Endpoint | Auth | Description |
| --- | --- | --- | --- |
| GET | `/api/news/` | No | Latest movie news |
| GET | `/api/news/?q=keyword` | No | Filtered headlines |

---

## ⚠️ Error Responses

| Status | Meaning | Common Cause |
| --- | --- | --- |
| **400** | Bad Request | Validation error (check field-level messages) |
| **401** | Unauthorized | Missing or expired JWT token |
| **403** | Forbidden | Action not permitted (e.g., messaging self) |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Server Error | Check Django server logs |

---

## 🛠 Roadmap & Limitations

* **Comment Listing:** Currently, a direct list endpoint for post comments is missing. (Add `CommentListView`).
* **Follow Toggle:** Endpoint exists in views but needs registration in `accounts/urls.py`.
* **Messaging:** Plans to add `sender_id` to `MessageSerializer` for easier front-end lookup.
* **Production:** Ensure `DEBUG=False` and set specific `CORS_ALLOWED_ORIGINS` before deployment.

---
