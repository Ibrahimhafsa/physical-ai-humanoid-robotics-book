/**
 * RAGChatLayout Component
 * Wraps the Docusaurus layout to inject the RAG Chat Widget globally
 * This component is used in the swizzled Layout for global widget embedding
 */

import React, { useMemo } from 'react';
import RAGChatWidget from '../RAGChatWidget';
import type { ReactNode } from 'react';

interface RAGChatLayoutProps {
  /** The BaseLayout component from Docusaurus */
  children: ReactNode;
  /**
   * Props passed to the layout component
   * Forwarded from Docusaurus
   */
  [key: string]: any;
}

/**
 * RAGChatLayout - Wraps Docusaurus BaseLayout with RAG Chat Widget
 *
 * This component implements the Docusaurus layout swizzling pattern:
 * 1. Receives the original BaseLayout as children
 * 2. Renders the BaseLayout with the RAGChatWidget overlaid
 * 3. Passes environment-configured API URL to the widget
 *
 * **Swizzling Pattern**:
 * The layout swizzling mechanism in Docusaurus allows us to wrap the entire
 * page layout without modifying Docusaurus core or adding code to every markdown file.
 *
 * This replaces `src/theme/Layout/index.tsx` in the Docusaurus build.
 *
 * **Environment Configuration**:
 * The backend API URL is read from `process.env.REACT_APP_API_URL`.
 * During Docusaurus build, this environment variable is injected into the bundle.
 *
 * @example
 * // In src/theme/Layout/index.tsx (the swizzle point):
 * import BaseLayout from '@theme-original/Layout';
 * import RAGChatLayout from '@site/src/components/RAGChatLayout';
 *
 * export default function Layout(props) {
 *   return <RAGChatLayout {...props}>{BaseLayout(props)}</RAGChatLayout>;
 * }
 */
export const RAGChatLayout: React.FC<RAGChatLayoutProps> = ({
  children,
}) => {
  /**
   * Get API URL from environment
   * Falls back to localhost:8000 if not configured
   */
  const apiUrl = useMemo(() => {
    const envUrl = process.env.REACT_APP_API_URL;
    if (!envUrl) {
      console.warn(
        'REACT_APP_API_URL not configured. Using default: http://localhost:8000/ask'
      );
      return 'http://localhost:8000/ask';
    }
    return envUrl;
  }, []);

  return (
    <>
      {/* Render the original Docusaurus layout */}
      {children}

      {/* Render the RAG Chat Widget globally */}
      <RAGChatWidget
        apiUrl={apiUrl}
        position="bottom-right"
        theme="auto"
        enableTextSelection={true}
        maxMessages={50}
        onError={(error: Error) => {
          console.error('RAGChatWidget error:', error);
        }}
      />
    </>
  );
};

export default RAGChatLayout;
