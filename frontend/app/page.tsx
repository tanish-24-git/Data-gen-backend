import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Database, Zap, Shield, Download } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Database className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">DataGen Pro</h1>
            </div>
            <nav className="hidden md:flex items-center space-x-6">
              <Link href="#features" className="text-gray-600 hover:text-gray-900">
                Features
              </Link>
              <Link href="#how-it-works" className="text-gray-600 hover:text-gray-900">
                How it Works
              </Link>
              <Button asChild>
                <Link href="/generate">Get Started</Link>
              </Button>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            Generate Synthetic Datasets
            <span className="text-blue-600"> Instantly</span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Create realistic, customizable synthetic datasets for testing, development, and analysis. Powered by AI and
            designed for developers who need quality data fast.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="lg" className="text-lg px-8 py-3">
              <Link href="/generate">Start Generating</Link>
            </Button>
            <Button variant="outline" size="lg" className="text-lg px-8 py-3 bg-transparent">
              <Link href="#how-it-works">Learn More</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">Why Choose DataGen Pro?</h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our platform combines the power of AI with intuitive design to deliver the best synthetic data generation
              experience.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Card className="text-center">
              <CardHeader>
                <Zap className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                <CardTitle>Lightning Fast</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Generate thousands of rows of synthetic data in seconds with our optimized AI engine.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Database className="h-12 w-12 text-green-600 mx-auto mb-4" />
                <CardTitle>Flexible Schema</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Define custom columns with different data types and provide examples for AI-guided generation.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Shield className="h-12 w-12 text-purple-600 mx-auto mb-4" />
                <CardTitle>Privacy First</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  All data is generated synthetically. No real user data is stored or processed.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <Download className="h-12 w-12 text-orange-600 mx-auto mb-4" />
                <CardTitle>Easy Export</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Download your generated datasets as CSV files, ready for immediate use in your projects.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">How It Works</h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">Generate synthetic datasets in three simple steps</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-600 text-white rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                1
              </div>
              <h4 className="text-xl font-semibold mb-4">Define Your Schema</h4>
              <p className="text-gray-600">
                Specify column names, data types, and provide examples to guide the AI generation process.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-green-600 text-white rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                2
              </div>
              <h4 className="text-xl font-semibold mb-4">Set Row Count</h4>
              <p className="text-gray-600">
                Choose how many rows of data you need, from a few dozen to thousands of records.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-purple-600 text-white rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-6">
                3
              </div>
              <h4 className="text-xl font-semibold mb-4">Generate & Download</h4>
              <p className="text-gray-600">
                Our AI generates realistic data based on your specifications and delivers it as a CSV file.
              </p>
            </div>
          </div>

          <div className="text-center mt-12">
            <Button asChild size="lg">
              <Link href="/generate">Try It Now</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Database className="h-6 w-6" />
              <span className="text-lg font-semibold">DataGen Pro</span>
            </div>
            <div className="text-gray-400">© 2024 DataGen Pro. All rights reserved.</div>
          </div>
        </div>
      </footer>
    </div>
  )
}
