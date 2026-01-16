export type ExperienceItem = {
  type: 'work' | 'education';
  title: string;
  subtitle: string;
  date: string;
  description: string;
};

export const experience: ExperienceItem[] = [
  {
    type: 'work',
    title: 'Software Engineer',
    subtitle: 'Google, Remote',
    date: '2020 - present',
    description:
      'Creative Direction, User Experience, Visual Design, Project Management, Team Leading',
  },
  {
    type: 'work',
    title: 'Full Stack Developer',
    subtitle: 'Facebook, Menlo Park, CA',
    date: '2018 - 2020',
    description:
      'Creative Direction, User Experience, Visual Design, Project Management, Team Leading',
  },
  {
    type: 'education',
    title: 'Content Marketing for Web, Mobile and Social Media',
    subtitle: 'Online Course',
    date: 'April 2013',
    description: 'Strategy, Social Media',
  },
];
