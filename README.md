# XML Studies Data Extraction

This project extracts biomedical study information from an XML file and creates a structured pandas DataFrame.

## Description

The `structure_data()` function parses the `studies.xml` file and extracts the following fields for each study:
- **DOI** (Digital Object Identifier) from `<ce:doi>` tag
- **Publication Date** from `<publicationdate>` tag, converted to `YYYY-MM-DD` format
- **Title** from `<titletext>` tag
- **Abstract** from `<ce:para>` tag

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## File Structure

```
.
├── data/
│   └── studies.xml          # XML file with biomedical studies
├── code.py                   # Main script with structure_data() function
├── test_example.py           # Example test script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Usage

```python
from code import structure_data

# Extract data from XML and create DataFrame
output = structure_data()

# View DOI and publication dates
print(output[['doi', 'publication_date']])

# View titles
print(output[['title']])

# View abstracts
print(output[['abstract']])
```

## Output Format

The function returns a pandas DataFrame with the following columns:

| Column            | Type      | Description                                      |
|-------------------|-----------|--------------------------------------------------|
| `doi`             | string    | Digital object identifier                        |
| `publication_date`| string    | Publication date in YYYY-MM-DD format            |
| `title`           | string    | Study title                                      |
| `abstract`        | string    | Study abstract text                              |

## Example

```python
>>> output = structure_data()
>>> output[['doi', 'publication_date']]

                                     doi publication_date
0              10.1007/s00431-007-0495-y       2008-03-09
1                      10.1345/aph.1K303       2008-02-05
2                10.1586/17474108.3.1.33       2008-01-12
...
```

## Testing

Run the test example:

```bash
python3 test_example.py
```

## Data Source

The XML file (`studies.xml`) contains data from a scientific database with information about biomedical studies including metadata, authors, publication details, and abstracts.
