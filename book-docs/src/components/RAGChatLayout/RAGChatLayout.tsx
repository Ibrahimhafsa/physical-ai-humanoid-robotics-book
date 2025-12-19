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
 * The backend API URL is determined from:
 * 1. Window.__RAG_API_URL__ (injected by HTML template or build script)
 * 2. process.env.REACT_APP_API_URL (build-time environment variable)
 * 3. Fallback to development default (http://localhost:8000/ask)
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
   * Get API URL from multiple sources (in order of precedence):
   * 1. Window.__RAG_API_URL__ - Set by Docusaurus HTML template or build process
   * 2. process.env.REACT_APP_API_URL - Build-time environment variable
   * 3. Fallback to localhost:8000/ask for local development
   *
   * For production deployments:
   * - Set the API_URL environment variable during build: `API_URL=https://api.example.com/ask npm run build`
   * - Or inject it into the HTML template dynamically before serving
   *
   * Console logs for debugging (only in development):
   */
  const apiUrl = useMemo(() => {
    // Try runtime injection first (set by HTML or build script)
    if (typeof window !== 'undefined' && (window as any).__RAG_API_URL__) {
      const injectedUrl = (window as any).__RAG_API_URL__;
      if (process.env.NODE_ENV === 'development') {
        console.log('[RAGChatWidget] Using injected API URL:', injectedUrl);
      }
      return injectedUrl;
    }

    // Try build-time environment variable
    if (typeof process !== 'undefined' && process.env?.REACT_APP_API_URL) {
      const envUrl = process.env.REACT_APP_API_URL;
      if (process.env.NODE_ENV === 'development') {
        console.log('[RAGChatWidget] Using env API URL:', envUrl);
      }
      return envUrl;
    }

    // Fallback for development
    const fallbackUrl = 'http://localhost:8000';
    if (process.env.NODE_ENV === 'development') {
      console.log('[RAGChatWidget] Using fallback API URL:', fallbackUrl);
    }
    return fallbackUrl;
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
