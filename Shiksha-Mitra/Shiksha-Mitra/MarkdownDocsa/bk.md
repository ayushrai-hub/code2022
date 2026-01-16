Shiksha-Mitra Backend (FastAPI) — Detailed Implementation Guide
This is a comprehensive backend guide for building the Shiksha-Mitra platform using FastAPI. It covers what to implement, which tools to use, APIs to expose, and how everything integrates end-to-end.

0) High-level Goals
Reliable, secure, and scalable FastAPI backend
PostgreSQL via SQLAlchemy/SQLModel and Alembic migrations
JWT-based auth + Multi-provider OAuth + Email + Phone OTP + 2FA
Redis for caching, sessions, rate limiting, and pub/sub
WebSockets for real-time chat/notifications and WebRTC signaling
ML-driven matching service (batch + on-demand)
AI/RAG assistant using OpenAI + LangChain + sentence-transformers + Pinecone
Background jobs via Celery + Redis
Robust observability (Sentry, structured logs), CI/CD, and security
1) Tech Stack and Dependencies
Backend Framework

FastAPI (ASGI)
Uvicorn (ASGI server)
Data and Storage

PostgreSQL (primary DB)
SQLAlchemy 2.x + SQLModel for ORM
Alembic for migrations
Redis for cache, rate limit counters, OTP, session, pub/sub
Auth and Security

python-jose[cryptography] for JWT
passlib[bcrypt] for password hashing
Authlib for OAuth clients (Google, GitHub, LinkedIn)
pyotp for TOTP-based 2FA
slowapi for rate limiting (optional but recommended)
python-multipart for file uploads
helmet-style security headers via Starlette middleware config
AI/ML

openai for GPT models
langchain for RAG orchestration
sentence-transformers for local embeddings
pinecone-client for vector search
Async/Background Tasks and Real-time

celery for background jobs
aioredis/redis for async Redis
FastAPI WebSockets for chat/signaling
Media and Notifications

cloudinary for media storage
sendgrid for email
twilio for SMS/WhatsApp (OTP, notifications)
Testing and Monitoring

pytest, pytest-asyncio, httpx for tests
structlog for JSON logging
sentry-sdk[fastapi] for monitoring
Example requirements.txt (additions marked)

fastapi, uvicorn, sqlalchemy, sqlmodel, alembic, psycopg2-binary, redis, pydantic, pydantic-settings
python-jose[cryptography], passlib[bcrypt], python-multipart
openai, langchain, sentence-transformers, pinecone-client
celery, aioredis, websockets
cloudinary, Pillow
sendgrid, twilio
pytest, pytest-asyncio, httpx, factory-boy
structlog, sentry-sdk[fastapi]
authlib 1.3.1 (add)
slowapi 0.1.9 (add)
pyotp 2.9.0 (add)
2) Project Structure
shiksha-mitra-backend/

app/
main.py
core/
config.py (PydanticSettings)
database.py (engine/session)
redis.py (Redis client)
security.py (JWT, password, scopes)
deps.py (FastAPI dependencies: db, current_user, roles)
models/ (SQLModel or SQLAlchemy ORM models)
user.py, profile.py, match.py, chat.py, study_session.py, oauth.py, tokens.py, analytics.py
schemas/ (Pydantic models)
auth.py, user.py, profile.py, match.py, chat.py, common.py
api/v1/ (Routers)
auth.py, users.py, profiles.py, matching.py, chats.py, study_sessions.py, ai.py, admin.py, analytics.py
services/ (Business logic)
auth_service.py, user_service.py, profile_service.py, matching_service.py, chat_service.py, ai_service.py, notification_service.py, media_service.py
repositories/ (DB persistence logic)
base.py, user_repository.py, profile_repository.py, match_repository.py, chat_repository.py
websocket/
connection_manager.py, chat_handler.py, signaling_handler.py, notification_handler.py
tasks/ (Celery)
matching_tasks.py, email_tasks.py, analytics_tasks.py, media_tasks.py
middleware/
cors.py, logging.py, rate_limiting.py, security_headers.py
alembic/ (migrations)
tests/
docker/
Dockerfile, docker-compose.yml, docker-compose.prod.yml
scripts/
seed_database.py, run_migrations.py, create_admin.py
.env.example, alembic.ini, pyproject.toml
3) Configuration and Environment
Environment variables (example)

APP_ENV, APP_PORT
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/db
REDIS_URL=redis://redis:6379/0
SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
JWT_ALG=HS256
OAUTH_GOOGLE_CLIENT_ID, OAUTH_GOOGLE_CLIENT_SECRET
OAUTH_GITHUB_CLIENT_ID, OAUTH_GITHUB_CLIENT_SECRET
OAUTH_LINKEDIN_CLIENT_ID, OAUTH_LINKEDIN_CLIENT_SECRET
SENDGRID_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@cloud_name
OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENV
SENTRY_DSN
app/core/config.py

