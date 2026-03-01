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

### Endpoint summary
| Method | Path                                  | Auth Required | Description                              | Notes                                                                            |
| ------ | ------------------------------------- | ------------- | ---------------------------------------- | -------------------------------------------------------------------------------- |
| POST   | /api/auth/login/                      | No            | Obtain JWT access and refresh tokens     | Use `access` for authenticated requests                                          |
| POST   | /api/auth/refresh/                    | No            | Refresh access token using refresh token | Returns new access token                                                         |
| POST   | /api/accounts/register/               | No            | Register a new user                      | Requires username, email, password/password2, bio, avatar, date_of_birth, gender |
| GET    | /api/accounts/profiles/<username>     | Optional      | Retrieve user profile                    | Includes follower/following counts and is_following relative to current user     |
| GET    | /api/accounts/test/                   | Optional      | Test authentication endpoint             | Returns simple auth verification                                                 |
| POST   | /api/feed/posts/                      | Yes           | Create a new post                        | Include `content`, optional `image`, optional `tmdb_id`                          |
| POST   | /api/feed/posts/<pk>/like/            | Yes           | Toggle like/unlike a post                | Returns `{"liked": true/false}`                                                  |
| POST   | /api/feed/posts/<post_id>/comment/    | Yes           | Add a comment to a post                  | Include `content`                                                                |
| GET    | /api/feed/posts/<pk>/                 | Optional      | Retrieve a single post                   | Includes counts: likes, comments, reposts, and `is_liked`                        |
| GET    | /api/feed/comments/<pk>/              | Optional      | Retrieve a single comment                | Includes threaded replies                                                        |
| POST   | /api/feed/posts/<pk>/repost/          | Yes           | Create a repost of an existing post      | Returns the repost object                                                        |
| GET    | /api/movies/search/                   | Optional      | Search TMDB movies                       | Query param: `?query=<text>`; includes local average_rating if reviewed          |
| GET    | /api/movies/<tmdb_id>/                | Optional      | Get TMDB movie details                   | Includes local ratings: average_rating and review_count                          |
| POST   | /api/movies/<tmdb_id>/review/         | Yes           | Submit or update a movie review          | Include `rating` and `content`                                                   |
| POST   | /api/movies/<tmdb_id>/list/           | Yes           | Toggle movie in Favorites or Watchlist   | Include `list_type` = favorite/watchlist                                         |
| GET    | /api/movies/list/<list_type>/         | Yes           | Retrieve current user's movies in a list | `<list_type>` = favorite or watchlist                                            |
| GET    | /api/messages/send/                   | Yes           | Send a private message                   | Include `receiver` (user id) and `content`                                       |
| GET    | /api/messages/inbox/                  | Yes           | Retrieve inbox messages                  | Paginated                                                                        |
| GET    | /api/messages/conversation/<user_id>/ | Yes           | Retrieve conversation with specific user | Paginated, bidirectional                                                         |
| POST   | /api/messages/<pk>/read/              | Yes           | Mark a message as read                   | `pk` = message id                                                                |
| GET    | /api/messages/unread-count/           | Yes           | Get unread messages count                | Returns `{"unread_count": number}`                                               |
| GET    | /api/news/                            | Optional      | Retrieve trending news from News API     | Returns list of articles with title, url, source, published_at                   |
