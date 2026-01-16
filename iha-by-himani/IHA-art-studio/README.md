# IHA Art Studio

An art studio application built with React and TypeScript.

## Overview

IHA Art Studio is a web application for showcasing and managing art-related content. The application provides features for displaying artwork, managing art collections, and potentially art creation tools.

## Technology Stack

- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Build Tool** - Likely Vite or Create React App
- **React Icons** - Icon library

## Project Structure

```
IHA-art-studio/
├── src/
│   ├── components/        # React components
│   ├── pages/             # Page components
│   ├── assets/            # Images and media
│   ├── styles/            # CSS/styling files
│   └── App.tsx            # Main app component
├── public/                # Static assets
├── package.json
└── README.md
```

## Status

⚠️ **Note:** Source code structure needs verification. Only `node_modules` is currently visible.

## Expected Features

Based on the project name, this application likely includes:
- Art gallery/portfolio display
- Artwork management
- Possibly art creation tools
- User interactions (likes, comments, etc.)
- Responsive design for art viewing

## Setup (When Source Code is Available)

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
cd iha-by-himani/IHA-art-studio
npm install
```

### Development

```bash
npm run dev
# or
npm start
```

### Build

```bash
npm run build
```

## Development Guidelines

- Use TypeScript for type safety
- Follow React best practices
- Keep components modular
- Optimize images for web
- Ensure responsive design
- Add loading states for images

## Next Steps

1. **If this is a new project:**
   - Set up React + TypeScript project structure
   - Create component architecture
   - Implement art gallery features
   - Add image optimization
   - Create this README

2. **If source code exists elsewhere:**
   - Locate the source files
   - Move them to this directory
   - Update this README with actual structure
   - Document features and usage

## Dependencies (Expected)

- `react` - React library
- `react-dom` - React DOM rendering
- `typescript` - TypeScript compiler
- `react-icons` - Icon library (already in node_modules)
- Build tool (Vite, CRA, or similar)

## Features to Implement

- [ ] Art gallery with grid/list views
- [ ] Image lightbox/modal
- [ ] Art filtering/categorization
- [ ] Responsive image loading
- [ ] Artwork details page
- [ ] Search functionality
- [ ] Social sharing
- [ ] Contact form

## Performance Considerations

- Optimize images (WebP format, lazy loading)
- Implement virtual scrolling for large galleries
- Use image CDN if applicable
- Minimize bundle size
- Implement code splitting

## Testing

Tests should cover:
- Component rendering
- Image loading
- User interactions
- Responsive behavior

```bash
npm test
```

## Deployment

Deploy to:
- Vercel (recommended for React apps)
- Netlify
- GitHub Pages
- Any static hosting service

---

**Last Updated:** 2025-01-16  
**Status:** Source code structure needs verification
