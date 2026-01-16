Backend & API Implementation Guide
Table of Contents
Project Architecture
Database Design
Authentication System
Core APIs Development
Real-time Features
AI Integration
Testing Strategy
Performance Optimization
Deployment & DevOps
Monitoring & Maintenance
1. Project Architecture
1.1 Backend Stack Selection
Primary Technology Stack:

typescript
// package.json dependencies
{
  "dependencies": {
    "express": "^4.18.0",
    "typescript": "^5.0.0",
    "@prisma/client": "^5.0.0",
    "jsonwebtoken": "^9.0.0",
    "bcryptjs": "^2.4.3",
    "joi": "^17.9.0",
    "redis": "^4.6.0",
    "socket.io": "^4.7.0",
    "winston": "^3.10.0",
    "helmet": "^7.0.0",
    "cors": "^2.8.5",
    "express-rate-limit": "^6.8.0",
    "multer": "^1.4.5",
    "cloudinary": "^1.37.0"
  }
}
1.2 Project Structure
text
backend/
├── src/
│   ├── controllers/          # Request handlers
│   │   ├── auth.controller.ts
│   │   ├── user.controller.ts
│   │   ├── matching.controller.ts
│   │   └── ai.controller.ts
│   ├── services/            # Business logic
│   │   ├── auth.service.ts
│   │   ├── user.service.ts
│   │   ├── matching.service.ts
│   │   └── ai.service.ts
│   ├── repositories/        # Data access layer
│   │   ├── user.repository.ts
│   │   ├── match.repository.ts
│   │   └── chat.repository.ts
│   ├── middleware/          # Express middleware
│   │   ├── auth.middleware.ts
│   │   ├── validation.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── rateLimit.middleware.ts
│   ├── routes/             # API routes
│   │   ├── auth.routes.ts
│   │   ├── user.routes.ts
│   │   ├── matching.routes.ts
│   │   └── ai.routes.ts
│   ├── utils/              # Utility functions
│   │   ├── jwt.util.ts
│   │   ├── encryption.util.ts
│   │   ├── validation.util.ts
│   │   └── logger.util.ts
│   ├── types/              # TypeScript definitions
│   │   ├── user.types.ts
│   │   ├── auth.types.ts
│   │   └── api.types.ts
│   ├── config/             # Configuration
│   │   ├── database.config.ts
│   │   ├── redis.config.ts
│   │   └── app.config.ts
│   └── app.ts              # Express app setup
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
│   └── api/
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
1.3 Application Setup
typescript
// src/app.ts
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { errorHandler } from './middleware/error.middleware';
import { logger } from './utils/logger.util';
import { connectDatabase } from './config/database.config';
import { connectRedis } from './config/redis.config';

// Route imports
import authRoutes from './routes/auth.routes';
import userRoutes from './routes/user.routes';
import matchingRoutes from './routes/matching.routes';
import aiRoutes from './routes/ai.routes';

class App {
  public express: express.Application;

  constructor() {
    this.express = express();
    this.initializeMiddleware();
    this.initializeRoutes();
    this.initializeErrorHandling();
  }

  private initializeMiddleware(): void {
    this.express.use(helmet());
    this.express.use(cors({
      origin: process.env.FRONTEND_URL || 'http://localhost:3000',
      credentials: true
    }));
    this.express.use(compression());
    this.express.use(express.json({ limit: '10mb' }));
    this.express.use(express.urlencoded({ extended: true, limit: '10mb' }));
  }

  private initializeRoutes(): void {
    this.express.use('/api/v1/auth', authRoutes);
    this.express.use('/api/v1/users', userRoutes);
    this.express.use('/api/v1/matching', matchingRoutes);
    this.express.use('/api/v1/ai', aiRoutes);
  }

  private initializeErrorHandling(): void {
    this.express.use(errorHandler);
  }

