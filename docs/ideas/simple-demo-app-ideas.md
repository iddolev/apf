# Simple Demo App Ideas for APF

Simple webapp ideas that exercise all five APF agent roles: backend, frontend, testing, code review, and tech lead.

---

## 1. Bookmark Manager

- Backend: REST API for CRUD on bookmarks + tags, simple auth
- Frontend: Tag-based UI with search/filter, drag-to-reorder
- Testing: API tests, UI tests for filtering logic
- Code Review: Data validation, SQL injection prevention
- Tech Lead: Schema design decisions, API contract alignment

## 2. Poll/Voting App

- Backend: Create polls, cast votes, real-time tallies
- Frontend: Poll creation form, live results with charts
- Testing: Race conditions on vote counting, input validation
- Code Review: Duplicate vote prevention, data integrity
- Tech Lead: Architecture for real-time updates (SSE vs polling vs WebSocket)

## 3. Habit Tracker

- Backend: Track daily habits, streaks, completion history
- Frontend: Calendar/grid view, streak visualizations
- Testing: Date boundary edge cases, streak calculation logic
- Code Review: Time zone handling, business logic correctness
- Tech Lead: Data model for flexible habit frequencies

## 4. Shared Shopping List

- Backend: Lists, items, categories, simple multi-user support
- Frontend: Checklist UI with categories, add/remove items
- Testing: Concurrent edits, item state transitions
- Code Review: Input sanitization, API design consistency
- Tech Lead: Conflict resolution strategy for shared state

## 5. Micro-Blog / Status Board

- Backend: Post short messages, markdown support, simple feed
- Frontend: Feed view, compose box, markdown preview
- Testing: XSS prevention, pagination, empty states
- Code Review: Content sanitization, API pagination patterns
- Tech Lead: Feed architecture, caching strategy

---

## Recommendation

**Poll/Voting App**. It's simple enough to build quickly but naturally creates interesting decisions
across all agents — real-time updates force a tech lead architecture call, vote integrity demands
good code review, race conditions make testing meaningful, and both backend and frontend have clear,
non-trivial work.
