This is the properly formatted Markdown code for your GitHub `README.md`. It includes functional anchors for the Table of Contents, syntax highlighting for the code blocks, and correctly formatted tables.

```markdown
# CineSocial Backend API

CineSocial is a headless social platform designed for movie enthusiasts. It provides movie data via TMDB integration and facilitates social interactions through posts, comments, likes, messaging, and news aggregation. 

This backend is built using **Django REST Framework (DRF)** and utilizes **JWT** for secure authentication.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [User & Profile Endpoints](#user--profile-endpoints)
4. [Social Feed Endpoints](#social-feed-endpoints)
5. [Movie Wiki Endpoints](#movie-wiki-endpoints)
6. [Messaging Endpoints](#messaging-endpoints)
7. [News Endpoints](#news-endpoints)
8. [Pagination & Rate Limiting](#pagination--rate-limiting)
9. [Environment Variables](#environment-variables)

---

## Getting Started

### Installation
Clone the repository and set up a virtual environment:

```bash
git clone <repository-url>
cd cinesocial
python -m venv venv

# Activate environment
source venv/bin/activate # Linux / macOS
venv\Scripts\activate    # Windows

pip install -r requirements.txt

```

### Database & Server

Run migrations and initialize the development server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

```

---

## Authentication

### Register

`POST /api/auth/register/`

**Request Body:**

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "securepassword",
  "password2": "securepassword",
  "bio": "Movie fan",
  "avatar": null,
  "date_of_birth": "2000-01-01",
  "gender": "M"
}

```

### Login

`POST /api/auth/login/`

**Request Body:**

```json
{
  "username": "user1",
  "password": "securepassword"
}

```

*Response: Returns JWT tokens (`access`, `refresh`).*

> **Note:** Include the header `Authorization: Bearer <access_token>` for all protected endpoints.

---

## User & Profile Endpoints

### Get User Profile

`GET /api/profiles/{username}/`

Returns user details including:

* Bio and avatar.
* `follower_count` and `following_count`.
* `is_following` status (relative to the current user).

### Follow / Unfollow

`POST /api/profiles/{username}/follow/`
Toggles the follow state.

---

## Social Feed Endpoints

### Create Post

`POST /api/posts/create/`

* **Type:** `multipart/form-data`
* **Fields:** `content` (string), `image` (file, optional), `tmdb_id` (int, optional).

### Interactions

* **Repost:** `POST /api/posts/{post_id}/repost/`
* **Like / Unlike:** `POST /api/posts/{post_id}/like/`
* **Comment:** `POST /api/posts/{post_id}/comment/`

### Feed & Retrieval

* **Main Feed:** `GET /api/posts/feed/` (Posts from followed users).
* **Single Post:** `GET /api/posts/{post_id}/` (Includes interaction counts and like status).

---

## Movie Wiki Endpoints

### Search & Details

* **Search:** `GET /api/movies/search/?query=inception`
* **Details:** `GET /api/movies/{tmdb_id}/`

### Reviews & Lists

* **Submit Review:** `POST /api/movies/{tmdb_id}/review/` (Rating 1-10).
* **Manage Lists:** `POST /api/movies/{tmdb_id}/list/` (Body: `{"list_type": "favorite"}` or `"watchlist"`).

---

## Messaging Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/messages/send/` | POST | Send message to `receiver` (ID) |
| `/api/messages/inbox/` | GET | List latest messages |
| `/api/messages/conversation/{user_id}/` | GET | Full chat history |
| `/api/messages/unread-count/` | GET | Count of unread messages |

---

## News Endpoints

`GET /api/news/` | `GET /api/news/?q=Marvel`

Returns trending articles from NewsAPI including titles, descriptions, and source URLs.

---

## Pagination & Rate Limiting

* **Pagination:** List endpoints default to 10 items per page.
* **Throttling:**

| User Type | Limit |
| --- | --- |
| Anonymous | 50 requests / day |
| Authenticated | 1,000 requests / day |

---

## Environment Variables

Create a `.env` file in the root directory:

```env
DJANGO_SECRET_KEY=your_secret_key
TMDB_API_KEY=your_tmdb_api_key
NEWS_API_KEY=your_news_api_key

```

---

## Notes

* All data modification endpoints require JWT authentication.
* Interactions (Likes, Follows, Reviews) are toggle-based or update-on-resubmit.