  public async start(port: number): Promise<void> {
    try {
      await connectDatabase();
      await connectRedis();
      
      this.express.listen(port, () => {
        logger.info(`Server started on port ${port}`);
      });
    } catch (error) {
      logger.error('Failed to start server:', error);
      process.exit(1);
    }
  }
}

export default App;
2. Database Design
2.1 Prisma Schema
prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

enum Role {
  STUDENT
  TEACHER
  INSTITUTION
  ADMIN
}

enum MatchStatus {
  PENDING
  ACCEPTED
  REJECTED
  BLOCKED
}

enum ChatType {
  DIRECT
  GROUP
  STUDY_ROOM
}

model User {
  id          String   @id @default(cuid())
  email       String   @unique
  phone       String?  @unique
  password    String?
  role        Role     @default(STUDENT)
  isVerified  Boolean  @default(false)
  isActive    Boolean  @default(true)
  lastSeen    DateTime @default(now())
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  // Relations
  profile          Profile?
  oauthAccounts    OAuthAccount[]
  sentMatches      Match[]        @relation("MatchSender")
  receivedMatches  Match[]        @relation("MatchReceiver")
  chatParticipants ChatParticipant[]
  messages         Message[]
  studySessions    StudySession[]
  aiConversations  AIConversation[]

  @@map("users")
}

model Profile {
  id              String    @id @default(cuid())
  userId          String    @unique
  firstName       String
  lastName        String
  avatar          String?
  bio             String?
  dateOfBirth     DateTime?
  location        Json?     // {city, state, country}
  timezone        String?
  
  // Academic Information
  currentLevel    String?   // High School, Undergraduate, Graduate
  institution     String?
  major           String?
  yearOfStudy     Int?
  gpa             Float?
  
  // Learning Preferences
  learningStyle   String[]  // Visual, Auditory, Kinesthetic, Reading
  studyTimes      Json?     // Preferred study schedule
  subjects        String[]  // Areas of study/interest
  goals           String[]  // Learning objectives
  
  // Social & Collaboration
  languages       String[]
  availability    Json?     // Weekly availability schedule
  collaborationPrefs Json?  // Group size, communication style, etc.
  
  // Verification & Trust
  verificationLevel Int    @default(0) // 0-100 verification score
  trustScore        Float  @default(50.0)
  
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt
  
  user            User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("profiles")
}

model OAuthAccount {
  id          String @id @default(cuid())
  userId      String
  provider    String // google, github, linkedin
  providerId  String
  email       String
  accessToken String?
  refreshToken String?
  expiresAt   DateTime?
  createdAt   DateTime @default(now())
  
  user        User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  @@unique([provider, providerId])
  @@map("oauth_accounts")
}

model Match {
  id          String      @id @default(cuid())
  senderId    String
  receiverId  String
  status      MatchStatus @default(PENDING)
  message     String?
  matchScore  Float?      // Algorithm-calculated compatibility score
  
  // Match metadata
  commonInterests Json?
  sharedSubjects  String[]
  compatibilityFactors Json?
  
  createdAt   DateTime    @default(now())
  updatedAt   DateTime    @updatedAt
  respondedAt DateTime?
  
  sender      User        @relation("MatchSender", fields: [senderId], references: [id])
  receiver    User        @relation("MatchReceiver", fields: [receiverId], references: [id])
  
  @@unique([senderId, receiverId])
  @@map("matches")
}

model Chat {
  id          String    @id @default(cuid())
  type        ChatType
  name        String?   // For group chats and study rooms
  description String?
  isActive    Boolean   @default(true)
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
  
  participants ChatParticipant[]
  messages     Message[]
  
  @@map("chats")
}

model ChatParticipant {
  id        String   @id @default(cuid())
  chatId    String
  userId    String
  joinedAt  DateTime @default(now())
  leftAt    DateTime?
  isAdmin   Boolean  @default(false)
  isMuted   Boolean  @default(false)
  
  chat      Chat     @relation(fields: [chatId], references: [id], onDelete: Cascade)
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  @@unique([chatId, userId])
  @@map("chat_participants")
}

