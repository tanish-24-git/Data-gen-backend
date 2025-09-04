import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Navigation } from "@/components/navigation"
import { Sparkles, Mail, Linkedin, Github, Code, Database, Zap } from "lucide-react"

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <div className="flex justify-center mb-6">
              <div className="p-3 bg-primary/10 rounded-full">
                <Sparkles className="h-12 w-12 text-primary" />
              </div>
            </div>
            <h1 className="text-4xl font-bold text-foreground mb-4 text-balance">About Datagen</h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto text-pretty">
              A modern synthetic dataset generation platform built to simplify data creation for developers, data
              scientists, and researchers.
            </p>
          </div>

          {/* Project Overview */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="h-5 w-5" />
                Project Overview
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">
                Datagen is a full-stack application that bridges the gap between data needs and data availability. By
                leveraging advanced AI techniques, it transforms simple CSV files or text descriptions into
                comprehensive synthetic datasets that maintain statistical integrity while protecting privacy.
              </p>
              <div className="grid md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-muted/30 rounded-lg">
                  <Database className="h-8 w-8 text-primary mx-auto mb-2" />
                  <h4 className="font-semibold text-foreground">Schema Extraction</h4>
                  <p className="text-sm text-muted-foreground">Intelligent CSV analysis</p>
                </div>
                <div className="text-center p-4 bg-muted/30 rounded-lg">
                  <Sparkles className="h-8 w-8 text-primary mx-auto mb-2" />
                  <h4 className="font-semibold text-foreground">AI Generation</h4>
                  <p className="text-sm text-muted-foreground">Realistic synthetic data</p>
                </div>
                <div className="text-center p-4 bg-muted/30 rounded-lg">
                  <Zap className="h-8 w-8 text-primary mx-auto mb-2" />
                  <h4 className="font-semibold text-foreground">Instant Download</h4>
                  <p className="text-sm text-muted-foreground">Streaming file delivery</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Technical Stack */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Technical Stack</CardTitle>
              <CardDescription>Built with modern technologies for performance and scalability</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-foreground mb-3">Frontend</h4>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary">Next.js 14</Badge>
                    <Badge variant="secondary">React</Badge>
                    <Badge variant="secondary">TypeScript</Badge>
                    <Badge variant="secondary">Tailwind CSS</Badge>
                    <Badge variant="secondary">shadcn/ui</Badge>
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold text-foreground mb-3">Backend</h4>
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary">Node.js</Badge>
                    <Badge variant="secondary">API Routes</Badge>
                    <Badge variant="secondary">File Processing</Badge>
                    <Badge variant="secondary">Streaming</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Creator Section */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Created By</CardTitle>
              <CardDescription>Meet the developer behind Datagen</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col md:flex-row gap-6 items-start">
                <div className="w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                  <Code className="h-12 w-12 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-foreground mb-2">Developer</h3>
                  <p className="text-muted-foreground mb-4">
                    A passionate full-stack developer focused on creating tools that solve real-world data challenges.
                    With expertise in modern web technologies and data processing, this project represents a commitment
                    to making synthetic data generation accessible and efficient.
                  </p>
                  <div className="flex flex-wrap gap-3">
                    <Button variant="outline" size="sm" asChild>
                      <a href="mailto:developer@datagen.com" className="flex items-center gap-2">
                        <Mail className="h-4 w-4" />
                        Email
                      </a>
                    </Button>
                    <Button variant="outline" size="sm" asChild>
                      <a
                        href="https://linkedin.com/in/developer"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2"
                      >
                        <Linkedin className="h-4 w-4" />
                        LinkedIn
                      </a>
                    </Button>
                    <Button variant="outline" size="sm" asChild>
                      <a
                        href="https://github.com/developer"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2"
                      >
                        <Github className="h-4 w-4" />
                        GitHub
                      </a>
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Use Cases */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Use Cases</CardTitle>
              <CardDescription>Perfect for various data needs across industries</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-foreground mb-2">Development & Testing</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Application testing with realistic data</li>
                    <li>• Database seeding and migration testing</li>
                    <li>• Performance benchmarking</li>
                    <li>• Demo data for presentations</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold text-foreground mb-2">Data Science & Research</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Algorithm training and validation</li>
                    <li>• Privacy-preserving data sharing</li>
                    <li>• Statistical analysis and modeling</li>
                    <li>• Research dataset augmentation</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Features */}
          <Card>
            <CardHeader>
              <CardTitle>Key Features</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-foreground">Multiple Input Methods</h4>
                    <p className="text-sm text-muted-foreground">CSV upload or natural language descriptions</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-foreground">Flexible Output Formats</h4>
                    <p className="text-sm text-muted-foreground">Generate CSV or JSON files</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-foreground">Scalable Generation</h4>
                    <p className="text-sm text-muted-foreground">From 1 to 100,000 rows on demand</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-foreground">Streaming Downloads</h4>
                    <p className="text-sm text-muted-foreground">Instant file delivery without server storage</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
