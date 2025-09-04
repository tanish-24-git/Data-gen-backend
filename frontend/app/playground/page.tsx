"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Upload, FileText, Download, Sparkles } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { Navigation } from "@/components/navigation"

export default function PlaygroundPage() {
  const [file, setFile] = useState<File | null>(null)
  const [prompt, setPrompt] = useState("")
  const [numRows, setNumRows] = useState(1000)
  const [format, setFormat] = useState("csv")
  const [isGenerating, setIsGenerating] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const { toast } = useToast()

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0]
    if (selectedFile && selectedFile.type === "text/csv") {
      setFile(selectedFile)
      toast({
        title: "File uploaded successfully",
        description: `${selectedFile.name} is ready for processing.`,
      })
    } else {
      toast({
        title: "Invalid file type",
        description: "Please upload a CSV file.",
        variant: "destructive",
      })
    }
  }

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault()
  }

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault()
    const droppedFile = event.dataTransfer.files[0]
    if (droppedFile && droppedFile.type === "text/csv") {
      setFile(droppedFile)
      toast({
        title: "File uploaded successfully",
        description: `${droppedFile.name} is ready for processing.`,
      })
    } else {
      toast({
        title: "Invalid file type",
        description: "Please upload a CSV file.",
        variant: "destructive",
      })
    }
  }

  const handleGenerate = async () => {
    if (!file && !prompt.trim()) {
      toast({
        title: "Missing input",
        description: "Please upload a CSV file or enter a dataset description.",
        variant: "destructive",
      })
      return
    }

    setIsGenerating(true)

    try {
      const formData = new FormData()

      if (file) {
        formData.append("file", file)
      }

      if (prompt.trim()) {
        formData.append("prompt", prompt.trim())
      }

      formData.append("num_rows", numRows.toString())
      formData.append("format", format)

      const response = await fetch("/api/generate-dataset", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Failed to generate dataset")
      }

      // Extract filename from Content-Disposition header
      const contentDisposition = response.headers.get("Content-Disposition")
      const filename = contentDisposition?.match(/filename=(.+)/)?.[1] || `dataset.${format}`

      // Create blob and trigger download
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

      toast({
        title: "Dataset generated successfully",
        description: `Your ${format.toUpperCase()} file has been downloaded.`,
      })
    } catch (error) {
      console.error("Error generating dataset:", error)
      toast({
        title: "Generation failed",
        description: "There was an error generating your dataset. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4 text-balance">
              Create Synthetic Datasets Instantly
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
              Upload a CSV file to extract schema or describe your dataset needs. Generate high-quality synthetic data
              in seconds.
            </p>
          </div>

          {/* How It Works Section */}
          <div className="mb-12">
            <h3 className="text-2xl font-bold text-foreground text-center mb-8">How It Works</h3>
            <div className="grid md:grid-cols-3 gap-6">
              <Card className="text-center">
                <CardContent className="pt-6">
                  <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Upload className="h-6 w-6 text-primary" />
                  </div>
                  <h4 className="font-semibold text-foreground mb-2">1. Upload or Describe</h4>
                  <p className="text-sm text-muted-foreground text-pretty">
                    Upload a CSV file to extract the schema, or describe your desired dataset structure in plain text.
                  </p>
                </CardContent>
              </Card>

              <Card className="text-center">
                <CardContent className="pt-6">
                  <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Sparkles className="h-6 w-6 text-primary" />
                  </div>
                  <h4 className="font-semibold text-foreground mb-2">2. Configure & Generate</h4>
                  <p className="text-sm text-muted-foreground text-pretty">
                    Set the number of rows and output format (CSV or JSON), then let our AI generate realistic synthetic
                    data.
                  </p>
                </CardContent>
              </Card>

              <Card className="text-center">
                <CardContent className="pt-6">
                  <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Download className="h-6 w-6 text-primary" />
                  </div>
                  <h4 className="font-semibold text-foreground mb-2">3. Download Instantly</h4>
                  <p className="text-sm text-muted-foreground text-pretty">
                    Your synthetic dataset is generated and automatically downloaded to your device, ready to use.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Main Form Grid */}
          <div className="grid lg:grid-cols-2 gap-8">
            {/* Left Column - File Upload */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="h-5 w-5" />
                  Upload CSV File
                </CardTitle>
                <CardDescription>Upload a CSV file to extract the schema for synthetic data generation</CardDescription>
              </CardHeader>
              <CardContent>
                <div
                  className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  {file ? (
                    <div>
                      <p className="text-sm font-medium text-foreground">{file.name}</p>
                      <p className="text-xs text-muted-foreground mt-1">{(file.size / 1024).toFixed(1)} KB</p>
                    </div>
                  ) : (
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">
                        Drop your CSV file here or click to browse
                      </p>
                      <p className="text-xs text-muted-foreground">Supports CSV files up to 10MB</p>
                    </div>
                  )}
                </div>
                <input ref={fileInputRef} type="file" accept=".csv" onChange={handleFileUpload} className="hidden" />

                <div className="mt-6">
                  <div className="absolute inset-0 flex items-center">
                    <span className="w-full border-t border-border" />
                  </div>
                  <div className="relative flex justify-center text-xs uppercase">
                    <span className="bg-background px-2 text-muted-foreground">Or</span>
                  </div>
                </div>

                <div className="mt-6">
                  <Label htmlFor="prompt" className="text-sm font-medium">
                    Describe Your Dataset
                  </Label>
                  <Textarea
                    id="prompt"
                    placeholder="e.g., Customer data with name, email, age, purchase history, and preferences"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    className="mt-2 min-h-[100px]"
                  />
                  <p className="text-xs text-muted-foreground mt-2">
                    Describe the columns and data types you want in your synthetic dataset
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Right Column - Configuration */}
            <Card>
              <CardHeader>
                <CardTitle>Dataset Configuration</CardTitle>
                <CardDescription>Configure the output format and size of your synthetic dataset</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <Label htmlFor="num-rows" className="text-sm font-medium">
                    Number of Rows
                  </Label>
                  <Input
                    id="num-rows"
                    type="number"
                    min="1"
                    max="100000"
                    value={numRows}
                    onChange={(e) => setNumRows(Number.parseInt(e.target.value) || 1000)}
                    className="mt-2"
                  />
                  <p className="text-xs text-muted-foreground mt-2">Generate between 1 and 100,000 rows</p>
                </div>

                <div>
                  <Label htmlFor="format" className="text-sm font-medium">
                    Output Format
                  </Label>
                  <Select value={format} onValueChange={setFormat}>
                    <SelectTrigger className="mt-2">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="csv">CSV</SelectItem>
                      <SelectItem value="json">JSON</SelectItem>
                    </SelectContent>
                  </Select>
                  <p className="text-xs text-muted-foreground mt-2">Choose your preferred file format for download</p>
                </div>

                <div className="pt-4">
                  <Button
                    onClick={handleGenerate}
                    disabled={isGenerating || (!file && !prompt.trim())}
                    className="w-full"
                    size="lg"
                  >
                    {isGenerating ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-foreground mr-2" />
                        Generating Dataset...
                      </>
                    ) : (
                      <>
                        <Download className="h-4 w-4 mr-2" />
                        Generate Dataset
                      </>
                    )}
                  </Button>
                </div>

                {(file || prompt.trim()) && (
                  <div className="bg-muted/50 rounded-lg p-4 mt-4">
                    <h4 className="text-sm font-medium text-foreground mb-2">Preview</h4>
                    <div className="text-xs text-muted-foreground space-y-1">
                      <p>
                        <strong>Input:</strong> {file ? `File: ${file.name}` : "Text prompt"}
                      </p>
                      <p>
                        <strong>Rows:</strong> {numRows.toLocaleString()}
                      </p>
                      <p>
                        <strong>Format:</strong> {format.toUpperCase()}
                      </p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}