model Message {
  id        String   @id @default(cuid())
  chatId    String
  senderId  String
  content   String
  type      String   @default("text") // text, image, file, system
  metadata  Json?    // File info, image dimensions, etc.
  isEdited  Boolean  @default(false)
  isDeleted Boolean  @default(false)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  chat      Chat     @relation(fields: [chatId], references: [id], onDelete: Cascade)
  sender    User     @relation(fields: [senderId], references: [id], onDelete: Cascade)
  
  @@map("messages")
}

model StudySession {
  id          String   @id @default(cuid())
  hostId      String
  title       String
  description String?
  subject     String
  startTime   DateTime
  endTime     DateTime?
  isActive    Boolean  @default(true)
  maxParticipants Int?
  
  // Session configuration
  allowsRecording Boolean @default(false)
  requiresApproval Boolean @default(false)
  isPublic        Boolean @default(true)
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  host        User     @relation(fields: [hostId], references: [id])
  
  @@map("study_sessions")
}

model AIConversation {
  id          String   @id @default(cuid())
  userId      String
  title       String?
  context     Json?    // Conversation context and metadata
  messageCount Int     @default(0)
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  messages    AIMessage[]
  
  @@map("ai_conversations")
}

model AIMessage {
  id             String         @id @default(cuid())
  conversationId String
  role           String         // user, assistant, system
  content        String
  metadata       Json?          // Token count, model used, etc.
  createdAt      DateTime       @default(now())
  
  conversation   AIConversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  @@map("ai_messages")
}

// Analytics and Metrics
model UserActivity {
  id        String   @id @default(cuid())
  userId    String
  action    String   // login, match_request
  prisma
// Continuing the Prisma schema...

// Analytics and Metrics
model UserActivity {
  id        String   @id @default(cuid())
  userId    String
  action    String   // login, match_request, chat_sent, study_session_joined
  metadata  Json?    // Additional context data
  ipAddress String?
  userAgent String?
  createdAt DateTime @default(now())
  
  @@map("user_activities")
}

model SystemMetrics {
  id        String   @id @default(cuid())
  metric    String   // active_users, matches_made, messages_sent
  value     Float
  period    String   // daily, weekly, monthly
  date      DateTime
  metadata  Json?
  createdAt DateTime @default(now())
  
  @@unique([metric, period, date])
  @@map("system_metrics")
}

// Indexes for performance optimization
@@index([email], map: "users_email_idx")
@@index([phone], map: "users_phone_idx")
@@index([lastSeen], map: "users_last_seen_idx")
@@index([senderId, receiverId], map: "matches_sender_receiver_idx")
@@index([status], map: "matches_status_idx")
@@index([createdAt], map: "matches_created_at_idx")
@@index([chatId, createdAt], map: "messages_chat_created_idx")
@@index([senderId], map: "messages_sender_idx")
@@index([userId, action, createdAt], map: "user_activities_user_action_idx")
2.2 Database Configuration
typescript
// src/config/database.config.ts
import { PrismaClient } from '@prisma/client';
import { logger } from '../utils/logger.util';

let prisma: PrismaClient;

declare global {
  var __prisma: PrismaClient | undefined;
}

if (process.env.NODE_ENV === 'production') {
  prisma = new PrismaClient({
    log: ['error', 'warn'],
    errorFormat: 'minimal',
  });
} else {
  if (!global.__prisma) {
    global.__prisma = new PrismaClient({
      log: ['query', 'info', 'warn', 'error'],
      errorFormat: 'pretty',
    });
  }
  prisma = global.__prisma;
}

export async function connectDatabase(): Promise<void> {
  try {
    await prisma.$connect();
    logger.info('Database connected successfully');
  } catch (error) {
    logger.error('Database connection failed:', error);
    throw error;
  }
}

export async function disconnectDatabase(): Promise<void> {
  await prisma.$disconnect();
}

export { prisma };
2.3 Redis Configuration
typescript
// src/config/redis.config.ts
import Redis from 'redis';
import { logger } from '../utils/logger.util';

const redisClient = Redis.createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379',
  retryDelayOnFailover: 100,
  enableReadyCheck: true,
  lazyConnect: true,
});

