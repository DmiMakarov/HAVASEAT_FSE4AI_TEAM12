import axios from 'axios'

// Get backend configuration from environment variables
const BACKEND_HOST = import.meta.env.BACKEND_HOST || 'localhost'
const BACKEND_PORT = import.meta.env.BACKEND_PORT || '5000'

// Construct the base API URL
const API_BASE_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`

/**
 * API service for communicating with the backend
 */
const apiService = {
  /**
   * Send an image to the backend for digit recognition
   * @param {File} imageFile - The image file to upload
   * @returns {Promise} - Response from the backend with recognized digits
   */
  async recognizeDigits(imageFile) {
    try {
      // Create FormData to send the image file
      const formData = new FormData()
      formData.append('image', imageFile)

      // Send POST request to the backend
      const response = await axios.post(`${API_BASE_URL}/api/recognize`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 30000 // 30 second timeout
      })

      return response.data
    } catch (error) {
      // Handle different types of errors
      if (error.response) {
        // Server responded with an error status
        throw new Error(error.response.data.message || 'Server error occurred')
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Cannot connect to backend. Please check if the server is running.')
      } else if (error.code === 'ERR_NETWORK') {
        // Network error
        throw new Error('Cannot connect to backend. Please check if the server is running.')
      } else {
        // Something else went wrong
        throw new Error('An error occurred while processing the request')
      }
    }
  }
}

export default apiService

