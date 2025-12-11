/**
 * Type declarations for Docusaurus theme aliases
 * These are resolved by Docusaurus at runtime, not by TypeScript
 */

declare module '@theme-original/Layout' {
  import type { ComponentType } from 'react';
  const Layout: ComponentType<any>;
  export default Layout;
}

declare module '@site/src/components/RAGChatLayout' {
  import type { ComponentType } from 'react';
  const RAGChatLayout: ComponentType<any>;
  export default RAGChatLayout;
}