redisClient.on('connect', () => {
  logger.info('Redis connected successfully');
});

redisClient.on('error', (error) => {
  logger.error('Redis connection error:', error);
});

export async function connectRedis(): Promise<void> {
  try {
    await redisClient.connect();
  } catch (error) {
    logger.error('Failed to connect to Redis:', error);
    throw error;
  }
}

export { redisClient };
3. Authentication System
3.1 JWT Utility
typescript
// src/utils/jwt.util.ts
import jwt from 'jsonwebtoken';
import { redisClient } from '../config/redis.config';
import { logger } from './logger.util';

interface TokenPayload {
  userId: string;
  email: string;
  role: string;
}

interface TokenPair {
  accessToken: string;
  refreshToken: string;
}

export class JWTService {
  private static ACCESS_TOKEN_SECRET = process.env.JWT_ACCESS_SECRET!;
  private static REFRESH_TOKEN_SECRET = process.env.JWT_REFRESH_SECRET!;
  private static ACCESS_TOKEN_EXPIRES = '15m';
  private static REFRESH_TOKEN_EXPIRES = '7d';

  static generateTokens(payload: TokenPayload): TokenPair {
    const accessToken = jwt.sign(
      payload,
      this.ACCESS_TOKEN_SECRET,
      { expiresIn: this.ACCESS_TOKEN_EXPIRES }
    );

    const refreshToken = jwt.sign(
      payload,
      this.REFRESH_TOKEN_SECRET,
      { expiresIn: this.REFRESH_TOKEN_EXPIRES }
    );

    return { accessToken, refreshToken };
  }

  static verifyAccessToken(token: string): TokenPayload {
    try {
      return jwt.verify(token, this.ACCESS_TOKEN_SECRET) as TokenPayload;
    } catch (error) {
      throw new Error('Invalid access token');
    }
  }

  static verifyRefreshToken(token: string): TokenPayload {
    try {
      return jwt.verify(token, this.REFRESH_TOKEN_SECRET) as TokenPayload;
    } catch (error) {
      throw new Error('Invalid refresh token');
    }
  }

  static async storeRefreshToken(userId: string, refreshToken: string): Promise<void> {
    try {
      const key = `refresh_token:${userId}`;
      await redisClient.setEx(key, 7 * 24 * 60 * 60, refreshToken); // 7 days
    } catch (error) {
      logger.error('Failed to store refresh token:', error);
      throw error;
    }
  }

  static async validateRefreshToken(userId: string, refreshToken: string): Promise<boolean> {
    try {
      const key = `refresh_token:${userId}`;
      const storedToken = await redisClient.get(key);
      return storedToken === refreshToken;
    } catch (error) {
      logger.error('Failed to validate refresh token:', error);
      return false;
    }
  }

  static async revokeRefreshToken(userId: string): Promise<void> {
    try {
      const key = `refresh_token:${userId}`;
      await redisClient.del(key);
    } catch (error) {
      logger.error('Failed to revoke refresh token:', error);
    }
  }
}
3.2 Authentication Middleware
typescript
// src/middleware/auth.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { JWTService } from '../utils/jwt.util';
import { UserService } from '../services/user.service';
import { ApiError } from '../utils/apiError.util';

interface AuthRequest extends Request {
  user?: {
    userId: string;
    email: string;
    role: string;
  };
}

