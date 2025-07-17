"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Trash2, Plus, Download, ArrowLeft, Loader2 } from "lucide-react"
import Link from "next/link"
import { useToast } from "@/hooks/use-toast"

interface Column {
  id: string
  name: string
  type: string
  examples: any[]
}

interface GenerateRequest {
  columns: {
    name: string
    type: string
    examples: any[]
  }[]
  row_count: number
}

export default function GeneratePage() {
  const [columns, setColumns] = useState<Column[]>([
    { id: "1", name: "customer_id", type: "integer", examples: [1001, 1002, 1003] },
  ])
  const [rowCount, setRowCount] = useState<number>(100)
  const [isGenerating, setIsGenerating] = useState(false)
  const [newExample, setNewExample] = useState<{ [key: string]: string }>({})
  const { toast } = useToast()

  const addColumn = () => {
    const newColumn: Column = {
      id: Date.now().toString(),
      name: "",
      type: "string",
      examples: [],
    }
    setColumns([...columns, newColumn])
  }

  const removeColumn = (id: string) => {
    setColumns(columns.filter((col) => col.id !== id))
  }

  const updateColumn = (id: string, field: keyof Column, value: any) => {
    setColumns(columns.map((col) => (col.id === id ? { ...col, [field]: value } : col)))
  }

  const addExample = (columnId: string) => {
    const column = columns.find((col) => col.id === columnId)
    if (!column || !newExample[columnId]) return

    let parsedExample: any = newExample[columnId]

    // Parse based on column type
    if (column.type === "integer") {
      parsedExample = Number.parseInt(newExample[columnId])
      if (isNaN(parsedExample)) {
        toast({
          title: "Invalid Example",
          description: "Please enter a valid integer",
          variant: "destructive",
        })
        return
      }
    } else if (column.type === "float") {
      parsedExample = Number.parseFloat(newExample[columnId])
      if (isNaN(parsedExample)) {
        toast({
          title: "Invalid Example",
          description: "Please enter a valid number",
          variant: "destructive",
        })
        return
      }
    }

    updateColumn(columnId, "examples", [...column.examples, parsedExample])
    setNewExample({ ...newExample, [columnId]: "" })
  }

  const removeExample = (columnId: string, index: number) => {
    const column = columns.find((col) => col.id === columnId)
    if (!column) return

    const newExamples = column.examples.filter((_, i) => i !== index)
    updateColumn(columnId, "examples", newExamples)
  }

  const generateDataset = async () => {
  // Validation code remains unchanged
  if (columns.length === 0) {
    toast({ title: "No Columns", description: "Please add at least one column", variant: "destructive" });
    return;
  }
  for (const column of columns) {
    if (!column.name.trim()) {
      toast({ title: "Invalid Column", description: "All columns must have a name", variant: "destructive" });
      return;
    }
    if (column.examples.length === 0) {
      toast({ title: "Missing Examples", description: `Please add at least one example for column "${column.name}"`, variant: "destructive" });
      return;
    }
  }
  if (rowCount < 1 || rowCount > 10000) {
    toast({ title: "Invalid Row Count", description: "Row count must be between 1 and 10,000", variant: "destructive" });
    return;
  }

  setIsGenerating(true);

  try {
    const requestBody: GenerateRequest = {
      columns: columns.map((col) => ({
        name: col.name,
        type: col.type,
        examples: col.examples,
      })),
      row_count: rowCount,
    };

    const response = await fetch("http://localhost:8000/api/v1/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": "x7k9p2m8q3n5r4t6",
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Handle CSV file download
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "synthetic_dataset.csv"; // Match backend filename
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    toast({
      title: "Success!",
      description: `Generated ${rowCount} rows of synthetic data`,
    });
  } catch (error) {
    console.error("Error generating dataset:", error);
    toast({
      title: "Generation Failed",
      description: "Failed to generate dataset. Please check your connection and try again.",
      variant: "destructive",
    });
  } finally {
    setIsGenerating(false);
  }
};

  const convertToCSV = (data: any[]): string => {
    if (data.length === 0) return ""

    const headers = Object.keys(data[0])
    const csvRows = [
      headers.join(","),
      ...data.map((row) =>
        headers
          .map((header) => {
            const value = row[header]
            // Escape commas and quotes in CSV
            if (typeof value === "string" && (value.includes(",") || value.includes('"'))) {
              return `"${value.replace(/"/g, '""')}"`
            }
            return value
          })
          .join(","),
      ),
    ]

    return csvRows.join("\n")
  }

  const downloadCSV = (csvContent: string, filename: string) => {
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" })
    const link = document.createElement("a")
    const url = URL.createObjectURL(blob)
    link.setAttribute("href", url)
    link.setAttribute("download", filename)
    link.style.visibility = "hidden"
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Button variant="ghost" asChild>
              <Link href="/" className="flex items-center space-x-2">
                <ArrowLeft className="h-4 w-4" />
                <span>Back to Home</span>
              </Link>
            </Button>
            <h1 className="text-2xl font-bold">Dataset Generator</h1>
            <div></div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Row Count Configuration */}
          <Card>
            <CardHeader>
              <CardTitle>Dataset Configuration</CardTitle>
              <CardDescription>Configure the basic settings for your synthetic dataset</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="rowCount">Number of Rows</Label>
                  <Input
                    id="rowCount"
                    type="number"
                    min="1"
                    max="10000"
                    value={rowCount}
                    onChange={(e) => setRowCount(Number.parseInt(e.target.value) || 0)}
                    className="max-w-xs"
                  />
                  <p className="text-sm text-gray-500 mt-1">Maximum 10,000 rows per generation</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Column Configuration */}
          <Card>
            <CardHeader>
              <CardTitle>Column Configuration</CardTitle>
              <CardDescription>Define the structure of your dataset by adding columns and examples</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {columns.map((column) => (
                <div key={column.id} className="border rounded-lg p-4 space-y-4">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">Column {columns.indexOf(column) + 1}</h4>
                    {columns.length > 1 && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeColumn(column.id)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor={`name-${column.id}`}>Column Name</Label>
                      <Input
                        id={`name-${column.id}`}
                        value={column.name}
                        onChange={(e) => updateColumn(column.id, "name", e.target.value)}
                        placeholder="e.g., customer_id"
                      />
                    </div>

                    <div>
                      <Label htmlFor={`type-${column.id}`}>Data Type</Label>
                      <Select value={column.type} onValueChange={(value) => updateColumn(column.id, "type", value)}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="string">String</SelectItem>
                          <SelectItem value="integer">Integer</SelectItem>
                          <SelectItem value="float">Float</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label>Examples</Label>
                    <div className="flex flex-wrap gap-2 mb-2">
                      {column.examples.map((example, index) => (
                        <Badge
                          key={index}
                          variant="secondary"
                          className="cursor-pointer"
                          onClick={() => removeExample(column.id, index)}
                        >
                          {String(example)} ×
                        </Badge>
                      ))}
                    </div>
                    <div className="flex gap-2">
                      <Input
                        value={newExample[column.id] || ""}
                        onChange={(e) => setNewExample({ ...newExample, [column.id]: e.target.value })}
                        placeholder={`Add ${column.type} example`}
                        onKeyPress={(e) => {
                          if (e.key === "Enter") {
                            addExample(column.id)
                          }
                        }}
                      />
                      <Button type="button" variant="outline" onClick={() => addExample(column.id)}>
                        Add
                      </Button>
                    </div>
                    <p className="text-sm text-gray-500 mt-1">
                      Provide examples to guide AI generation. Click on examples to remove them.
                    </p>
                  </div>
                </div>
              ))}

              <Button type="button" variant="outline" onClick={addColumn} className="w-full bg-transparent">
                <Plus className="h-4 w-4 mr-2" />
                Add Column
              </Button>
            </CardContent>
          </Card>

          {/* Generate Button */}
          <div className="flex justify-center">
            <Button onClick={generateDataset} disabled={isGenerating} size="lg" className="px-8">
              {isGenerating ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Download className="h-4 w-4 mr-2" />
                  Generate Dataset
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
