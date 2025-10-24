'use client'

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { startResearch } from "@/lib/api"
import { ResearchRequest, ResearchResponse } from "@/lib/types"

export default function NewResearchPage() {
  const [companyName, setCompanyName] = useState('')
  const [userContext, setUserContext] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<ResearchResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  // Default company schema
  const defaultSchema = {
    title: "Company Information",
    type: "object",
    properties: {
      company_name: { type: "string", description: "Official company name" },
      industry: { type: "string", description: "Primary industry or sector" },
      founded_year: { type: "string", description: "Year company was founded" },
      headquarters: { type: "string", description: "Location of headquarters" },
      employee_count: { type: "string", description: "Number of employees" },
      revenue: { type: "string", description: "Annual revenue if available" },
      description: { type: "string", description: "Brief company description" },
      products_services: {
        type: "array",
        items: { type: "string" },
        description: "Main products or services"
      },
      key_executives: {
        type: "array",
        items: { type: "string" },
        description: "Names and titles of key executives"
      }
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const request: ResearchRequest = {
        company_name: companyName,
        extraction_schema: defaultSchema,
        user_context: userContext || undefined,
        max_iterations: 2
      }

      const response = await startResearch(request)
      setResult(response)
    } catch (err: any) {
      setError(err.message || 'Failed to start research')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold">New Research</h1>
        <p className="text-muted-foreground">
          Start a new company research task
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Research Parameters</CardTitle>
          <CardDescription>
            Enter the company name and optional context
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="company-name">Company Name *</Label>
              <Input
                id="company-name"
                placeholder="e.g., Anthropic"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="context">Additional Context (Optional)</Label>
              <Textarea
                id="context"
                placeholder="e.g., Focus on recent funding rounds and AI products"
                value={userContext}
                onChange={(e) => setUserContext(e.target.value)}
                rows={3}
              />
            </div>

            <div className="text-sm text-muted-foreground">
              Using default company schema with fields: company name, industry, founded year,
              headquarters, employees, revenue, description, products, executives
            </div>

            <Button type="submit" disabled={isLoading} className="w-full">
              {isLoading ? 'Researching...' : 'Start Research'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {error && (
        <Card className="border-destructive">
          <CardHeader>
            <CardTitle className="text-destructive">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm">{error}</p>
          </CardContent>
        </Card>
      )}

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>Research Results</CardTitle>
            <CardDescription>
              Completed in {result.iterations} iteration(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">Extracted Data</h4>
                <pre className="bg-muted p-4 rounded-lg overflow-auto text-sm">
                  {JSON.stringify(result.extracted_data, null, 2)}
                </pre>
              </div>

              {result.research_notes && (
                <div>
                  <h4 className="font-semibold mb-2">Research Notes</h4>
                  <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                    {result.research_notes}
                  </p>
                </div>
              )}

              {result.reflection_summary && (
                <div>
                  <h4 className="font-semibold mb-2">Quality Summary</h4>
                  <p className="text-sm text-muted-foreground">
                    {result.reflection_summary}
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
