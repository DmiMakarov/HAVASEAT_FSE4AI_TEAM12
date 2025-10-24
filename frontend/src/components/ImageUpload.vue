<template>
  <div class="image-upload-container">
    <div class="header">
      <div class="icon-container">
        <svg class="header-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h1>Digit Recognition</h1>
      <p class="subtitle">Upload an image and let AI recognize the digits</p>
    </div>

    <!-- File Input Area -->
    <div class="upload-section">
      <div
        class="dropzone"
        :class="{ 'dragover': isDragging }"
        @drop.prevent="handleDrop"
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @click="triggerFileInput"
      >
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          @change="handleFileSelect"
          style="display: none"
        />
        <div v-if="!imagePreview" class="upload-prompt">
          <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p>Click or drag and drop an image here</p>
          <p class="upload-hint">PNG, JPG, GIF up to 10MB</p>
        </div>
        <div v-else class="preview-container">
          <img :src="imagePreview" alt="Preview" class="image-preview" />
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="button-group" v-if="selectedFile">
        <button
          @click="recognizeImage"
          :disabled="isLoading"
          class="btn btn-primary"
        >
          <span v-if="!isLoading">Recognize Digits</span>
          <span v-else class="loading-text">
            <span class="spinner"></span>
            Processing...
          </span>
        </button>
        <button
          @click="clearImage"
          :disabled="isLoading"
          class="btn btn-secondary"
        >
          Clear
        </button>
      </div>

    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      <svg class="error-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      {{ errorMessage }}
    </div>

    <!-- Results Section -->
    <div v-if="recognizedDigits !== null" class="results-section">
      <h2>Recognition Result</h2>
      <div class="result-box">
        <p class="result-label">Recognized Digits:</p>
        <p class="result-value">{{ recognizedDigits }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import apiService from '../services/api.js'

export default {
  name: 'ImageUpload',
  setup() {
    const fileInput = ref(null)
    const selectedFile = ref(null)
    const imagePreview = ref(null)
    const recognizedDigits = ref(null)
    const isLoading = ref(false)
    const errorMessage = ref('')
    const isDragging = ref(false)

    // Maximum file size (10MB)
    const MAX_FILE_SIZE = 10 * 1024 * 1024

    const triggerFileInput = () => {
      fileInput.value.click()
    }

    const validateFile = (file) => {
      // Check if file is an image
      if (!file.type.startsWith('image/')) {
        throw new Error('Please select a valid image file')
      }

      // Check file size
      if (file.size > MAX_FILE_SIZE) {
        throw new Error('File size must be less than 10MB')
      }

      return true
    }

    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        processFile(file)
      }
    }

    const handleDrop = (event) => {
      isDragging.value = false
      const file = event.dataTransfer.files[0]
      if (file) {
        processFile(file)
      }
    }

    const processFile = (file) => {
      try {
        validateFile(file)
        selectedFile.value = file
        errorMessage.value = ''
        recognizedDigits.value = null

        // Create preview
        const reader = new FileReader()
        reader.onload = (e) => {
          imagePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      } catch (error) {
        errorMessage.value = error.message
      }
    }

    const recognizeImage = async () => {
      if (!selectedFile.value) return

      isLoading.value = true
      errorMessage.value = ''
      recognizedDigits.value = null

      try {
        const response = await apiService.recognizeDigits(selectedFile.value)

        // Handle response format from backend
        if (response.recognized_digit !== undefined) {
          recognizedDigits.value = response.recognized_digit
        } else {
          recognizedDigits.value = JSON.stringify(response)
        }
      } catch (error) {
        errorMessage.value = error.message
      } finally {
        isLoading.value = false
      }
    }

    const clearImage = () => {
      selectedFile.value = null
      imagePreview.value = null
      recognizedDigits.value = null
      errorMessage.value = ''
      if (fileInput.value) {
        fileInput.value.value = ''
      }
    }


    return {
      fileInput,
      selectedFile,
      imagePreview,
      recognizedDigits,
      isLoading,
      errorMessage,
      isDragging,
      triggerFileInput,
      handleFileSelect,
      handleDrop,
      processFile,
      recognizeImage,
      clearImage
    }
  }
}
</script>

<style scoped>
.image-upload-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  margin-bottom: 3rem;
  animation: fadeInDown 0.8s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.icon-container {
  display: inline-flex;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  margin-bottom: 1rem;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 12px 48px rgba(102, 126, 234, 0.4);
  }
}

.header-icon {
  width: 48px;
  height: 48px;
  color: white;
}

h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  letter-spacing: -0.5px;
}

