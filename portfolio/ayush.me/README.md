# Portfolio Website - ayush.me

A modern, responsive personal portfolio website built with React, TypeScript, and Vite.

## Overview

This portfolio website showcases personal projects, skills, experience, certifications, and contact information. Built with modern web technologies for optimal performance and user experience.

## Technology Stack

- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** (likely) - Styling
- **Lucide React** - Icons

## Project Structure

```
portfolio/ayush.me/
├── src/
│   ├── data/              # Data files
│   │   ├── about.ts       # Personal information
│   │   ├── projects.ts    # Project listings
│   │   ├── skills.ts      # Skills and technologies
│   │   ├── experience.ts  # Work experience
│   │   ├── certifications.ts # Certifications
│   │   ├── contact.ts     # Contact information
│   │   └── profiles.ts    # Social profiles
│   ├── components/        # React components (if exists)
│   ├── pages/             # Page components (if exists)
│   └── App.tsx            # Main app component
├── public/                # Static assets
├── package.json
├── vite.config.ts
└── README.md
```

## Features

- **Project Showcase**: Display personal projects with descriptions, tech stacks, and links
- **Skills Display**: Showcase technical skills and competencies
- **Experience Timeline**: Professional experience and achievements
- **Certifications**: Educational and professional certifications
- **Contact Information**: Multiple ways to get in touch
- **Responsive Design**: Works on all device sizes
- **Modern UI/UX**: Clean, professional design

## Setup

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
cd portfolio/ayush.me
npm install
```

### Development

```bash
npm run dev
```

The application will be available at `http://localhost:5173` (or the port Vite assigns).

### Build

```bash
npm run build
```

Build output will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Data Structure

### Projects
Projects are defined in `src/data/projects.ts` with the following structure:
```typescript
{
  name: string;
  description: string;
  shortDescription?: string;
  liveDemo?: string;
  sourceCode?: string;
  techStack?: string[];
  detailedDescription?: string;
  link: string;
  category: 'AI/ML' | 'Web' | 'Data' | 'Other';
}
```

### Skills
Skills are defined in `src/data/skills.ts` with categories and proficiency levels.

### Experience
Work experience entries with company, role, duration, and achievements.

## Customization

### Updating Content

1. **Projects**: Edit `src/data/projects.ts`
2. **Skills**: Edit `src/data/skills.ts`
3. **Experience**: Edit `src/data/experience.ts`
4. **About**: Edit `src/data/about.ts`
5. **Contact**: Edit `src/data/contact.ts`
6. **Certifications**: Edit `src/data/certifications.ts`

### Styling

- Modify component styles or global CSS
- Update theme colors and fonts
- Customize layout and spacing

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Configure build settings:
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Deploy

### Other Platforms

The built `dist/` folder can be deployed to:
- Netlify
- GitHub Pages
- Any static hosting service

## Development Guidelines

- Use TypeScript for type safety
- Follow React best practices
- Keep components modular and reusable
- Maintain consistent code style
- Add comments for complex logic

## Testing

Tests should be added for:
- Component rendering
- Data validation
- User interactions
- Responsive design

```bash
npm test
```

## Performance Optimization

- Code splitting for routes
- Lazy loading for images
- Optimize bundle size
- Use React.memo for expensive components
- Implement virtual scrolling for long lists

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Future Improvements

- [ ] Add animations (Framer Motion)
- [ ] Add dark mode
- [ ] Add blog section
- [ ] Add project filtering
- [ ] Add search functionality
- [ ] Add analytics
- [ ] Improve SEO
- [ ] Add PWA support

## License

[Add license information]

## Contact

For questions or suggestions, see contact information in the portfolio.

---

**Last Updated:** 2025-01-16
