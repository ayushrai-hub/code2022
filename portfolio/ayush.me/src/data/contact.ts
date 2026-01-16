export const contactData = {
  header: {
    title: "Let's Connect & Collaborate",
    description: "Whether you're an employer, collaborator, student, or just someone curious — I'd love to hear from you."
  },
  contactInfo: {
    address: "Bhopal, Madhya Pradesh, India",
    phone: "+91 74405 67944",
    email: "ayushrai0211@gmail.com",
    socials: [
      { name: "LinkedIn", url: "https://linkedin.com/in/ayushrai02", icon: "linkedin" },
      { name: "GitHub", url: "https://github.com/ayushrai-hub", icon: "github" },
      { name: "Twitter", url: "https://x.com/AyushRai0211", icon: "twitter" },
      { name: "Instagram", url: "https://instagram.com/ayush_rai02", icon: "instagram" }
    ]
  },
  form: {
    fields: [
      {
        name: "name",
        type: "text",
        label: "Full Name",
        required: true,
        placeholder: "Enter your full name"
      },
      {
        name: "email",
        type: "email",
        label: "Email",
        required: true,
        placeholder: "your.email@example.com"
      },
      {
        name: "phone",
        type: "tel",
        label: "Phone Number",
        required: false,
        placeholder: "+91 12345 67890"
      },
      {
        name: "organization",
        type: "text",
        label: "Organization (Optional)",
        required: false,
        placeholder: "Your company or institution"
      },
      {
        name: "contactType",
        type: "select",
        label: "How can I help you?",
        required: true,
        options: [
          { value: "hire", label: "Hire Me" },
          { value: "freelance", label: "Freelance/Contract Work" },
          { value: "consultancy", label: "Consultancy" },
          { value: "collaboration", label: "Collaboration" },
          { value: "other", label: "Other" }
        ]
      },
      {
        name: "message",
        type: "textarea",
        label: "Your Message",
        required: true,
        placeholder: "How can I help you?"
      }
    ],
    submitText: "Send Message",
    successMessage: "Thanks for reaching out! I'll get back to you soon.",
    errorMessage: "There was an error sending your message. Please try again later."
  }
};

export type ContactData = typeof contactData;
