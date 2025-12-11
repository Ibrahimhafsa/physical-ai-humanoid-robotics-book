/**
 * Swizzled Docusaurus Layout Component
 *
 * This file swizzles the Docusaurus theme layout to inject the RAG Chat Widget globally.
 *
 * **Swizzling Pattern**:
 * Docusaurus allows theme customization via swizzling. By creating a file at
 * `src/theme/Layout/index.tsx`, we override the default layout without modifying
 * Docusaurus core or theme packages.
 *
 * **How it works**:
 * 1. Import the original Layout component using @theme-original
 * 2. Wrap it with our RAGChatLayout component
 * 3. The RAGChatLayout renders both the original layout and the widget
 * 4. The widget appears on every page automatically
 *
 * **No per-page changes needed**:
 * This single file handles global widget embedding for all pages.
 * Markdown files and other components don't need any modifications.
 *
 * @see https://docusaurus.io/docs/advanced/swizzling
 * @see src/components/RAGChatLayout/RAGChatLayout.tsx
 */

import Layout from '@theme-original/Layout';
import RAGChatLayout from '@site/src/components/RAGChatLayout';

/**
 * Wrapped Layout component
 *
 * This replaces the default Docusaurus layout for all pages.
 * All props are forwarded to both the original Layout and our wrapper.
 */
export default function LayoutWrapper(props: any): JSX.Element {
  return (
    <RAGChatLayout {...props}>
      <Layout {...props} />
    </RAGChatLayout>
  );
}
