---
draft: true
---

I wanted to use a [Hugo HTML Partial Template](https://gohugo.io/templates/partials/) to handle displaying a `.csv` file as a table.

I asked ChatGPT for some advice on how to do that, and this was the response:

# How do you use an HTML partial to display a `.csv` file of tabular data?
Here's an example of how you can create a Hugo HTML partial that displays a CSV file as a table with the file path passed in as a parameter.

1. Create a new file named "csv-table.html" in your "layouts/partials" directory.
2. In the "csv-table.html" file, add the following code:

```go
{{- $csvFilePath := .csvFilePath }}
{{- $csvContent := readFile $csvFilePath }}
{{- $csvLines := split $csvContent "\n" }}
<table>
{{- range $index, $line := $csvLines }}
    <tr>
    {{- $cells := split $line "," }}
    {{- range $index2, $cell := $cells }}
        <td>{{ $cell }}</td>
    {{- end }}
    </tr>
{{- end }}
</table>
```

3. Save the file and commit the changes to your Hugo project repository.
4. In your Markdown file, you can now use the following shortcode to display the CSV file as a table:

```go
{{< csv-table csvFilePath="path/to/your/csv/file.csv" >}}
```

Here, "path/to/your/csv/file.csv" should be replaced with the actual file path of your CSV file.

This shortcode passes the file path to the "csv-table.html" partial as a parameter named "csvFilePath". The partial reads the contents of the CSV file, splits the lines and cells, and generates HTML code for the table.


# See Also
- [Hugo]()


#hugo #chatgpt #quartz #obsidian 