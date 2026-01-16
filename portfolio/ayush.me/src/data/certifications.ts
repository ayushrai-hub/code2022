export type Certification = {
  name: string;
  organization: string;
  date: string;
  url?: string;
};

export const certifications: Certification[] = [
  {
    name: 'AWS Certified Machine Learning Specialist',
    organization: 'Amazon Web Services',
    date: '2023',
  },
  {
    name: 'Google Cloud Certified Professional Data Engineer',
    organization: 'Google Cloud',
    date: '2022',
  },
  {
    name: 'Microsoft Certified Azure AI Engineer',
    organization: 'Microsoft',
    date: '2021',
  },
];
