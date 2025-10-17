import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ImageUpload from '../ImageUpload.vue'
import apiService from '../../services/api.js'

// Mock the API service
vi.mock('../../services/api.js', () => ({
  default: {
    recognizeDigits: vi.fn()
  }
}))

describe('ImageUpload Component', () => {
  let wrapper

  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks()
  })

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount()
    }
  })

  describe('Component Rendering', () => {
    it('should render the component correctly', () => {
      wrapper = mount(ImageUpload)

      expect(wrapper.find('h1').text()).toBe('Digit Recognition')
      expect(wrapper.find('.subtitle').text()).toContain('Upload an image')
      expect(wrapper.find('.dropzone').exists()).toBe(true)
    })

    it('should show upload prompt when no image is selected', () => {
      wrapper = mount(ImageUpload)

      expect(wrapper.find('.upload-prompt').exists()).toBe(true)
      expect(wrapper.text()).toContain('Click or drag and drop an image here')
    })

    it('should not show buttons when no file is selected', () => {
      wrapper = mount(ImageUpload)

      expect(wrapper.find('.button-group').exists()).toBe(false)
    })
  })

  describe('File Selection', () => {
    it('should handle file selection via input', async () => {
      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      // Mock FileReader
      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      // Directly call processFile since we can't set file input values in jsdom
      await wrapper.vm.processFile(file)
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.selectedFile).toBeTruthy()
    })

    it('should display image preview after file selection', async () => {
      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.imagePreview).toBeTruthy()
      expect(wrapper.find('.preview-container').exists()).toBe(true)
      expect(wrapper.find('.image-preview').exists()).toBe(true)
    })

    it('should show action buttons after file selection', async () => {
      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)
      await wrapper.vm.$nextTick()

      expect(wrapper.find('.button-group').exists()).toBe(true)
      expect(wrapper.findAll('.btn').length).toBe(2)
    })
  })

  describe('File Validation', () => {
    it('should accept valid image files', async () => {
      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.errorMessage).toBe('')
      expect(wrapper.vm.selectedFile).toBeTruthy()
    })

    it('should reject non-image files', async () => {
      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.txt', { type: 'text/plain' })

      await wrapper.vm.processFile(file)
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.errorMessage).toBe('Please select a valid image file')
      expect(wrapper.vm.selectedFile).toBeNull()
    })

    it('should reject files larger than 10MB', async () => {
      wrapper = mount(ImageUpload)

      const largeFile = new File(['x'.repeat(11 * 1024 * 1024)], 'large.png', {
        type: 'image/png'
      })

      await wrapper.vm.processFile(largeFile)
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.errorMessage).toBe('File size must be less than 10MB')
      expect(wrapper.vm.selectedFile).toBeNull()
    })
  })

  describe('Digit Recognition', () => {
    it('should call API service when recognizing digits', async () => {
      apiService.recognizeDigits.mockResolvedValue({ digits: '12345' })

      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)
      await wrapper.vm.recognizeImage()
      await wrapper.vm.$nextTick()

      expect(apiService.recognizeDigits).toHaveBeenCalledWith(file)
      expect(wrapper.vm.recognizedDigits).toBe('12345')
    })

    it('should display recognized digits', async () => {
      apiService.recognizeDigits.mockResolvedValue({ digits: '67890' })

      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)
      await wrapper.vm.recognizeImage()
      await wrapper.vm.$nextTick()

      expect(wrapper.find('.results-section').exists()).toBe(true)
      expect(wrapper.find('.result-value').text()).toBe('67890')
    })

    it('should handle different API response formats', async () => {
      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)

      // Test 'result' format
      apiService.recognizeDigits.mockResolvedValue({ result: '111' })
      await wrapper.vm.recognizeImage()
      expect(wrapper.vm.recognizedDigits).toBe('111')

      // Test 'recognized_digits' format
      apiService.recognizeDigits.mockResolvedValue({ recognized_digits: '222' })
      await wrapper.vm.recognizeImage()
      expect(wrapper.vm.recognizedDigits).toBe('222')
    })

    it('should show loading state during recognition', async () => {
      apiService.recognizeDigits.mockImplementation(() =>
        new Promise(resolve => setTimeout(() => resolve({ digits: '123' }), 100))
      )

      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)

      const recognizePromise = wrapper.vm.recognizeImage()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.isLoading).toBe(true)
      expect(wrapper.find('.spinner').exists()).toBe(true)

      await recognizePromise
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.isLoading).toBe(false)
    })

    it('should handle API errors gracefully', async () => {
      apiService.recognizeDigits.mockRejectedValue(new Error('API Error'))

      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)
      await wrapper.vm.recognizeImage()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.errorMessage).toBe('API Error')
      expect(wrapper.find('.error-message').exists()).toBe(true)
    })

    it('should disable buttons during loading', async () => {
      apiService.recognizeDigits.mockImplementation(() =>
        new Promise(resolve => setTimeout(() => resolve({ digits: '123' }), 100))
      )

      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)
      await wrapper.vm.$nextTick()

      const recognizeButton = wrapper.find('.btn-primary')
      const clearButton = wrapper.find('.btn-secondary')

      const recognizePromise = wrapper.vm.recognizeImage()
      await wrapper.vm.$nextTick()

      expect(recognizeButton.attributes('disabled')).toBeDefined()
      expect(clearButton.attributes('disabled')).toBeDefined()

      await recognizePromise
    })
  })

  describe('Clear Functionality', () => {
    it('should clear all data when clear button is clicked', async () => {
      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      await wrapper.vm.processFile(file)
      wrapper.vm.recognizedDigits = '12345'
      wrapper.vm.errorMessage = 'Test error'
      await wrapper.vm.$nextTick()

      await wrapper.vm.clearImage()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.selectedFile).toBeNull()
      expect(wrapper.vm.imagePreview).toBeNull()
      expect(wrapper.vm.recognizedDigits).toBeNull()
      expect(wrapper.vm.errorMessage).toBe('')
    })
  })

  describe('Drag and Drop', () => {
    it('should handle dragover event', async () => {
      wrapper = mount(ImageUpload)

      const dropzone = wrapper.find('.dropzone')
      await dropzone.trigger('dragover')

      expect(wrapper.vm.isDragging).toBe(true)
      expect(dropzone.classes()).toContain('dragover')
    })

    it('should handle dragleave event', async () => {
      wrapper = mount(ImageUpload)

      const dropzone = wrapper.find('.dropzone')
      await dropzone.trigger('dragover')
      expect(wrapper.vm.isDragging).toBe(true)

      await dropzone.trigger('dragleave')
      expect(wrapper.vm.isDragging).toBe(false)
    })

    it('should handle drop event', async () => {
      wrapper = mount(ImageUpload)

      const file = new File(['test'], 'test.png', { type: 'image/png' })

      global.FileReader = class {
        readAsDataURL() {
          this.onload({ target: { result: 'data:image/png;base64,test' } })
        }
      }

      const dropzone = wrapper.find('.dropzone')
      const dropEvent = {
        dataTransfer: {
          files: [file]
        }
      }

      await dropzone.trigger('drop', dropEvent)
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.isDragging).toBe(false)
    })
  })

  describe('UI Interactions', () => {
    it('should trigger file input when dropzone is clicked', async () => {
      wrapper = mount(ImageUpload)

      const fileInput = wrapper.find('input[type="file"]')
      const clickSpy = vi.spyOn(fileInput.element, 'click')

      const dropzone = wrapper.find('.dropzone')
      await dropzone.trigger('click')

      expect(clickSpy).toHaveBeenCalled()
    })
  })

  describe('Error Display', () => {
    it('should show error message when present', async () => {
      wrapper = mount(ImageUpload)

      wrapper.vm.errorMessage = 'Test error message'
      await wrapper.vm.$nextTick()

      expect(wrapper.find('.error-message').exists()).toBe(true)
      expect(wrapper.find('.error-message').text()).toContain('Test error message')
    })

    it('should not show error message when empty', () => {
      wrapper = mount(ImageUpload)

      expect(wrapper.find('.error-message').exists()).toBe(false)
    })
  })
})

