export type Project = {
  name: string;
  description: string;
  shortDescription?: string;
  liveDemo?: string;
  sourceCode?: string;
  techStack?: string[];
  detailedDescription?: string;
  link: string;
  category: 'AI/ML' | 'Web' | 'Data' | 'Other';
};

export const projects: Project[] = [
  {
    name: 'Shiksha-Mitra',
    shortDescription: 'A collaborative learning and acknowledgement platform for career and educational growth through community-driven support.',
    description:
      'Shiksha-Mitra is a collaborative learning and acknowledgement platform designed to help peers support and recognize each other\'s growth in career and education. It provides an ecosystem where learners, professionals, and mentors can exchange resources, acknowledge progress, and celebrate milestones. The project emphasizes community-driven growth, building a culture of appreciation and collective success in the academic and professional journey.',
    liveDemo: 'https://shiksha-mitra.vercel.app/',
    sourceCode: 'https://github.com/ayushrai-hub/Shiksha-Mitra',
    techStack: [
      'Next.js',
      'React',
      'TypeScript',
      'Tailwind CSS',
      'Serverless Functions',
      'Firebase',
      'MongoDB',
      'Vercel',
    ],
    detailedDescription:
      'Shiksha-Mitra is a collaborative learning and acknowledgement platform designed to help peers support and recognize each other\'s growth in career and education. It provides an ecosystem where learners, professionals, and mentors can exchange resources, acknowledge progress, and celebrate milestones. The project emphasizes community-driven growth, building a culture of appreciation and collective success in the academic and professional journey.',
    link: 'https://shiksha-mitra.vercel.app/',
    category: 'Web',
  },
  {
    name: 'Expert-O',
    shortDescription: 'A visionary collective of polymaths blending technology, design, strategy, and AI-driven workflows for transformative digital solutions.',
    description:
      'Expert-O is a visionary collective of polymaths in India that blends technology, design, strategy, and AI-driven workflows to deliver transformative digital solutions. It positions itself as an elite tribe of multi-disciplinary innovators who execute 5x faster by leveraging AI augmentation and cross-domain expertise. The platform showcases their mission, values, services, portfolio, pricing models, thought leadership, and recruitment process, with a goal to reshape India\'s digital future.',
    liveDemo: 'https://expert-o.vercel.app/',
    techStack: [
      'Next.js',
      'React',
      'TypeScript',
      'Tailwind CSS',
      'Framer Motion',
      'Three.js',
      'Vercel',
    ],
    detailedDescription:
      'Expert-O is a visionary collective of polymaths in India that blends technology, design, strategy, and AI-driven workflows to deliver transformative digital solutions. It positions itself as an elite tribe of multi-disciplinary innovators who execute 5x faster by leveraging AI augmentation and cross-domain expertise. The platform showcases their mission, values, services, portfolio, pricing models, thought leadership, and recruitment process, with a goal to reshape India\'s digital future. 👉 In short: Expert-O is a polymath-driven digital innovation studio, combining AI, technology, and systemic thinking to accelerate India\'s growth through impactful projects and visionary execution.',
    link: 'https://expert-o.vercel.app/',
    category: 'Web',
  },
  {
    name: 'Ihabyhimani',
    description: 'A tool to analyze large datasets and generate insights.',
    link: '#',
    category: 'Data',
  },
  {
    name: 'Dynamic Portfolio Website',
    shortDescription:
      'A modern single-page portfolio website to showcase expertise in Generative AI, Web Development, and Data Science.',
    description:
      'A modern single-page portfolio website designed to showcase my expertise in Generative AI, Web Development, and Data Science. Built with Next.js, React, TypeScript, and Tailwind CSS, the project includes interactive sections for projects, skills, experience, research, and a dynamic resume. It integrates a serverless contact form, Headless CMS, and Google Analytics 4, and is deployed on Vercel with CI/CD, SEO optimization, and full mobile responsiveness.',
    liveDemo: 'https://ayush-rai-work.vercel.app/',
    sourceCode: 'https://github.com/ayushrai-hub/ayush.me',
    techStack: [
      'Next.js',
      'React',
      'TypeScript',
      'Tailwind CSS',
      'Serverless Functions',
      'Headless CMS',
      'Google Analytics 4',
      'Vercel',
    ],
    detailedDescription:
      'This comprehensive portfolio website represents the culmination of modern web development practices combined with cutting-edge technology. The site features a fully responsive design optimized for all devices, with SEO-friendly implementation including structured data markup. Key features include dynamic content management through headless CMS integration, real-time analytics via Google Analytics 4, and optimized performance through Vercel\'s edge deployment. The contact form leverages serverless functions for secure, fast processing without backend infrastructure.',
    link: 'https://ayush-rai-work.vercel.app/',
    category: 'Web',
  },
];
