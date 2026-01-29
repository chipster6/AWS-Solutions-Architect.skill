# Phase 0: Development and Testing Environment Setup Guide

## Overview

This guide provides detailed instructions for setting up development and testing environments for the AWS Solutions Architect skill enhancement project. It covers local development environments, cloud development environments, testing infrastructure, and environment configuration standards.

## Environment Architecture

### Development Environment Structure
```
Development Environment Hierarchy
├── Local Development
│   ├── IDE Configuration (VS Code, IntelliJ)
│   ├── Docker Containers
│   ├── Local Testing Tools
│   └── Development Scripts
├── Cloud Development
│   ├── AWS Cloud9
│   ├── GitHub Codespaces
│   ├── Cloud Testing Tools
│   └── Remote Development
├── Version Control
│   ├── Git Repository
│   ├── Branching Strategy
│   └── Code Review Process
└── Collaboration Tools
    ├── Slack / Teams
    ├── Project Management
    └── Documentation Wiki
```

### Testing Environment Structure
```
Testing Environment Hierarchy
├── Unit Testing
│   ├── Jest / Mocha
│   ├── Test Coverage
│   └── Code Quality
├── Integration Testing
│   ├── Cypress / Selenium
│   ├── API Testing
│   └── End-to-End Testing
├── Performance Testing
│   ├── Load Testing
│   ├── Stress Testing
│   └── Scalability Testing
└── Security Testing
    ├── Vulnerability Scanning
    ├── Penetration Testing
    └── Compliance Testing
```

## Local Development Environment Setup

### Prerequisites
- **Operating System**: macOS, Linux, or Windows 10+
- **RAM**: Minimum 8GB, Recommended 16GB
- **Storage**: Minimum 50GB free space
- **Internet**: Stable broadband connection

### Step 1: Install Development Tools

#### 1.1 Install VS Code
```bash
# Download from https://code.visualstudio.com/
# Install VS Code with default settings

# Recommended Extensions:
# - Python
# - Docker
# - GitLens
# - Markdown All in One
# - Prettier
# - ESLint
```

#### 1.2 Install Docker Desktop
```bash
# Download from https://www.docker.com/products/docker-desktop
# Install with default settings
# Ensure Docker is running after installation

# Verify installation:
docker --version
```

#### 1.3 Install Git
```bash
# For macOS:
brew install git

# For Linux:
sudo apt-get install git

# For Windows:
download from https://git-scm.com/download/win

# Configure Git:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 1.4 Install Node.js and npm
```bash
# Using nvm (recommended):
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install Node.js LTS:
nvm install --lts
nvm use --lts

# Verify installation:
node --version
npm --version
```

### Step 2: Configure Development Environment

#### 2.1 Set Up Project Directory
```bash
# Create project directory
mkdir -p ~/Projects/aws-solutions-architect
cd ~/Projects/aws-solutions-architect

# Initialize Git repository
git init
```

#### 2.2 Configure VS Code
```json
{
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "editor.trimAutoWhitespace": true,
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "editor.formatOnSave": true,
    "prettier.singleQuote": true,
    "prettier.trailingComma": "es5"
}
```

#### 2.3 Set Up Docker Environment
```bash
# Create Docker Compose file
docker-compose.yml
```

### Step 3: Install Project Dependencies

#### 3.1 Clone Repository
```bash
# Clone the AWS Solutions Architect repository
git clone https://github.com/your-org/aws-solutions-architect.git
cd aws-solutions-architect

# Install dependencies
npm install
```

#### 3.2 Set Up Development Scripts
```json
{
  "scripts": {
    "dev": "npm run build && npm run start",
    "build": "webpack --mode development",
    "start": "webpack-dev-server --mode development --open",
    "test": "jest --watch",
    "lint": "eslint .",
    "format": "prettier --write ."
  }
}
```

## Cloud Development Environment Setup

### AWS Cloud9 Setup

#### 1. Create Cloud9 Environment
```bash
# Log in to AWS Management Console
# Navigate to Cloud9 service
# Click "Create environment"
# Configure environment settings:
# - Name: aws-solutions-architect-dev
# - Environment type: Create a new EC2 instance
# - Instance type: t3.medium
# - Platform: Amazon Linux 2
# - Cost-saving settings: After 30 minutes
```

#### 2. Configure Cloud9 Environment
```bash
# Update system packages
sudo yum update -y

