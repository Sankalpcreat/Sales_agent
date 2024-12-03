# AI Sales Assistant - Backend System

The backend infrastructure for the AI Sales Assistant is engineered to revolutionize sales operations by automating essential processes such as lead scoring, automated follow-ups, AI-driven proposal creation, and meeting summarization. This system handles core business logic, manages API endpoints, and ensures seamless integration with AI models and databases, thereby enhancing productivity and efficiency.

## **Architecture Overview**

Presented below is a high-level architecture diagram of the backend system, illustrating its components and interconnections:

![Backend Architecture](./backend/assets/screen.png)

## Key Features

- **Lead Scoring**: Utilize engagement metrics and activity analysis to prioritize and rank leads effectively.
- **Automated Follow-Ups**: Efficiently schedule, dispatch reminders, and execute follow-up communications automatically.
- **AI-Driven Proposal Drafting**: Employ artificial intelligence to craft personalized and impactful proposals tailored to client needs.
- **Meeting Summarization**: Generate concise and coherent summaries of meeting discussions, whether from notes or audio recordings.
- **Lead Recommendations**: Leverage FAISS technology to offer intelligent suggestions for similar leads, enhancing lead nurturing strategies.

## Additional Benefits

- **Scalability**: Designed to scale seamlessly with business growth, ensuring consistent performance.
- **Security**: Incorporates robust security protocols to safeguard data and maintain confidentiality.
- **Customization**: Offers customizable features to adapt to specific business requirements and workflows.

## Testing Coverage

Our backend implements comprehensive testing for all agent components. Here's an overview of our test coverage:

### Agent Test Coverage

#### Lead Scoring Agent
- Tests score calculation for leads
- Handles empty leads
- Validates input types

#### Follow-up Agent
- Tests scheduling follow-up tasks
- Verifies scheduler service integration

#### Lead Suggestions Agent
- Tests similar lead recommendations
- Handles invalid query vectors
- Handles empty query vectors

#### Meeting Summary Agent
- Tests meeting summarization functionality

#### Proposal Drafting Agent
- Tests proposal generation
- Verifies correct prompt formatting

### Test Implementation Details

All agents have been tested individually and are working as expected. Each test verifies the core functionality of its respective agent while properly mocking external dependencies (OllamaApiClient, SchedulerService, etc.).

### Running Tests

To run all agent tests:
```bash
cd backend
pytest tests/agents/ -v
```

To run a specific agent's tests:
```bash
cd backend
pytest tests/agents/test_lead_scoring.py -v
```