Use Pydantic Settings to load envs.
Provide computed defaults and validation.
4) Database Design (ER Overview)
Core entities

User: id, email, phone, password_hash, role, is_active, is_verified, twofa_enabled, created_at, updated_at
OAuthAccount: id, provider, provider_account_id, access_token, refresh_token, user_id
Profile: first_name, last_name, avatar_url, bio, location fields, visibility settings
Education: school, degree, field, start_date, end_date, profile_id
Skill: name, level, profile_id
Interest: name, profile_id
Availability: weekday, start_time, end_time, timezone, user_id
StudyPreference: learning_style, goals, modalities, subjects, level, user_id
PortfolioItem/Achievement: title, description, link, issued_by, date, profile_id
Match and MatchCandidate: store candidates and confirmed matches
MatchFeedback: rating, comment, success flags
ChatRoom: id, type (direct/group/session), member list
Message: id, room_id, sender_id, content, content_type, file_url, created_at, edited_at
StudySession: id, topic, start_at, end_at, participants, whiteboard_state_url, recording_url
AnalyticsEvent: user_id, name, payload_json, created_at
Tokens: RefreshToken (jti, user_id, expires_at, revoked), EmailVerificationToken, PhoneOTP, PasswordResetToken
AIConversation: id, user_id, messages, context, created_at
Indexing strategy

Unique indexes on email, phone
B-tree indexes on foreign keys (user_id, room_id)
GIN index for JSONB fields (preferences, analytics payload if needed)
Composite indexes for message retrieval (room_id, created_at desc)
Partial indexes for active tokens
Example SQLModel model (excerpt)

python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: cuid(), primary_key=True)
    email: str = Field(index=True, unique=True)
    phone: Optional[str] = Field(default=None, index=True, unique=True)
    password_hash: Optional[str] = None
    role: str = Field(default="STUDENT")
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    twofa_enabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    profile: Optional["Profile"] = Relationship(back_populates="user")

class Profile(SQLModel, table=True):
    id: str = Field(default_factory=lambda: cuid(), primary_key=True)
    user_id: str = Field(foreign_key="user.id", unique=True)
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    visibility: str = Field(default="PUBLIC")

    user: "User" = Relationship(back_populates="profile")
Migration flow

Define models
Autogenerate migrations: alembic revision --autogenerate -m "init"
Review, then apply: alembic upgrade head
5) Authentication and Authorization
Flows supported

Email/password with bcrypt
Multi-provider OAuth2 (Google, GitHub, LinkedIn) via Authlib
Phone OTP verification via Twilio (login and 2nd-factor)
Email verification via SendGrid link
JWT Auth: Access + Refresh tokens (short + long TTL)
Role-based access control (Student, Teacher, Institution, Admin)
Optional 2FA (TOTP via pyotp)
Token strategy

Access token: 15 minutes default
Refresh token: 7–30 days; store jti in DB or Redis; allow rotation; revoke on logout
JWT claims: sub (user_id), role, scopes, token_use (access/refresh), exp, jti
Password policy

Hash with bcrypt + salt (pass
GPT-5 (Thinking)
continue


Thought Process
expand
Shiksha-Mitra Backend (FastAPI) — Detailed Implementation Guide (Continued)
This continues from section 5. It provides in-depth implementation details, APIs, and integration notes for the entire FastAPI backend.

5) Authentication and Authorization (continued)
Password policy

Hash with bcrypt via passlib context (auto-salt).
Minimum length 12, require 1 uppercase, 1 lowercase, 1 digit, 1 symbol.
Password breach check (optional): k-Anonymity via HaveIBeenPwned range API.
Store only hashes; never log or return raw passwords.
Password reset via signed one-time token (short TTL, single-use).
Account linking

Users can link OAuth providers to existing accounts after a verified login.
Flow:
Authenticated user hits /auth/oauth/link/{provider} to start OAuth.
On callback, if provider_account_id already linked to another user, block with 409.
Else persist OAuthAccount and return updated linked providers list.
Email verification

On signup, send signed verification link with expiry (e.g., 24h).
Verify endpoint marks user.is_verified = True, logs time, invalidates token.
Re-send limit: rate-limit by email and IP.
Phone OTP

OTP code (6 digits) stored in Redis with TTL (e.g., 5–10 minutes).
Rate-limit by phone and IP (e.g., 3 per hour, 10/day).
Twilio SMS delivery; optional WhatsApp.
On verify, mark phone_verified_at, attach to user if not already.
2FA (TOTP)