export const authenticateToken = async (
  req: AuthRequest,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
      throw new ApiError(401, 'Access token required');
    }

    const payload = JWTService.verifyAccessToken(token);
    
    // Verify user still exists and is active
    const user = await UserService.findById(payload.userId);
    if (!user || !user.isActive) {
      throw new ApiError(401, 'User not found or inactive');
    }

    req.user = payload;
    next();
  } catch (error) {
    next(error);
  }
};

export const authorize = (roles: string[]) => {
  return (req: AuthRequest, res: Response, next: NextFunction): void => {
    try {
      if (!req.user) {
        throw new ApiError(401, 'Authentication required');
      }

      if (!roles.includes(req.user.role)) {
        throw new ApiError(403, 'Insufficient permissions');
      }

      next();
    } catch (error) {
      next(error);
    }
  };
};
3.3 Authentication Service
typescript
// src/services/auth.service.ts
import bcrypt from 'bcryptjs';
import { prisma } from '../config/database.config';
import { JWTService } from '../utils/jwt.util';
import { ApiError } from '../utils/apiError.util';
import { OTPService } from './otp.service';
import { EmailService } from './email.service';

interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role?: 'STUDENT' | 'TEACHER' | 'INSTITUTION';
}

interface LoginData {
  email: string;
  password: string;
}

export class AuthService {
  static async register(data: RegisterData) {
    const { email, password, firstName, lastName, role = 'STUDENT' } = data;

    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email }
    });

    if (existingUser) {
      throw new ApiError(400, 'User already exists with this email');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12);

    // Create user with profile
    const user = await prisma.user.create({
      data: {
        email,
        password: hashedPassword,
        role,
        profile: {
          create: {
            firstName,
            lastName,
          }
        }
      },
      include: {
        profile: true
      }
    });

    // Send verification email
    const verificationToken = await OTPService.generateEmailVerificationToken(user.id);
    await EmailService.sendVerificationEmail(email, verificationToken);

    // Generate tokens
    const tokens = JWTService.generateTokens({
      userId: user.id,
      email: user.email,
      role: user.role
    });

    // Store refresh token
    await JWTService.storeRefreshToken(user.id, tokens.refreshToken);

    return {
      user: {
        id: user.id,
        email: user.email,
        role: user.role,
        isVerified: user.isVerified,
        profile: user.profile
      },
      tokens
    };
  }

  static async login(data: LoginData) {
    const { email, password } = data;

    // Find user with profile
    const user = await prisma.user.findUnique({
      where: { email },
      include: { profile: true }
    });

    if (!user || !user.password) {
      throw new ApiError(401, 'Invalid credentials');
    }

    // Verify password
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      throw new ApiError(401, 'Invalid credentials');
    }

    // Check if user is active
    if (!user.isActive) {
      throw new ApiError(403, 'Account is deactivated');
    }

    // Update last seen
    await prisma.user.update({
      where: { id: user.id },
      data: { lastSeen: new Date() }
    });

    // Generate tokens
    const tokens = JWTService.generateTokens({
      userId: user.id,
      email: user.email,
      role: user.role
    });

    // Store refresh token
    await JWTService.storeRefreshToken(user.id, tokens.refreshToken);

    return {
      user: {
        id: user.id,
        email: user.email,
        role: user.role,
        isVerified: user.isVerified,
        profile: user.profile
      },
      tokens
    };
  }

  static async refreshToken(refreshToken: string) {
    try {
      const payload = JWTService.verifyRefreshToken(refreshToken);
      
      // Validate refresh token in Redis
      const isValidToken = await JWTService.validateRefreshToken(
        payload.userId, 
        refreshToken
      );

      if (!isValidToken) {
        throw new ApiError(401, 'Invalid refresh token');
      }

      // Verify user still exists
      const user = await prisma.user.findUnique({
        where: { id: payload.userId }
      });

      if (!user || !user.isActive) {
        throw new ApiError(401, 'User not found or inactive');
      }

      // Generate new tokens
      const tokens = JWTService.generateTokens({
        userId: user.id,
        email: user.email,
        role: user.role
      });

      // Store new refresh token
      await JWTService.storeRefreshToken(user.id, tokens.refreshToken);

      return tokens;
    } catch (error) {
      throw new ApiError(401, 'Invalid refresh token');
    }
  }

  static async logout(userId: string) {
    // Revoke refresh token
    await JWTService.revokeRefreshToken(userId);
    
    return { message: 'Logged out successfully' };
  }

  static async verifyEmail(token: string) {
    const userId = await OTPService.verifyEmailVerificationToken(token);
    
    await prisma.user.update({
      where: { id: userId },
      data: { isVerified: true }
    });

    return { message: 'Email verified successfully' };
  }

  static async requestPasswordReset(email: string) {
    const user = await prisma.user.findUnique({
      where: { email }
    });

    if (!user) {
      // Don't reveal if email exists
      return { message: 'If the email exists, a reset link has been sent' };
    }

    const resetToken = await OTPService.generatePasswordResetToken(user.id);
    await EmailService.sendPasswordResetEmail(email, resetToken);

    return { message: 'If the email exists, a reset link has been sent' };
  }

  static async resetPassword(token: string, newPassword: string) {
    const userId = await OTPService.verifyPasswordResetToken(token);
    
    const hashedPassword = await bcrypt.hash(newPassword, 12);
    
    await prisma.user.update({
      where: { id: userId },
      data: { password: hashedPassword }
    });

    // Revoke all refresh tokens
    await JWTService.revokeRefreshToken(userId);

    return { message: 'Password reset successfully' };
  }
}
3.4 Authentication Routes
typescript
// src/routes/auth.routes.ts
import { Router } from 'express';
import { AuthController } from '../controllers/auth.controller';
import { validateRequest } from '../middleware/validation.middleware';
import { authValidationSchemas } from '../validators/auth.validators';
import { rateLimit } from 'express-rate-limit';

