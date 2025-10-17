import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'
import ImageUpload from '../components/ImageUpload.vue'

describe('App Component', () => {
  it('should render the App component', () => {
    const wrapper = mount(App)
    expect(wrapper.exists()).toBe(true)
  })

  it('should contain ImageUpload component', () => {
    const wrapper = mount(App)
    expect(wrapper.findComponent(ImageUpload).exists()).toBe(true)
  })

  it('should have correct structure', () => {
    const wrapper = mount(App)
    expect(wrapper.find('#app').exists()).toBe(true)
  })
})

