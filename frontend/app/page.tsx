import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Upload, Sparkles, Database, Zap } from "lucide-react"
import { Navigation } from "@/components/navigation"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 text-center">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-center mb-6">
            <div className="p-3 bg-primary/10 rounded-full">
              <Sparkles className="h-12 w-12 text-primary" />
            </div>
          </div>
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 text-balance">
            Generate Synthetic Datasets
            <span className="text-primary"> Instantly</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto text-pretty">
            Create high-quality synthetic data from CSV files or text descriptions. Perfect for testing, development,
            and data science projects.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="lg" className="text-lg px-8">
              <Link href="/playground">
                <Zap className="h-5 w-5 mr-2" />
                Start Generating
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="text-lg px-8 bg-transparent">
              <Link href="/about">Learn More</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">Why Choose Datagen?</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Powerful features designed to make synthetic data generation simple and efficient
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="text-center">
              <CardHeader>
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Upload className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Multiple Input Methods</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-pretty">
                  Upload CSV files to extract schemas or describe your dataset needs in plain text. Flexible input
                  options for any workflow.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Database className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>High-Quality Data</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-pretty">
                  Generate realistic, coherent synthetic data that maintains statistical properties and relationships
                  from your source data.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Zap className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Lightning Fast</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-pretty">
                  Generate thousands of rows in seconds. Streaming downloads mean you get your data as soon as it's
                  ready.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="bg-muted/30 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-foreground mb-4">How It Works</h2>
              <p className="text-lg text-muted-foreground">Three simple steps to generate your synthetic dataset</p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6 text-primary-foreground font-bold text-xl">
                  1
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-4">Upload or Describe</h3>
                <p className="text-muted-foreground text-pretty">
                  Upload a CSV file to extract the schema, or describe your desired dataset structure using natural
                  language.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6 text-primary-foreground font-bold text-xl">
                  2
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-4">Configure Generation</h3>
                <p className="text-muted-foreground text-pretty">
                  Set the number of rows (1-100,000) and choose your output format (CSV or JSON) to match your needs.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6 text-primary-foreground font-bold text-xl">
                  3
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-4">Download Instantly</h3>
                <p className="text-muted-foreground text-pretty">
                  Your synthetic dataset is generated and automatically downloaded, ready to use in your projects.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-16 text-center">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold text-foreground mb-4">Ready to Generate Your Data?</h2>
          <p className="text-lg text-muted-foreground mb-8">
            Start creating synthetic datasets in seconds. No signup required.
          </p>
          <Button asChild size="lg" className="text-lg px-8">
            <Link href="/playground">
              <Sparkles className="h-5 w-5 mr-2" />
              Try Datagen Now
            </Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