Use pyotp to generate secret; display QR (otpauth URL).
Require 2 consecutive valid codes to enable.
Store backup codes (salted hashes) for recovery, one-time use.
During login, after primary auth, challenge for TOTP if enabled.
OAuth2 (Authlib)

Providers: Google, GitHub, LinkedIn.
Use OAuth PKCE (if using public clients), state param for CSRF.
Map provider profile to user fields; store provider_account_id and tokens.
Refresh tokens

JWT access (15m), refresh (7–30 days).
Store refresh token jti in DB or Redis with status and expiry.
Rotate refresh on each use (issue new refresh, revoke old).
Revoke all on password change or suspicious activity.
Authorization model

Roles: STUDENT, TEACHER, INSTITUTION, ADMIN.
Optional scopes per endpoint.
Ownership checks on user-owned resources (IDOR prevention).
Admin-only routes protected by role dependency.
Rate limiting and bot defense

slowapi for IP+identity-based rate limits (e.g., /auth/*).
Optional CAPTCHA after threshold (hCaptcha/Cloudflare Turnstile) verification.
Brute-force lockout with exponential backoff per user/email.
5.1 Auth Data Models (SQLModel)
User: id, email, phone, password_hash, role, is_active, is_verified, twofa_enabled, created_at, updated_at
OAuthAccount: id, provider, provider_account_id, access_token, refresh_token, token_expires_at, user_id
RefreshToken: jti, user_id, revoked_at, expires_at, user_agent_hash, ip_hash
EmailVerificationToken: id, user_id, token, expires_at, used_at
PasswordResetToken: id, user_id, token, expires_at, used_at
5.2 Security Utilities
JWT encode/decode with python-jose, alg = HS256 or RS256 (recommended in prod).
Password hashing with passlib CryptContext.
CSRF for cookie-based flows (if any), else stick to Authorization: Bearer for APIs.
Security headers middleware (CSP, HSTS, X-Content-Type-Options, Referrer-Policy).
5.3 Core Auth Endpoints
POST /api/v1/auth/register
body: { email, password, first_name, last_name, phone? }
actions: create user, send verification email, optional OTP to phone
POST /api/v1/auth/login
body: { email, password }
returns: { access_token, refresh_token, requires_2fa? }
POST /api/v1/auth/2fa/verify
body: { code or backup_code }
returns: tokens
POST /api/v1/auth/refresh
body: { refresh_token }
rotates refresh, checks jti, returns new access/refresh
POST /api/v1/auth/logout
body: { refresh_token? }, revoke current refresh token (and optionally all)
POST /api/v1/auth/password/forgot
body: { email }, send password reset link
POST /api/v1/auth/password/reset
body: { token, new_password }
POST /api/v1/auth/phone/send-otp
body: { phone }
POST /api/v1/auth/phone/verify
body: { phone, code }
GET /api/v1/auth/email/verify?token=...
GET /api/v1/auth/me
returns current user profile summary
GET /api/v1/auth/oauth/{provider}
redirect to provider auth URL
GET /api/v1/auth/oauth/{provider}/callback
handles provider callback, sign-in/up, returns tokens
POST /api/v1/auth/oauth/link/{provider}
link provider to existing account (requires Authorization)
DELETE /api/v1/auth/oauth/unlink/{provider}
Responses include standardized error shape: { error: { code, message, details? } }

6) User and Profile Management
Entities

Profile: basic info, avatar_url, bio, visibility
Education, Experience (optional), Skills, Interests
Preferences: learning_style, subjects, level, goals
Availability: weekday, start_time, end_time, tz
Portfolio/Achievements
Endpoints

GET /api/v1/users/{id} (admin or self with limited fields)
GET /api/v1/users/me
PATCH /api/v1/users/me
body: partial updates for user fields allowed by policy
GET /api/v1/profiles/me
PATCH /api/v1/profiles/me
multipart for avatar upload or Cloudinary signed upload workflow
POST /api/v1/profiles/me/education
PATCH /api/v1/profiles/me/education/{edu_id}
DELETE /api/v1/profiles/me/education/{edu_id}
Similar endpoints for skills, interests, availability, achievements
Validation

Use Pydantic models; constrain strings, whitelist enums.
Zod-friendly JSON schema support for frontend form generation if needed.
Media handling

Prefer client-to-Cloudinary direct uploads with signed presets.
Backend issues a signed upload signature; store resulting URL in DB after webhook confirmation.
Privacy and visibility

Visibility: PUBLIC, NETWORK, PRIVATE; filter fields accordingly in serializers.
Enforce ownership checks on write routes.
7) Study Buddy Matching Service
Goals

Multi-factor: subject, level, learning style, schedule overlap, proximity (optional), personality (optional via survey), goals, historical success
Hybrid approach:
Rule-based weighted scoring for initial candidates
Collaborative filtering and success prediction for reranking
Feedback loop via MatchFeedback
Data required

User Preferences/Subjects/Levels
Availability (time-grid by TZ)
Location (optional approximate geohash)
Interaction history: past matches, ratings, duration, outcomes
Implicit signals: message counts, session attendance
Scoring components (example weights)

Subject overlap (0–30)
Level compatibility (0–10)
Availability overlap (0–25)
Goals alignment (0–10)
Learning style compatibility (0–10)
Distance penalty or boost (±5)
Personality/Survey similarity (0–5)
Past success priors (±10)
Algorithm (pseudocode)

Candidate retrieval
Filter by role (students vs teachers or peer match), active, verified
Subject/level prefilter via tags
Optional geo prefilter by region
Compute features: Jaccard(subjects), time-overlap (minutes), style distance, goal vector cos-sim
Base score = Σ weight_i * feature_i
Collaborative filtering rerank
Train lightweight implicit ALS or nearest-neighbor from feedback matrix (user x partner, rating)
Use similarities to adjust scores
Success probability model
Logistic regression/xgboost on historical features; multiply score by P(success)
Safety filters
Blocklist, age-appropriate constraints, report scores
Final list
Sort desc by score, keep top N
Diversity constraint (avoid repeated same-school or same-geo too often)
Processing

On-demand suggestions endpoint returns candidates quickly using cached features in Redis.
Nightly batch job recomputes embeddings/features and stores precomputed candidate sets.
Endpoints

GET /api/v1/matching/suggestions?limit=10
POST /api/v1/matching/accept
body: { candidate_user_id }
creates Match, notifies counterpart; mutual accept -> confirmed match
POST /api/v1/matching/decline
GET /api/v1/matching/history
POST /api/v1/matching/feedback
body: { match_id, rating (1–5), comment?, success_flags? }
Storage

MatchCandidate: user_id, candidate_id, score, computed_at
Match: id, user_a_id, user_b_id, status (PENDING, CONFIRMED, ENDED), created_at
MatchFeedback: match_id, rater_id, rating, comment, tags, created_at
Testing

Seed synthetic users with varied profiles.
Evaluate precision@K using a holdout of known “successful” pairs.
8) Real-time Communication (Chat, Presence, Signaling)
Transport

WebSockets via FastAPI for:
Chat channels (1:1, group)
Presence (online/offline, typing)
Notifications
WebRTC signaling (offer/answer/candidates)
Connection management

JWT auth on connection
Keep connection map: user_id -> websocket set
Ping/pong heartbeats, auto-reconnect support
Topic rooms keyed by chat_room_id
Chat features

Message types: text, image, file, voice note
Upload files via REST to Cloudinary; send message with URL
Message states: sent, delivered, read; maintain read receipts
Pagination: keyset by created_at, id
Moderation: profanity filter, blocklist, report message endpoint
Encryption: at-rest via DB; optional client-side E2EE (out of scope here)
Signaling for WebRTC

WS topics per session room: send offer, answer, ICE candidates
STUN/TURN
Use public STUN (e.g., Google) for dev
Use managed TURN (Twilio/Nimble/WSTURN) for prod reliability
Session lifecycle events: created, joined, left, ended
Consent for recording: boolean flag stored in session, block recording if not consented
Endpoints (REST)

POST /api/v1/chats
body: { member_ids, type }
GET /api/v1/chats/{room_id}/messages?before=...&limit=50
POST /api/v1/chats/{room_id}/messages
body: { content, content_type, file_url? }
POST /api/v1/chats/{room_id}/read-receipts
POST /api/v1/chats/{room_id}/report
GET /api/v1/chats
DELETE /api/v1/chats/{room_id} (owner/admin)
WebSocket channels

/ws/chat?token=...
subscribe: { action: "join", room_id }
message: { action: "message", room_id, payload: { ... } }
typing: { action: "typing", room_id, is_typing: true }
ack delivery/read events
/ws/signaling?token=...
{ action: "offer"/"answer"/"candidate", room_id, payload }
Persistence

ChatRoom: id, type, members
Message: id, room_id, sender_id, content, type, file_url, created_at, edited_at, deleted_at
MessageReceipt: message_id, user_id, delivered_at, read_at
9) Study Sessions and Whiteboard
Entities

StudySession: id, topic, created_by, room_id (chat), start_at, end_at, recording_url, whiteboard_state_url, consent_recording
SessionParticipant: session_id, user_id, joined_at, left_at, role
Endpoints

POST /api/v1/study-sessions

