export type Skill = {
  name: string;
  category: 'Frontend' | 'Backend' | 'AI/ML' | 'Cloud/DevOps' | 'Tools/Other';
  level: number; // 1-100
};

export const skills: Skill[] = [
  // Frontend
  { name: 'JavaScript', category: 'Frontend', level: 95 },
  { name: 'TypeScript', category: 'Frontend', level: 90 },
  { name: 'React', category: 'Frontend', level: 95 },
  { name: 'Vite', category: 'Frontend', level: 85 },
  { name: 'Tailwind CSS', category: 'Frontend', level: 90 },

  // Backend
  { name: 'Node.js', category: 'Backend', level: 85 },
  { name: 'Express', category: 'Backend', level: 80 },
  { name: 'Python', category: 'Backend', level: 75 },
  { name: 'GraphQL', category: 'Backend', level: 70 },
  { name: 'PostgreSQL', category: 'Backend', level: 80 },
  { name: 'MongoDB', category: 'Backend', level: 75 },

  // AI/ML
  { name: 'Machine Learning', category: 'AI/ML', level: 90 },
  { name: 'Deep Learning', category: 'AI/ML', level: 85 },
  { name: 'NLP', category: 'AI/ML', level: 80 },
  { name: 'Computer Vision', category: 'AI/ML', level: 75 },

  // Cloud/DevOps
  { name: 'Docker', category: 'Cloud/DevOps', level: 85 },
  { name: 'Kubernetes', category: 'Cloud/DevOps', level: 70 },
  { name: 'AWS', category: 'Cloud/DevOps', level: 80 },
  { name: 'Azure', category: 'Cloud/DevOps', level: 75 },
  { name: 'GCP', category: 'Cloud/DevOps', level: 70 },

  // Tools/Other
  { name: 'Git', category: 'Tools/Other', level: 95 },
  { name: 'Jest', category: 'Tools/Other', level: 85 },
  { name: 'Linux', category: 'Tools/Other', level: 80 },
];
