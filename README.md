# XML Studies Data Structuring

## Overview
This project parses bibliographic XML data from scientific studies and converts it into a structured pandas DataFrame for easier analysis.

## Files
- `code.py` - Main Python script containing the `structure_data()` function
- `studies.xml` - Input XML file containing bibliographic data for 7 scientific studies
- `structured_studies.csv` - Output CSV file with structured data
- `README.md` - This documentation file

## Requirements
```
pandas>=2.0.0
xmltodict>=0.13.0
```

Install dependencies:
```bash
pip install pandas xmltodict
```

## Usage

### Basic Usage
```python
from code import structure_data

# Parse XML and create DataFrame
df = structure_data()

# Access the structured data
print(df.head())
print(df.columns)
```

### Running as Script
```bash
python3 code.py
```

This will:
1. Parse the XML file
2. Create a structured DataFrame
3. Save results to `structured_studies.csv`
4. Display summary statistics

## Data Structure

The `structure_data()` function extracts the following information from each study:

### Identifiers
- `doi` - Digital Object Identifier
- `pui` - Publisher Unique Identifier
- `medline_id` - MEDLINE/PubMed ID

### Bibliographic Information
- `title` - Full title of the study
- `citation_type` - Type of citation (ar=article, re=review, cp=conference paper)
- `first_author` - First author name (format: "Surname, Given Name")
- `author_count` - Total number of unique authors
- `keywords` - Author-provided keywords (semicolon-separated)
- `abstract` - Full abstract text

### Publication Details
- `journal` - Full journal name
- `journal_abbrev` - Abbreviated journal name
- `issn` - International Standard Serial Number
- `volume` - Volume number
- `issue` - Issue number
- `first_page` - Starting page number
- `last_page` - Ending page number
- `publication_date` - Publication date (datetime.date object)
- `publication_year` - Publication year
- `publisher` - Publisher name

### Additional Metadata
- `classification_codes` - Subject classification codes (semicolon-separated)
- `ref_count` - Number of references in bibliography

## Sample Output

### Dataset Statistics
- **Total studies**: 7
- **Studies with DOI**: 7 (100%)
- **Studies with abstracts**: 7 (100%)
- **Average author count**: 3.00

### Citation Types Distribution
- Article (ar): 5 studies
- Review (re): 1 study
- Conference Paper (cp): 1 study

### Top Journals
Each of the 7 studies appears in a different journal, including:
- European Journal of Pediatrics
- Annals of Pharmacotherapy
- Expert Review of Obstetrics and Gynecology
- Colloids and Surfaces A: Physicochemical and Engineering Aspects
- Nephrology
- Journal of the American Chemical Society
- Headache

## Function Details

### `structure_data()`
Parses the XML file `studies.xml` and returns a pandas DataFrame.

**Returns**: 
- `pandas.DataFrame` - Structured data with 21 columns

**Process**:
1. Reads XML file from `studies.xml`
2. Parses XML using xmltodict
3. Extracts bibliographic information from each item
4. Handles missing/optional fields gracefully
5. Formats dates as datetime objects
6. Returns structured DataFrame

**Error Handling**:
- Handles missing or None enhancement data
- Gracefully processes both single and multiple author groups
- Manages various XML structure variations
- Handles missing date components

## Example Data Access

```python
# Load the function
from code import structure_data

# Get structured data
df = structure_data()

# Find studies by keyword
keyword_mask = df['keywords'].str.contains('headache', case=False, na=False)
headache_studies = df[keyword_mask]

# Get studies from specific year
studies_2008 = df[df['publication_year'] == '2008']

# Find studies by author
author_mask = df['first_author'].str.contains('Chang', case=False, na=False)
chang_studies = df[author_mask]

# Export filtered results
filtered_df = df[df['citation_type'] == 'ar']
filtered_df.to_csv('articles_only.csv', index=False)
```

## Notes

- The XML file uses namespaces (ce:, ait:) which are handled by xmltodict
- Author counts are based on unique author names to avoid duplicates from multiple author groups
- Publication dates are parsed to Python datetime.date objects when complete date information is available
- Missing or None values are handled gracefully and stored as None in the DataFrame
- Keywords and classification codes are stored as semicolon-separated strings

## Output Format

The structured data is saved as a CSV file with:
- UTF-8 encoding
- Comma-separated values
- Header row with column names
- No index column

## Troubleshooting

**Issue**: ModuleNotFoundError for pandas or xmltodict
**Solution**: Install required packages: `pip install pandas xmltodict`

**Issue**: FileNotFoundError for studies.xml
**Solution**: Ensure `studies.xml` is in the same directory as `code.py` or update the `xml_file_path` variable

**Issue**: AttributeError with enhancement data
**Solution**: This has been handled in the code by checking for None values before accessing dictionary methods
