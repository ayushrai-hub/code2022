/**
 * Tests for portfolio data files
 * 
 * Tests data structure, validation, and type safety for portfolio data.
 */

import { describe, it, expect } from 'vitest'

// Note: These tests assume the data files export named exports
// Adjust imports based on actual export structure

describe('Portfolio Data Tests', () => {
  describe('Projects Data', () => {
    it('should have valid project structure', async () => {
      // Import projects data
      const { projects } = await import('../src/data/projects')
      
      // Verify projects is an array
      expect(Array.isArray(projects)).toBe(true)
      expect(projects.length).toBeGreaterThan(0)
      
      // Verify each project has required fields
      projects.forEach((project: any) => {
        expect(project).toHaveProperty('name')
        expect(project).toHaveProperty('description')
        expect(project).toHaveProperty('link')
        expect(project).toHaveProperty('category')
        
        // Validate types
        expect(typeof project.name).toBe('string')
        expect(typeof project.description).toBe('string')
        expect(typeof project.link).toBe('string')
        expect(['AI/ML', 'Web', 'Data', 'Other']).toContain(project.category)
        
        // Validate optional fields
        if (project.techStack) {
          expect(Array.isArray(project.techStack)).toBe(true)
        }
        if (project.liveDemo) {
          expect(typeof project.liveDemo).toBe('string')
        }
        if (project.sourceCode) {
          expect(typeof project.sourceCode).toBe('string')
        }
      })
    })
    
    it('should have unique project names', async () => {
      const { projects } = await import('../src/data/projects')
      const names = projects.map((p: any) => p.name)
      const uniqueNames = new Set(names)
      expect(names.length).toBe(uniqueNames.size)
    })
    
    it('should have valid URLs for links', async () => {
      const { projects } = await import('../src/data/projects')
      projects.forEach((project: any) => {
        if (project.link) {
          expect(() => new URL(project.link)).not.toThrow()
        }
        if (project.liveDemo) {
          expect(() => new URL(project.liveDemo)).not.toThrow()
        }
        if (project.sourceCode) {
          expect(() => new URL(project.sourceCode)).not.toThrow()
        }
      })
    })
  })
  
  describe('Skills Data', () => {
    it('should have valid skills structure', async () => {
      const { skills } = await import('../src/data/skills')
      
      expect(Array.isArray(skills)).toBe(true)
      
      skills.forEach((skill: any) => {
        expect(skill).toHaveProperty('name')
        expect(typeof skill.name).toBe('string')
        
        if (skill.level) {
          expect(typeof skill.level).toBe('number')
          expect(skill.level).toBeGreaterThanOrEqual(0)
          expect(skill.level).toBeLessThanOrEqual(100)
        }
      })
    })
  })
  
  describe('Experience Data', () => {
    it('should have valid experience structure', async () => {
      const { experience } = await import('../src/data/experience')
      
      expect(Array.isArray(experience)).toBe(true)
      
      experience.forEach((exp: any) => {
        expect(exp).toHaveProperty('company')
        expect(exp).toHaveProperty('role')
        expect(typeof exp.company).toBe('string')
        expect(typeof exp.role).toBe('string')
      })
    })
  })
  
  describe('About Data', () => {
    it('should have valid about structure', async () => {
      const { aboutData } = await import('../src/data/about')
      
      expect(aboutData).toHaveProperty('hero')
      expect(aboutData).toHaveProperty('bio')
      expect(Array.isArray(aboutData.bio)).toBe(true)
      
      expect(aboutData.hero).toHaveProperty('headline')
      expect(aboutData.hero).toHaveProperty('tagline')
    })
  })
})