const router = Router();

// Rate limiting for auth routes
const authRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  message: { error: 'Too many authentication attempts, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});

const registerRateLimit = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 3, // 3 registrations per hour
  message: { error: 'Too many registration attempts, please try again later' },
});

router.post('/register', 
  registerRateLimit,
  validateRequest(authValidationSchemas.register),
  AuthController.register
);

router.post('/login',
  authRateLimit,
  validateRequest(authValidationSchemas.login),
  AuthController.login
);

router.post('/refresh',
  validateRequest(authValidationSchemas.refreshToken),
  AuthController.refreshToken
);

router.post('/logout',
  AuthController.logout
);

router.post('/verify-email',
  validateRequest(authValidationSchemas.verifyEmail),
  AuthController.verifyEmail
);

router.post('/request-password-reset',
  authRateLimit,
  validateRequest(authValidationSchemas.requestPasswordReset),
  AuthController.requestPasswordReset
);

router.post('/reset-password',
  authRateLimit,
  validateRequest(authValidationSchemas.resetPassword),
  AuthController.resetPassword
);

export default router;
3.5 Authentication Controller
typescript
// src/controllers/auth.controller.ts
import { Request, Response, NextFunction } from 'express';
import { AuthService } from '../services/auth.service';
import { ApiResponse } from '../utils/apiResponse.util';
import { logger } from '../utils/logger.util';

export class AuthController {
  static async register(req: Request, res: Response, next: NextFunction) {
    try {
      const result = await AuthService.register(req.body);
      
      logger.info(`User registered: ${req.body.email}`);
      
      ApiResponse.success(res, result, 'Registration successful', 201);
    } catch (error) {
      next(error);
    }
  }

  static async login(req: Request, res: Response, next: NextFunction) {
    try {
      const result = await AuthService.login(req.body);
      
      // Set refresh token as httpOnly cookie
      res.cookie('refreshToken', result.tokens.refreshToken, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite:

        