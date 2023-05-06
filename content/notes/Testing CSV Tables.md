---
title: "Testing CSV Tables"
tags:
- datasets
- csv
---

This is a test note. I'm going to refer to it from the main page.

# CSV Partial
I added a [Hugo HTML Partial](https://gohugo.io/templates/partials/) to `./layouts/partials` for displaying data in a `.csv` format. I'm going to use it now to see if it works and what it appears on the page as:

{{< csv-table csvFilePath="notes/csv/avalanche-danger-ratings-april-2023.csv" >}}