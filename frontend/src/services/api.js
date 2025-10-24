import axios from 'axios'

// Get backend configuration from environment variables
const BACKEND_HOST = import.meta.env.VITE_BACKEND_HOST || 'localhost'
const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5000'

// Construct the base API URL
const API_BASE_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`

// Log configuration for debugging
console.log('🔧 API Configuration:', {
  BACKEND_HOST,
  BACKEND_PORT,
  API_BASE_URL,
  environment: import.meta.env
})

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
    console.log('🚀 Starting digit recognition request...')
    console.log('📁 Image file details:', {
      name: imageFile.name,
      size: imageFile.size,
      type: imageFile.type
    })
    console.log('🌐 Request URL:', `${API_BASE_URL}/recognize_digit`)

    try {
      // Create FormData to send the image file
      const formData = new FormData()
      formData.append('image_file', imageFile)
      console.log('📦 FormData created successfully')

      console.log('📡 Sending POST request to backend...')
      // Send POST request to the backend
      const response = await axios.post(`${API_BASE_URL}/recognize_digit`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        timeout: 30000 // 30 second timeout
      })

      console.log('✅ Request successful!', {
        status: response.status,
        statusText: response.statusText,
        data: response.data
      })

      return response.data
    } catch (error) {
      console.error('❌ Request failed:', error)
      console.error('🔍 Error details:', {
        message: error.message,
        code: error.code,
        response: error.response ? {
          status: error.response.status,
          statusText: error.response.statusText,
          data: error.response.data
        } : null,
        request: error.request ? 'Request was made but no response received' : null
      })

      // Handle different types of errors
      if (error.response) {
        // Server responded with an error status
        console.error('📡 Server responded with error:', error.response.status, error.response.data)
        throw new Error(error.response.data.message || 'Server error occurred')
      } else if (error.request) {
        // Request was made but no response received
        console.error('🔌 No response received from server')
        throw new Error('Cannot connect to backend. Please check if the server is running.')
      } else if (error.code === 'ERR_NETWORK') {
        // Network error
        console.error('🌐 Network error occurred')
        throw new Error('Cannot connect to backend. Please check if the server is running.')
      } else {
        // Something else went wrong
        console.error('⚠️ Unexpected error:', error.message)
        throw new Error('An error occurred while processing the request')
      }
    }
  }
}

export default apiService

