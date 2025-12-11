/**
 * Test fixtures and mock data for RAG Chat Widget
 * Provides realistic mock responses for unit and integration testing
 */

import type {
  ChatMessage,
  RetrievalSource,
  QueryRequest,
  ChatResponse,
  ErrorResponse,
  WidgetState,
} from '../components/RAGChatWidget/types';

/**
 * Mock retrieval source (book excerpt)
 */
export const mockRetrievalSource: RetrievalSource = {
  chunk_id: 'chunk-001',
  text: 'Kinematics is the branch of mechanics that studies motion without considering the forces that cause it.',
  similarity_score: 0.89,
  source_url: 'http://localhost:3000/docs/physics/kinematics',
  section_title: '2.1 Introduction to Kinematics',
  rank: 1,
};

/**
 * Mock chat response from backend
 */
export const mockChatResponse: ChatResponse = {
  request_id: '550e8400-e29b-41d4-a716-446655440000',
  answer:
    'Kinematics is the branch of mechanics that describes the motion of objects and systems without concern for the forces that caused the motion.',
  sources: [mockRetrievalSource],
  context_used: 1,
  tokens_used: 42,
  response_time_ms: 1250,
  timestamp: new Date().toISOString(),
  note: 'Response generated from 1 context chunk',
};

/**
 * Mock user message
 */
export const mockUserMessage: ChatMessage = {
  id: 'msg-001',
  role: 'user',
  content: 'What is kinematics?',
  timestamp: new Date().toISOString(),
  selectedText: undefined,
};

/**
 * Mock assistant message with sources
 */
export const mockAssistantMessage: ChatMessage = {
  id: 'msg-002',
  role: 'assistant',
  content: mockChatResponse.answer,
  timestamp: new Date().toISOString(),
  sources: mockChatResponse.sources,
  metadata: {
    durationMs: mockChatResponse.response_time_ms,
    tokensUsed: mockChatResponse.tokens_used,
    contextUsed: mockChatResponse.context_used,
  },
};

/**
 * Mock error response (validation error)
 */
export const mockErrorResponseValidation: ErrorResponse = {
  detail: {
    error: 'Validation Error',
    details: [
      {
        field: 'query',
        message: 'Field required',
      },
    ],
    request_id: '550e8400-e29b-41d4-a716-446655440001',
  },
  timestamp: new Date().toISOString(),
};

/**
 * Mock error response (service unavailable)
 */
export const mockErrorResponseServiceUnavailable: ErrorResponse = {
  detail: {
    error: 'Service Unavailable',
    request_id: '550e8400-e29b-41d4-a716-446655440002',
  },
  timestamp: new Date().toISOString(),
};

/**
 * Mock initial widget state
 */
export const mockInitialWidgetState: WidgetState = {
  messages: [],
  isLoading: false,
  error: null,
  selectedText: null,
  isMinimized: false,
  apiUrl: 'http://localhost:8000/ask',
  sessionId: 'session-001',
};

/**
 * Mock widget state with one exchange
 */
export const mockWidgetStateWithMessages: WidgetState = {
  ...mockInitialWidgetState,
  messages: [mockUserMessage, mockAssistantMessage],
};

/**
 * Mock widget state with loading
 */
export const mockWidgetStateLoading: WidgetState = {
  ...mockInitialWidgetState,
  isLoading: true,
  messages: [mockUserMessage],
};

/**
 * Mock widget state with error
 */
export const mockWidgetStateWithError: WidgetState = {
  ...mockInitialWidgetState,
  error: 'Unable to reach server. Please check your connection.',
  messages: [mockUserMessage],
};

/**
 * Mock query request
 */
export const mockQueryRequest: QueryRequest = {
  query: 'What is kinematics?',
  top_k: 5,
  similarity_threshold: 0.5,
};

/**
 * Mock query request with context (selected text)
 */
export const mockQueryRequestWithContext: QueryRequest = {
  ...mockQueryRequest,
  context:
    'The study of motion without considering forces is called kinematics.',
};

/**
 * Mock fetch response (for testing fetch mocking)
 */
export function createMockFetchResponse(
  data: any,
  status = 200
): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

/**
 * Mock window.getSelection for text selection tests
 */
export function mockGetSelection(
  text: string
): jest.Mock<Selection | null, []> {
  return jest.fn(() => ({
    toString: () => text,
    rangeCount: text ? 1 : 0,
    getRangeAt: jest.fn(),
    addRange: jest.fn(),
    removeAllRanges: jest.fn(),
    removeRange: jest.fn(),
    type: text ? 'Range' : 'None',
  } as unknown as Selection));
}

/**
 * Mock Docusaurus context for layout tests
 */
export const mockDocusaurusContext = {
  siteConfig: {
    url: 'http://localhost:3000',
    baseUrl: '/',
    title: 'AI Physical Robotics Book',
  },
  isClient: true,
  isBrowser: true,
};

/**
 * Generate mock chat message
 */
export function generateMockChatMessage(
  role: 'user' | 'assistant' = 'user',
  overrides: Partial<ChatMessage> = {}
): ChatMessage {
  const baseMessage: ChatMessage = {
    id: `msg-${Math.random().toString(36).substr(2, 9)}`,
    role,
    content: 'Test message',
    timestamp: new Date().toISOString(),
  };

  return { ...baseMessage, ...overrides };
}

/**
 * Generate mock retrieval source
 */
export function generateMockRetrievalSource(
  overrides: Partial<RetrievalSource> = {}
): RetrievalSource {
  return {
    ...mockRetrievalSource,
    chunk_id: `chunk-${Math.random().toString(36).substr(2, 9)}`,
    ...overrides,
  };
}

/**
 * Generate mock chat response
 */
export function generateMockChatResponse(
  overrides: Partial<ChatResponse> = {}
): ChatResponse {
  return {
    ...mockChatResponse,
    request_id: `550e8400-e29b-41d4-a716-${Math.random().toString(36).substr(2, 12)}`,
    timestamp: new Date().toISOString(),
    ...overrides,
  };
}

/**
 * Setup global fetch mock (for use in test files)
 */
export function setupFetchMock(): jest.Mock {
  const fetchMock = jest.fn();
  global.fetch = fetchMock as any;
  return fetchMock;
}

/**
 * Cleanup global fetch mock
 */
export function cleanupFetchMock(): void {
  delete (global as any).fetch;
}
