/**
 * Test setup file for Vitest
 * 
 * Configures test environment and global mocks
 */

import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Extend Vitest's expect with custom matchers if needed
// Example: expect.extend(customMatchers)