# Install development tools
sudo yum install -y git docker nodejs npm

# Configure Node.js and npm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
nvm use --lts

# Install project dependencies
cd ~/environment/aws-solutions-architect
npm install
```

### GitHub Codespaces Setup

#### 1. Enable Codespaces
```bash
# Navigate to GitHub repository
# Click "Settings" → "Features" → "Codespaces"
# Enable Codespaces for the repository
```

#### 2. Create Codespace
```bash
# Navigate to repository
# Click "Code" → "Codespaces" → "New codespace"
# Configure codespace settings:
# - Machine type: Standard (2 core, 32 GB RAM)
# - Dev container: Use existing Dockerfile
# - Dotfiles: Optional
```

## Testing Environment Setup

### Unit Testing Setup

#### 1. Install Testing Framework
```bash
# Install Jest for JavaScript testing
npm install --save-dev jest

# Install testing utilities
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

#### 2. Configure Jest
```json
{
  "jest": {
    "testEnvironment": "jsdom",
    "setupFilesAfterEnv": ["<rootDir>/src/setupTests.js"],
    "moduleNameMapping": {
      "^@/(.*)$": "<rootDir>/src/$1"
    }
  }
}
```

#### 3. Create Test Scripts
```javascript
// src/components/__tests__/example.test.js
import { render, screen } from '@testing-library/react';
import ExampleComponent from '../ExampleComponent';

describe('ExampleComponent', () => {
  test('renders correctly', () => {
    render(<ExampleComponent />);
    expect(screen.getByText('Example')).toBeInTheDocument();
  });
});
```

### Integration Testing Setup

#### 1. Install Cypress
```bash
# Install Cypress for end-to-end testing
npm install --save-dev cypress

# Install additional utilities
npm install --save-dev @testing-library/cypress
```

#### 2. Configure Cypress
```javascript
// cypress.config.js
module.exports = {
  e2e: {
    baseUrl: 'http://localhost:3000',
    supportFile: 'cypress/support/e2e.js',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
  },
};
```

#### 3. Create Integration Tests
```javascript
// cypress/e2e/example.cy.js
describe('Example Application', () => {
  it('loads the application', () => {
    cy.visit('/');
    cy.get('h1').should('contain', 'Welcome');
  });
});
```

### Performance Testing Setup

#### 1. Install Load Testing Tools
```bash
# Install Artillery for load testing
npm install -g artillery

# Install additional tools
npm install --save-dev lighthouse
```

#### 2. Configure Load Tests
```yaml
# load-test.yml
config:
  target: "http://localhost:3000"
  phases:
    - duration: 60
      arrivalRate: 5
      name: "Warm up"
    - duration: 120
      arrivalRate: 10
      rampTo: 50
      name: "Ramp up"
    - duration: 300
      arrivalRate: 50
      name: " sustained load"

scenarios:
  - name: "Load test"
    flow:
      - get:
          url: "/"
      - post:
          url: "/api/data"
          json:
            key: "value"
```

## Environment Configuration Standards

### Development Environment Standards

#### 1. Code Quality Standards
```json
{
  "rules": {
    "quotes": ["error", "single"],
    "semi": ["error", "always"],
    "indent": ["error", 2],
    "linebreak-style": ["error", "unix"],
    "no-console": "warn",
    "no-unused-vars": "error"
  }
}
```

#### 2. Security Standards
```bash
# Security scanning with npm audit
npm audit

# Security configuration
# .npmrc
package-lock=false
prefer-frozen-lockfile=true

# .gitignore
node_modules/
.env
*.log
.DS_Store
```

#### 3. Documentation Standards
```markdown
# Documentation Template

## Overview
Brief description of the component or feature.

## Requirements
- List of requirements
- Acceptance criteria

## Implementation
- Technical details
- Configuration options

## Testing
- Test cases
- Expected results

## Deployment
- Deployment steps
- Environment requirements
```

