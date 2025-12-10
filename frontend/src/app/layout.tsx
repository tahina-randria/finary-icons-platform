import type { Metadata } from 'next'
import './globals.css'

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
    <html lang="fr" className="dark">
      <body>
        <div className="min-h-screen bg-background">
          <nav className="border-b border-border bg-card/50 backdrop-blur-sm">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-primary">
                  Finary Icons
                </h1>
                <div className="flex gap-6">
                  <a href="/" className="text-foreground hover:text-primary transition-colors">
                    Accueil
                  </a>
                  <a href="/icons" className="text-foreground hover:text-primary transition-colors">
                    Icônes
                  </a>
                  <a href="/generate" className="text-foreground hover:text-primary transition-colors">
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
