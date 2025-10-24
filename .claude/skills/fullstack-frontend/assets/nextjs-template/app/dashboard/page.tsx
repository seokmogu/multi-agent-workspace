'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useQuery } from "@tanstack/react-query"
import { getStats } from "@/lib/api"

export default function DashboardPage() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['stats'],
    queryFn: getStats,
  })

  if (isLoading) {
    return <div>Loading statistics...</div>
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Error Loading Stats</CardTitle>
          <CardDescription>
            Unable to connect to backend API. Please ensure the backend is running.
          </CardDescription>
        </CardHeader>
      </Card>
    )
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          Overview of your research activity and statistics
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader>
            <CardDescription>Total Jobs</CardDescription>
            <CardTitle className="text-3xl">{stats?.total_jobs || 0}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Success Rate</CardDescription>
            <CardTitle className="text-3xl">
              {stats?.success_rate ? `${(stats.success_rate * 100).toFixed(1)}%` : '0%'}
            </CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Avg Duration</CardDescription>
            <CardTitle className="text-3xl">
              {stats?.avg_duration_seconds ? `${stats.avg_duration_seconds.toFixed(1)}s` : '0s'}
            </CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardDescription>Total Cost</CardDescription>
            <CardTitle className="text-3xl">
              ${stats?.total_cost ? stats.total_cost.toFixed(2) : '0.00'}
            </CardTitle>
          </CardHeader>
        </Card>
      </div>

      {/* Additional Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Last 24 hours</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">Jobs Today</span>
                <span className="font-semibold">{stats?.today_jobs || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">Completed</span>
                <span className="font-semibold text-green-600">
                  {stats?.completed_jobs || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">Failed</span>
                <span className="font-semibold text-red-600">
                  {stats?.failed_jobs || 0}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common tasks</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <a href="/research/new" className="block text-sm text-primary hover:underline">
                → Start New Research
              </a>
              <a href="/history" className="block text-sm text-primary hover:underline">
                → View Research History
              </a>
              <a href="/schemas" className="block text-sm text-primary hover:underline">
                → Manage Schema Templates
              </a>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
