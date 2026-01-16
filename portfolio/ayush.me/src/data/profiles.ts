export type Profile = {
  name: string;
  url: string;
  icon: string;
  domain: 'development' | 'design' | 'data-science' | 'writing' | 'professional' | 'social' | 'portfolio';
  category: string;
  description: string;
};

export const profiles: Profile[] = [
  // Development & Coding
  {
    name: 'GitHub',
    url: 'https://github.com/ayushrai-hub',
    icon: 'github',
    domain: 'development',
    category: 'Code Hosting',
    description: 'Explore my open-source projects and contributions',
  },
  {
    name: 'LeetCode',
    url: 'https://leetcode.com/ayushrai0211',
    icon: 'code',
    domain: 'development',
    category: 'Coding Practice',
    description: 'Check out my problem-solving skills and solutions',
  },
  {
    name: 'Unstop',
    url: 'https://unstop.com/u/ayushrai4939',
    icon: 'award',
    domain: 'development',
    category: 'Competitions',
    description: 'View my participation in coding competitions',
  },

  // Data Science & Analytics
  {
    name: 'Kaggle',
    url: 'https://www.kaggle.com/ayushrai02',
    icon: 'bar-chart-2',
    domain: 'data-science',
    category: 'Data Science',
    description: 'Explore my data science projects and notebooks',
  },
  {
    name: 'Data Science Portfolio',
    url: 'https://www.datascienceportfol.io/ayushrai0211',
    icon: 'database',
    domain: 'data-science',
    category: 'Portfolio',
    description: 'My curated data science projects and case studies',
  },
  {
    name: 'Hugging Face',
    url: 'https://huggingface.co/ayushrai02',
    icon: 'robot',
    domain: 'data-science',
    category: 'AI/ML Models',
    description: 'Check out my AI models and contributions on Hugging Face',
  },

  // Design & Creative
  {
    name: 'Behance',
    url: 'https://www.behance.net/ayushrai17',
    icon: 'image',
    domain: 'design',
    category: 'Design Portfolio',
    description: 'View my creative design projects and artwork',
  },
  {
    name: 'Dribbble',
    url: 'https://dribbble.com/ayushrai',
    icon: 'droplet',
    domain: 'design',
    category: 'UI/UX Design',
    description: 'Check out my UI/UX design projects',
  },

  // Writing & Content
  {
    name: 'Medium',
    url: 'https://medium.com/@ayushrai0211',
    icon: 'book-open',
    domain: 'writing',
    category: 'Technical Blog',
    description: 'Read my technical articles and stories',
  },
  {
    name: 'Blogger',
    url: 'https://ayushrai02.blogspot.com/',
    icon: 'edit-3',
    domain: 'writing',
    category: 'Personal Blog',
    description: 'My personal thoughts and experiences',
  },

  // Professional Networks
  {
    name: 'LinkedIn',
    url: 'https://www.linkedin.com/in/ayushrai02/',
    icon: 'linkedin',
    domain: 'professional',
    category: 'Professional Network',
    description: 'Connect with me professionally',
  },
  {
    name: 'Salesforce Trailblazer',
    url: 'https://www.salesforce.com/trailblazer/ayushr02',
    icon: 'cloud',
    domain: 'professional',
    category: 'Certifications',
    description: 'My Salesforce certifications and badges',
  },
  {
    name: 'Upwork',
    url: 'https://upwork.com/freelancers/ayushrai',
    icon: 'briefcase',
    domain: 'professional',
    category: 'Freelance',
    description: 'Hire me for development projects',
  },

  // Portfolio & Personal Sites
  {
    name: 'Notion Portfolio',
    url: 'https://www.notion.so/Ayush-s-Portfolio-5d069b2fa8b64d7e8b939a0c9b946e7b',
    icon: 'layout-grid',
    domain: 'portfolio',
    category: 'Digital Portfolio',
    description: 'My comprehensive work portfolio',
  },
  {
    name: 'Super Site',
    url: 'https://ayush-rai.super.site/',
    icon: 'globe',
    domain: 'portfolio',
    category: 'Personal Website',
    description: 'My personal website and blog',
  },
  {
    name: 'Linktree',
    url: 'https://linktr.ee/ayush_rai02',
    icon: 'link',
    domain: 'portfolio',
    category: 'Link Hub',
    description: 'All my important links in one place',
  },

  // Social Media
  {
    name: 'Twitter / X',
    url: 'https://x.com/AyushRai0211',
    icon: 'twitter',
    domain: 'social',
    category: 'Microblogging',
    description: 'Follow me for updates and thoughts',
  },
  {
    name: 'Instagram',
    url: 'https://www.instagram.com/ayush_rai02/',
    icon: 'instagram',
    domain: 'social',
    category: 'Photos & Stories',
    description: 'See my personal moments and stories',
  },
  {
    name: 'Facebook',
    url: 'https://www.facebook.com/people/Ayush-Rai/pfbid02ha7vx1uEQ8tgakypf3A5U7uzpgJykuEVQffwPPqy9BnLhmz1g4aTeE93SdFuAvH1l/',
    icon: 'facebook',
    domain: 'social',
    category: 'Social Network',
    description: 'Connect with me on Facebook',
  },
];

export const domains = [
  {
    id: 'development',
    name: 'Development',
    description: 'Code repositories, competitive programming, and development profiles',
    icon: 'code',
    color: 'from-blue-500 to-blue-600',
  },
  {
    id: 'data-science',
    name: 'Data Science',
    description: 'Data analysis, machine learning, and data visualization work',
    icon: 'bar-chart-2',
    color: 'from-purple-500 to-pink-500',
  },
  {
    id: 'design',
    name: 'Design',
    description: 'UI/UX design, graphics, and creative work',
    icon: 'palette',
    color: 'from-pink-500 to-rose-500',
  },
  {
    id: 'writing',
    name: 'Writing',
    description: 'Blogs, articles, and technical writing',
    icon: 'edit-3',
    color: 'from-green-500 to-teal-500',
  },
  {
    id: 'professional',
    name: 'Professional',
    description: 'Networking, certifications, and career profiles',
    icon: 'briefcase',
    color: 'from-amber-500 to-orange-500',
  },
  {
    id: 'portfolio',
    name: 'Portfolio',
    description: 'My work showcases and personal websites',
    icon: 'layout-grid',
    color: 'from-indigo-500 to-purple-500',
  },
  {
    id: 'social',
    name: 'Social Media',
    description: 'Connect with me on various social platforms',
    icon: 'users',
    color: 'from-rose-500 to-pink-500',
  },
];
