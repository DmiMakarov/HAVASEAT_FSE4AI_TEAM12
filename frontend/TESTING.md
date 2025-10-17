# Testing Guide

This document provides information about the testing setup and how to run tests for the Vue Digit Recognition frontend.

## Testing Stack

- **Vitest**: Fast unit test framework powered by Vite
- **Vue Test Utils**: Official testing library for Vue.js
- **jsdom**: Simulates DOM environment for testing
- **axios-mock-adapter**: Mocks HTTP requests for API testing
- **@vitest/ui**: Interactive UI for viewing test results
- **@vitest/coverage-v8**: Code coverage reporting

## Running Tests

### Using Docker (Recommended)

```bash
# Run all tests once
make test

# Run tests in watch mode (auto-rerun on file changes)
make test-watch

# Run tests with interactive UI
make test-ui

# Run tests with coverage report
make test-coverage
```

### Without Docker

```bash
cd frontend

# Install dependencies first
npm install

# Run all tests once
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## Test Structure

Tests are organized in a dedicated `tests/` folder (similar to Python projects):

```
frontend/
├── src/                        # Source code
│   ├── components/
│   └── services/
└── tests/                      # All tests in one place
    ├── App.test.js             # App component tests
    ├── components/
    │   └── ImageUpload.test.js # Component tests
    └── services/
        └── api.test.js         # API service tests
```

## Test Coverage

The test suite covers:

### API Service (`api.test.js`)
- ✅ Successful API calls
- ✅ Server error handling
- ✅ Network error handling
- ✅ Timeout handling
- ✅ FormData structure validation
- ✅ Multiple response formats support
- ✅ Custom error messages
- ✅ Configuration validation

### ImageUpload Component (`ImageUpload.test.js`)
- ✅ Component rendering
- ✅ File selection via input
- ✅ File selection via drag and drop
- ✅ Image preview display
- ✅ File validation (type and size)
- ✅ Digit recognition workflow
- ✅ Loading states
- ✅ Error handling and display
- ✅ Clear functionality
- ✅ Button states (enabled/disabled)
- ✅ UI interactions

### App Component (`App.test.js`)
- ✅ Main app structure
- ✅ Component integration

## Writing New Tests

### Example: Component Test

```javascript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '../MyComponent.vue'

describe('MyComponent', () => {
  it('should render correctly', () => {
    const wrapper = mount(MyComponent)
    expect(wrapper.text()).toContain('Expected text')
  })

  it('should handle button click', async () => {
    const wrapper = mount(MyComponent)
    await wrapper.find('button').trigger('click')
    expect(wrapper.vm.someProperty).toBe('expected value')
  })
})
```

### Example: API Test

```javascript
import { describe, it, expect, beforeEach } from 'vitest'
import MockAdapter from 'axios-mock-adapter'
import axios from 'axios'
import apiService from '../api.js'

describe('API Service', () => {
  let mock

  beforeEach(() => {
    mock = new MockAdapter(axios)
  })

  afterEach(() => {
    mock.reset()
  })

  it('should fetch data successfully', async () => {
    mock.onGet('/api/data').reply(200, { data: 'test' })

    const result = await apiService.getData()
    expect(result.data).toBe('test')
  })
})
```

## Best Practices

### 1. Test Organization
- Group related tests using `describe` blocks
- Use descriptive test names that explain what is being tested
- Keep tests focused on a single piece of functionality

### 2. Test Isolation
- Each test should be independent
- Use `beforeEach` and `afterEach` hooks for setup and cleanup
- Reset mocks and clear states between tests

### 3. Assertions
- Make one primary assertion per test
- Use specific matchers (`toBe`, `toEqual`, `toContain`, etc.)
- Test both positive and negative cases

### 4. Async Testing
```javascript
it('should handle async operations', async () => {
  const result = await someAsyncFunction()
  expect(result).toBeDefined()
})
```

### 5. Component Testing
```javascript
it('should update reactive data', async () => {
  const wrapper = mount(Component)
  wrapper.vm.someData = 'new value'
  await wrapper.vm.$nextTick() // Wait for DOM update
  expect(wrapper.text()).toContain('new value')
})
```

## Mocking

### Mocking Modules
```javascript
vi.mock('../api.js', () => ({
  default: {
    recognizeDigits: vi.fn()
  }
}))
```

### Mocking Global Objects
```javascript
global.FileReader = class {
  readAsDataURL() {
    this.onload({ target: { result: 'mock-data' } })
  }
}
```

## Coverage Reports

After running `make test-coverage`, you can view the coverage report:

```bash
# Open HTML coverage report
open frontend/coverage/index.html
```

Coverage includes:
- **Statements**: Percentage of statements executed
- **Branches**: Percentage of conditional branches tested
- **Functions**: Percentage of functions called
- **Lines**: Percentage of lines executed

### Target Coverage
- Aim for at least 80% coverage
- Focus on critical paths and user interactions
- Don't sacrifice test quality for coverage numbers

## Continuous Integration

Tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    cd frontend
    npm install
    npm test

- name: Upload Coverage
  run: |
    cd frontend
    npm run test:coverage
```

## Debugging Tests

### Run Single Test File
```bash
npm test -- ImageUpload.test.js
```

### Run Tests Matching Pattern
```bash
npm test -- -t "should handle file selection"
```

### Debug in VS Code
Add to `.vscode/launch.json`:
```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug Vitest Tests",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["test"],
  "console": "integratedTerminal"
}
```

### Use `console.log` in Tests
```javascript
it('should debug test', () => {
  console.log('Debug info:', someVariable)
  expect(someVariable).toBeDefined()
})
```

## Common Issues

### Issue: "Cannot find module"
**Solution**: Ensure all dependencies are installed
```bash
npm install
```

### Issue: "ReferenceError: File is not defined"
**Solution**: Mock the global object
```javascript
global.File = class extends Blob {
  constructor(chunks, filename, options) {
    super(chunks, options)
    this.name = filename
  }
}
```

### Issue: Tests timeout
**Solution**: Increase timeout in `vitest.config.js`
```javascript
test: {
  testTimeout: 10000
}
```

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [Vue Test Utils Documentation](https://test-utils.vuejs.org/)
- [Testing Library Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Vitest UI](https://vitest.dev/guide/ui.html)

## Contributing Tests

When adding new features:
1. Write tests alongside the feature code
2. Ensure all tests pass before committing
3. Maintain or improve code coverage
4. Follow existing test patterns and conventions
5. Document any complex test scenarios

Happy Testing! 🧪✨

