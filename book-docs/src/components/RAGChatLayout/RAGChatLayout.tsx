/**
 * RAGChatLayout Component
 * Wraps the Docusaurus layout to inject the RAG Chat Widget globally
 */

import React, { useMemo } from 'react';
import type { ReactNode } from 'react';
import RAGChatWidget from '../RAGChatWidget';

interface RAGChatLayoutProps {
  children: ReactNode;
  [key: string]: any;
}

export const RAGChatLayout: React.FC<RAGChatLayoutProps> = ({ children }) => {
  /**
   * IMPORTANT RULE:
   * - This file must return ONLY the BASE backend URL
   * - NEVER append /ask here
   * - apiClient.ts is responsible for adding /ask
   */

  const apiUrl = useMemo(() => {
    // ✅ Production (injected via docusaurus.config.js scripts)
    if (typeof window !== 'undefined' && (window as any).__RAG_API_URL__) {
      return (window as any).__RAG_API_URL__;
    }

    // ✅ Local development fallback
    return 'http://localhost:8000';
  }, []);

  return (
    <>
      {children}

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
