import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"

export default function Home() {
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-4 py-12">
        <h1 className="text-4xl font-bold tracking-tight">
          AI-Powered Company Research
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Automated web research with structured data extraction.
          Get comprehensive company information in seconds.
        </p>
        <div className="flex gap-4 justify-center pt-4">
          <Link href="/research/new">
            <Button size="lg">Start Research</Button>
          </Link>
          <Link href="/dashboard">
            <Button variant="outline" size="lg">View Dashboard</Button>
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Automated Research</CardTitle>
            <CardDescription>
              Multi-phase research pipeline with web search and data extraction
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>• LLM-powered query generation</li>
              <li>• 8 search provider options</li>
              <li>• Structured JSON extraction</li>
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quality Assurance</CardTitle>
            <CardDescription>
              Reflection loop ensures high-quality results
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>• Completeness scoring</li>
              <li>• Missing field detection</li>
              <li>• Iterative improvement</li>
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Flexible Schemas</CardTitle>
            <CardDescription>
              Customize extraction schema for any use case
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>• Custom field definitions</li>
              <li>• Template library</li>
              <li>• JSON schema support</li>
            </ul>
          </CardContent>
        </Card>
      </div>

      {/* Quick Start */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Start</CardTitle>
          <CardDescription>Get started in 3 simple steps</CardDescription>
        </CardHeader>
        <CardContent>
          <ol className="space-y-4">
            <li className="flex gap-4">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-bold">
                1
              </span>
              <div>
                <h4 className="font-semibold">Enter Company Name</h4>
                <p className="text-sm text-muted-foreground">
                  Provide the name of the company you want to research
                </p>
              </div>
            </li>
            <li className="flex gap-4">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-bold">
                2
              </span>
              <div>
                <h4 className="font-semibold">Select or Customize Schema</h4>
                <p className="text-sm text-muted-foreground">
                  Choose a template or define your own extraction fields
                </p>
              </div>
            </li>
            <li className="flex gap-4">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-bold">
                3
              </span>
              <div>
                <h4 className="font-semibold">Review Results</h4>
                <p className="text-sm text-muted-foreground">
                  Get structured data with sources and confidence scores
                </p>
              </div>
            </li>
          </ol>
          <div className="mt-6">
            <Link href="/research/new">
              <Button>Start Your First Research</Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
