import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Finary Icons Platform',
  description: 'AI-powered icon generation platform for Finary motion designers',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
          <nav className="border-b bg-white/80 backdrop-blur-sm">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-slate-900">
                  Finary Icons
                </h1>
                <div className="flex gap-4">
                  <a href="/" className="text-slate-600 hover:text-slate-900">
                    Accueil
                  </a>
                  <a href="/icons" className="text-slate-600 hover:text-slate-900">
                    Icônes
                  </a>
                  <a href="/generate" className="text-slate-600 hover:text-slate-900">
                    Générer
                  </a>
                </div>
              </div>
            </div>
          </nav>
          <main>{children}</main>
        </div>
      </body>
    </html>
  )
}