### Testing Environment Standards

#### 1. Test Data Management
```bash
# Test data directory structure
test-data/
├── unit/
│   ├── input/
│   └── expected/
├── integration/
│   ├── fixtures/
│   └── mocks/
└── performance/
    ├── datasets/
    └── scenarios/
```

#### 2. Test Automation Standards
```javascript
// Test automation configuration
{
  "testAutomation": {
    "unitTests": {
      "coverageThreshold": 80,
      "testTimeout": 5000
    },
    "integrationTests": {
      "parallelExecution": true,
      "retryAttempts": 2
    },
    "performanceTests": {
      "baselineMetrics": true,
      "alertThreshold": 20
    }
  }
}
```

## Environment Validation

### Validation Checklist

#### Development Environment Validation
- [ ] VS Code configured with required extensions
- [ ] Docker Desktop installed and running
- [ ] Git configured with user credentials
- [ ] Node.js and npm installed
- [ ] Project dependencies installed
- [ ] Development scripts working
- [ ] Code quality tools configured

#### Testing Environment Validation
- [ ] Unit testing framework installed
- [ ] Integration testing framework installed
- [ ] Performance testing tools installed
- [ ] Test data available
- [ ] Test automation configured
- [ ] Test coverage reporting enabled
- [ ] Security scanning configured

#### Cloud Environment Validation
- [ ] Cloud9 environment created and configured
- [ ] Codespaces enabled and working
- [ ] Remote development access configured
- [ ] Cloud storage and databases accessible
- [ ] Network connectivity verified
- [ ] Security groups and IAM roles configured

## Troubleshooting Guide

### Common Development Issues

#### 1. Docker Issues
```bash
# Common Docker problems and solutions
# Docker daemon not running
# Solution: Start Docker Desktop or Docker service

# Permission denied
# Solution: Add user to docker group
sudo usermod -aG docker $USER

# Out of disk space
# Solution: Clean up unused images and containers
docker system prune -a
```

#### 2. Node.js Issues
```bash
# Common Node.js problems and solutions
# Module not found
# Solution: Reinstall dependencies
rm -rf node_modules && npm install

# Version conflicts
# Solution: Use nvm to manage Node.js versions
nvm install --lts
nvm use --lts

# Memory issues
# Solution: Increase Node.js memory limit
export NODE_OPTIONS=--max-old-space-size=4096
```

#### 3. Git Issues
```bash
# Common Git problems and solutions
# Authentication issues
# Solution: Configure SSH keys or personal access tokens

# Merge conflicts
# Solution: Resolve conflicts manually or use merge tools
git mergetool

# Large file issues
# Solution: Use Git LFS for large files
git lfs install
```

### Common Testing Issues

#### 1. Test Failures
```bash
# Common test failure causes and solutions
# Environment not set up
# Solution: Check test environment configuration

# Dependencies missing
# Solution: Install required test dependencies

# Test data issues
# Solution: Verify test data availability and format
```

#### 2. Performance Issues
```bash
# Common performance issues and solutions
# Resource constraints
# Solution: Increase system resources or optimize tests

# Network latency
# Solution: Use local test data or mock services

# Test execution time
# Solution: Optimize test cases or use parallel execution
```

## Next Steps

### Immediate Actions
1. Set up local development environment
2. Configure cloud development environment
3. Install testing frameworks and tools
4. Create test data and test cases
5. Validate environment configuration

### Short-term Actions (Week 1)
1. Complete environment setup and validation
2. Configure CI/CD pipeline integration
3. Set up monitoring and logging
4. Establish documentation standards
5. Conduct team training on development tools

### Long-term Actions (Month 1)
1. Optimize development workflows
2. Implement advanced testing strategies
3. Set up automated environment provisioning
4. Establish environment governance
5. Conduct regular environment audits

---

**Development and Testing Environment Setup Guide**: Version 1.0.0  
**Created**: 2026-01-28  
**Next Review**: 2026-02-04  
**Implementation Start**: 2026-01-28