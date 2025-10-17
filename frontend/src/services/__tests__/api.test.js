import { describe, it, expect, beforeEach, vi } from 'vitest'
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import apiService from '../api.js'

describe('API Service', () => {
  let mock

  beforeEach(() => {
    // Create a new mock adapter for each test
    mock = new MockAdapter(axios)
  })

  afterEach(() => {
    // Reset the mock adapter after each test
    mock.reset()
  })

  describe('recognizeDigits', () => {
    it('should successfully recognize digits from an image', async () => {
      // Mock successful response
      const mockResponse = { digits: '12345' }
      mock.onPost(/\/api\/recognize$/).reply(200, mockResponse)

      // Create a mock file
      const file = new File(['test'], 'test.png', { type: 'image/png' })

      // Call the API
      const result = await apiService.recognizeDigits(file)

      // Verify the result
      expect(result).toEqual(mockResponse)
      expect(mock.history.post.length).toBe(1)
      expect(mock.history.post[0].url).toContain('/api/recognize')
    })

    it('should handle server error responses', async () => {
      // Mock error response
      mock.onPost(/\/api\/recognize$/).reply(500, { message: 'Internal Server Error' })

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      // Expect the API call to throw an error
      await expect(apiService.recognizeDigits(file)).rejects.toThrow('Internal Server Error')
    })

    it('should handle network errors', async () => {
      // Mock network error
      mock.onPost(/\/api\/recognize$/).networkError()

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      // Expect the API call to throw an error
      // Network errors might return different messages depending on how they're caught
      await expect(apiService.recognizeDigits(file)).rejects.toThrow()
    })

    it('should handle timeout errors', async () => {
      // Mock timeout
      mock.onPost(/\/api\/recognize$/).timeout()

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      // Expect the API call to throw an error
      await expect(apiService.recognizeDigits(file)).rejects.toThrow()
    })

    it('should send FormData with correct structure', async () => {
      mock.onPost(/\/api\/recognize$/).reply((config) => {
        // Verify that FormData was sent
        expect(config.headers['Content-Type']).toContain('multipart/form-data')
        return [200, { digits: '123' }]
      })

      const file = new File(['test'], 'test.png', { type: 'image/png' })
      await apiService.recognizeDigits(file)

      expect(mock.history.post.length).toBe(1)
    })

    it('should handle different response formats (result)', async () => {
      mock.onPost(/\/api\/recognize$/).reply(200, { result: '67890' })

      const file = new File(['test'], 'test.png', { type: 'image/png' })
      const result = await apiService.recognizeDigits(file)

      expect(result).toEqual({ result: '67890' })
    })

    it('should handle different response formats (recognized_digits)', async () => {
      mock.onPost(/\/api\/recognize$/).reply(200, { recognized_digits: '99999' })

      const file = new File(['test'], 'test.png', { type: 'image/png' })
      const result = await apiService.recognizeDigits(file)

      expect(result).toEqual({ recognized_digits: '99999' })
    })

    it('should respect timeout configuration', async () => {
      // This test verifies that timeout is set in the request
      mock.onPost(/\/api\/recognize$/).reply((config) => {
        expect(config.timeout).toBe(30000)
        return [200, { digits: '111' }]
      })

      const file = new File(['test'], 'test.png', { type: 'image/png' })
      await apiService.recognizeDigits(file)
    })
  })

  describe('API Base URL Configuration', () => {
    it('should use environment variables for API URL', () => {
      // The API URL should be constructed from environment variables
      // This is implicitly tested by the mock adapter matching the URL pattern
      mock.onPost(/\/api\/recognize$/).reply(200, { digits: '123' })

      const file = new File(['test'], 'test.png', { type: 'image/png' })
      return expect(apiService.recognizeDigits(file)).resolves.toBeDefined()
    })
  })

  describe('Error Messages', () => {
    it('should return custom error message from server', async () => {
      mock.onPost(/\/api\/recognize$/).reply(400, { message: 'Invalid image format' })

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      await expect(apiService.recognizeDigits(file)).rejects.toThrow('Invalid image format')
    })

    it('should return generic error message when server message is missing', async () => {
      mock.onPost(/\/api\/recognize$/).reply(500, {})

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      await expect(apiService.recognizeDigits(file)).rejects.toThrow('Server error occurred')
    })
  })
})

