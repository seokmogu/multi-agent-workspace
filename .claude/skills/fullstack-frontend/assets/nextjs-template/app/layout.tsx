import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "@/styles/globals.css"
import { Providers } from "./providers"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Company Research Platform",
  description: "AI-powered company research and data extraction",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <div className="min-h-screen bg-background">
            <nav className="border-b">
              <div className="container mx-auto px-4 py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-8">
                    <a href="/" className="text-2xl font-bold text-primary">
                      Research Platform
                    </a>
                    <div className="hidden md:flex space-x-4">
                      <a href="/dashboard" className="text-sm hover:text-primary">
                        Dashboard
                      </a>
                      <a href="/research/new" className="text-sm hover:text-primary">
                        New Research
                      </a>
                      <a href="/history" className="text-sm hover:text-primary">
                        History
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </nav>
            <main className="container mx-auto px-4 py-8">
              {children}
            </main>
          </div>
        </Providers>
      </body>
    </html>
  )
}
