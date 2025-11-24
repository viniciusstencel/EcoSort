import './globals.css';
import { ReactNode } from 'react';

export const metadata = {
  title: 'EcoSort',
  description: 'Projeto Next.js com TailwindCSS e TypeScript',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