@media (prefers-color-scheme: light) {
  h1 {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

.subtitle {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0;
  font-size: 1.2rem;
  font-weight: 300;
}

@media (prefers-color-scheme: light) {
  .subtitle {
    color: rgba(0, 0, 0, 0.6);
  }
}

.upload-section {
  margin-bottom: 2rem;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropzone {
  border: 3px dashed rgba(102, 126, 234, 0.3);
  border-radius: 24px;
  padding: 3rem 2rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  min-height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.dropzone::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
  transform: rotate(45deg);
  transition: all 0.6s ease;
}

@media (prefers-color-scheme: light) {
  .dropzone {
    background: rgba(255, 255, 255, 0.8);
    border-color: rgba(102, 126, 234, 0.4);
  }
}

.dropzone:hover {
  border-color: #667eea;
  transform: translateY(-4px);
  box-shadow: 0 12px 48px rgba(102, 126, 234, 0.3);
}

.dropzone:hover::before {
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%) translateY(-100%) rotate(45deg);
  }
  100% {
    transform: translateX(100%) translateY(100%) rotate(45deg);
  }
}

.dropzone.dragover {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
  transform: scale(1.02);
  box-shadow: 0 16px 64px rgba(76, 175, 80, 0.3);
}

@media (prefers-color-scheme: light) {
  .dropzone.dragover {
    background: rgba(76, 175, 80, 0.15);
  }
}

.upload-prompt {
  text-align: center;
}

.upload-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 1.5rem;
  color: #667eea;
  filter: drop-shadow(0 4px 12px rgba(102, 126, 234, 0.3));
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.upload-prompt p {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

@media (prefers-color-scheme: light) {
  .upload-prompt p {
    color: #2d3748;
  }
}

.upload-hint {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.5) !important;
  font-weight: 300;
}

@media (prefers-color-scheme: light) {
  .upload-hint {
    color: rgba(0, 0, 0, 0.4) !important;
  }
}

.preview-container {
  width: 100%;
  max-height: 450px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.image-preview {
  max-width: 100%;
  max-height: 450px;
  border-radius: 16px;
  object-fit: contain;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.image-preview:hover {
  transform: scale(1.02);
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.btn {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 600;
  min-width: 180px;
  position: relative;
  overflow: hidden;
  letter-spacing: 0.5px;
}

.btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn:hover::before {
  width: 300px;
  height: 300px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(-1px);
}

.btn-secondary {
  background: linear-gradient(135deg, #6B7280 0%, #4B5563 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(107, 114, 128, 0.3);
}

.btn-secondary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(107, 114, 128, 0.4);
}

.btn-secondary:active:not(:disabled) {
  transform: translateY(-1px);
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
  backdrop-filter: blur(10px);
  color: #ef4444;
  padding: 1.25rem 1.5rem;
  border-radius: 16px;
  margin: 1.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border: 2px solid rgba(239, 68, 68, 0.3);
  box-shadow: 0 4px 20px rgba(239, 68, 68, 0.2);
  animation: slideIn 0.4s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media (prefers-color-scheme: light) {
  .error-message {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.15) 100%);
    color: #dc2626;
  }
}

.error-icon {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.results-section {
  margin-top: 2.5rem;
  padding: 2.5rem;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(67, 160, 71, 0.1) 100%);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 2px solid rgba(76, 175, 80, 0.3);
  box-shadow: 0 8px 32px rgba(76, 175, 80, 0.2);
  animation: zoomIn 0.5s ease-out;
}

@keyframes zoomIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@media (prefers-color-scheme: light) {
  .results-section {
    background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(67, 160, 71, 0.15) 100%);
  }
}

.results-section h2 {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  font-weight: 600;
}

@media (prefers-color-scheme: light) {
  .results-section h2 {
    color: #1a202c;
  }
}

.result-box {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

@media (prefers-color-scheme: light) {
  .result-box {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(0, 0, 0, 0.05);
  }
}

.result-label {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 1rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
}

@media (prefers-color-scheme: light) {
  .result-label {
    color: rgba(0, 0, 0, 0.6);
  }
}

.result-value {
  font-size: 4rem;
  font-weight: 800;
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  text-shadow: 0 4px 20px rgba(76, 175, 80, 0.3);
  animation: popIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes popIn {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@media (max-width: 600px) {
  .header-icon {
    width: 40px;
    height: 40px;
  }

  .icon-container {
    padding: 0.75rem;
  }

  h1 {
    font-size: 2.2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .dropzone {
    padding: 2rem 1rem;
    min-height: 280px;
  }

  .upload-icon {
    width: 56px;
    height: 56px;
  }

  .button-group {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    min-width: unset;
  }

  .result-value {
    font-size: 3rem;
  }

  .results-section {
    padding: 2rem 1.5rem;
  }
}

</style>



