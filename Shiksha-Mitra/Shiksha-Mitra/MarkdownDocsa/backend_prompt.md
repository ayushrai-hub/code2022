You are a senior full-stack developer tasked with implementing the complete backend infrastructure and APIs for Shiksha-Mitra, an educational platform that connects students for collaborative learning. 

Build a robust, scalable backend system with the following requirements:

PHASE 1 - FOUNDATION & ARCHITECTURE (Weeks 1-2)
========================================

1. PROJECT SETUP & ARCHITECTURE:
   - Set up Node.js + Express.js OR Next.js API routes architecture
   - Configure TypeScript with strict mode
   - Implement clean architecture pattern (controllers, services, repositories)
   - Set up environment configuration management
   - Create API versioning strategy (/api/v1/)
   - Implement proper error handling middleware
   - Set up logging system (Winston/Pino)
   - Configure CORS, helmet, and security middleware

2. DATABASE DESIGN & SETUP:
   - Design PostgreSQL schema for all entities
   - Set up Prisma ORM with proper relations
   - Create migration scripts
   - Implement database connection pooling
   - Set up Redis for caching and sessions
   - Design indexes for optimal query performance
   - Implement soft delete functionality

3. AUTHENTICATION SYSTEM:
   - JWT token management (access + refresh tokens)
   - OAuth integration (Google, GitHub, LinkedIn)
   - Phone number OTP verification
   - Email verification flow
   - Password hashing with bcrypt + salt
   - Rate limiting for auth endpoints
   - Session management with Redis
   - Role-based access control (RBAC)

PHASE 2 - CORE APIs & BUSINESS LOGIC (Weeks 3-5)
===============================================

4. USER MANAGEMENT APIs:
   - POST /api/v1/auth/register
   - POST /api/v1/auth/login
   - POST /api/v1/auth/refresh
   - POST /api/v1/auth/logout
   - GET /api/v1/users/profile
   - PUT /api/v1/users/profile
   - POST /api/v1/users/upload-avatar
   - GET /api/v1/users/search

5. STUDY BUDDY MATCHING SYSTEM:
   - Design matching algorithm with weighted scoring
   - POST /api/v1/matching/find-buddies
   - GET /api/v1/matching/recommendations
   - POST /api/v1/matching/send-request
   - PUT /api/v1/matching/respond-request
   - GET /api/v1/matching/connections
   - DELETE /api/v1/matching/remove-connection

6. REAL-TIME COMMUNICATION:
   - Socket.io setup for real-time features
   - Chat system with message persistence
   - Online status tracking
   - Study room creation and management
   - File sharing with proper validation
   - Message encryption for privacy

PHASE 3 - ADVANCED FEATURES (Weeks 6-8)
=====================================

7. AI INTEGRATION:
   - OpenAI GPT-4 API integration
   - Conversation context management
   - POST /api/v1/ai/chat
   - POST /api/v1/ai/generate-study-plan
   - POST /api/v1/ai/explain-concept
   - POST /api/v1/ai/create-quiz
   - Implement RAG for educational content

8. CONTENT MANAGEMENT:
   - Study material upload and management
   - Content categorization and tagging
   - Search functionality with filters
   - Content moderation system
   - Version control for study materials

9. ANALYTICS & INSIGHTS:
   - User behavior tracking
   - Learning progress analytics
   - Platform usage statistics
   - Performance metrics collection
   - Dashboard APIs for admin panel

PHASE 4 - OPTIMIZATION & DEPLOYMENT (Weeks 9-10)
==============================================

10. PERFORMANCE OPTIMIZATION:
    - Database query optimization
    - Implement caching strategies
    - API response compression
    - Background job processing
    - Rate limiting and throttling

11. TESTING & QUALITY ASSURANCE:
    - Unit tests for all services
    - Integration tests for APIs
    - Load testing for critical endpoints
    - Security vulnerability testing
    - API documentation with Swagger

12. DEPLOYMENT & MONITORING:
    - Docker containerization
    - CI/CD pipeline setup
    - Production environment configuration
    - Monitoring and alerting setup
    - Backup and recovery strategies

TECHNICAL REQUIREMENTS:
====================
- Use TypeScript throughout
- Implement proper error handling and validation (Zod)
- Follow RESTful API conventions
- Use middleware for cross-cutting concerns
- Implement proper logging and monitoring
- Ensure API security best practices
- Write comprehensive tests (Jest)
- Document APIs with OpenAPI/Swagger

DELIVERABLES:
============
For each phase, provide:
1. Complete TypeScript code implementation
2. Database schema and migrations
3. API endpoint documentation
4. Test cases and examples
5. Deployment configuration
6. Performance optimization notes
7. Security implementation details

Start with Phase 1 and provide complete, production-ready code for each component.