import xmltodict
import pandas as pd
import datetime

def structure_data():
    xml_file_path = 'studies.xml'
    with open(xml_file_path, 'r') as f:
        data = f.read()
    
    # Parse XML to dictionary
    parsed_data = xmltodict.parse(data)
    
    # Extract items from the bibdataset
    items = parsed_data['bibdataset']['item']
    
    # Initialize list to store structured data
    structured_records = []
    
    # Process each item
    for item in items:
        record = {}
        
        # Extract basic identifiers
        bibrecord = item.get('bibrecord', {})
        item_info = bibrecord.get('item-info', {})
        
        # DOI and identifiers
        itemidlist = item_info.get('itemidlist', {})
        if itemidlist:
            record['doi'] = itemidlist.get('ce:doi', None)
            if isinstance(itemidlist.get('itemid'), list):
                for item_id in itemidlist.get('itemid', []):
                    if item_id.get('@idtype') == 'MEDL':
                        record['medline_id'] = item_id.get('#text', None)
                    elif item_id.get('@idtype') == 'PUI':
                        record['pui'] = item_id.get('#text', None)
            elif isinstance(itemidlist.get('itemid'), dict):
                item_id = itemidlist.get('itemid')
                if item_id.get('@idtype') == 'MEDL':
                    record['medline_id'] = item_id.get('#text', None)
                elif item_id.get('@idtype') == 'PUI':
                    record['pui'] = item_id.get('#text', None)
        
        # Head section
        head = bibrecord.get('head', {})
        
        # Title
        citation_title = head.get('citation-title', {})
        titletext = citation_title.get('titletext', {})
        if isinstance(titletext, dict):
            record['title'] = titletext.get('#text', None)
        else:
            record['title'] = titletext
        
        # Citation type
        citation_info = head.get('citation-info', {})
        citation_type = citation_info.get('citation-type', {})
        record['citation_type'] = citation_type.get('@code', None) if isinstance(citation_type, dict) else None
        
        # Authors - get first author and count
        author_groups = head.get('author-group', [])
        if not isinstance(author_groups, list):
            author_groups = [author_groups] if author_groups else []
        
        authors_list = []
        for group in author_groups:
            authors = group.get('author', [])
            if not isinstance(authors, list):
                authors = [authors] if authors else []
            for author in authors:
                surname = author.get('ce:surname', '')
                given_name = author.get('ce:given-name', '')
                if surname or given_name:
                    authors_list.append(f"{surname}, {given_name}".strip(', '))
        
        record['first_author'] = authors_list[0] if authors_list else None
        record['author_count'] = len(set(authors_list))  # Use set to avoid duplicates
        
        # Keywords
        author_keywords = citation_info.get('author-keywords', {})
        keywords = author_keywords.get('author-keyword', [])
        if not isinstance(keywords, list):
            keywords = [keywords] if keywords else []
        record['keywords'] = '; '.join(keywords) if keywords else None
        
        # Abstract
        abstracts = head.get('abstracts', {})
        abstract = abstracts.get('abstract', {})
        if isinstance(abstract, dict):
            ce_para = abstract.get('ce:para', '')
            record['abstract'] = ce_para if isinstance(ce_para, str) else None
        else:
            record['abstract'] = None
        
        # Source information
        source = head.get('source', {})
        record['journal'] = source.get('sourcetitle', None)
        record['journal_abbrev'] = source.get('sourcetitle-abbrev', None)
        record['issn'] = None
        issn = source.get('issn', [])
        if isinstance(issn, list):
            for iss in issn:
                if iss.get('@type') == 'print':
                    record['issn'] = iss.get('#text', None)
                    break
        elif isinstance(issn, dict):
            record['issn'] = issn.get('#text', None)
        
        # Volume and issue
        volisspag = source.get('volisspag', {})
        voliss = volisspag.get('voliss', {})
        record['volume'] = voliss.get('@volume', None) if isinstance(voliss, dict) else None
        record['issue'] = voliss.get('@issue', None) if isinstance(voliss, dict) else None
        
        # Pages
        pagerange = volisspag.get('pagerange', {})
        if isinstance(pagerange, dict):
            record['first_page'] = pagerange.get('@first', None)
            record['last_page'] = pagerange.get('@last', None)
        else:
            record['first_page'] = None
            record['last_page'] = None
        
        # Publication date
        publicationdate = source.get('publicationdate', {})
        if publicationdate:
            year = publicationdate.get('year', None)
            month = publicationdate.get('month', None)
            day = publicationdate.get('day', None)
            
            try:
                if year and month and day:
                    record['publication_date'] = datetime.date(int(year), int(month), int(day))
                elif year and month:
                    record['publication_date'] = datetime.date(int(year), int(month), 1)
                elif year:
                    record['publication_date'] = datetime.date(int(year), 1, 1)
                else:
                    record['publication_date'] = None
            except (ValueError, TypeError):
                record['publication_date'] = None
        else:
            record['publication_date'] = None
        
        record['publication_year'] = source.get('publicationyear', {}).get('@first', None)
        
        # Publisher
        publisher = source.get('publisher', {})
        record['publisher'] = publisher.get('publishername', None)
        
        # Enhancement data
        enhancement = head.get('enhancement', {})
        if enhancement is None:
            enhancement = {}
        
        # Classifications
        classificationgroup = enhancement.get('classificationgroup', {})
        classifications = classificationgroup.get('classifications', {})
        if isinstance(classifications, dict):
            classification_list = classifications.get('classification', [])
            if not isinstance(classification_list, list):
                classification_list = [classification_list] if classification_list else []
            
            class_codes = [c.get('classification-code', '') for c in classification_list]
            record['classification_codes'] = '; '.join(filter(None, class_codes)) if class_codes else None
        else:
            record['classification_codes'] = None
        
        # Bibliography count
        tail = bibrecord.get('tail', {})
        bibliography = tail.get('bibliography', {})
        record['ref_count'] = bibliography.get('@refcount', None) if isinstance(bibliography, dict) else None
        
        structured_records.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(structured_records)
    
    return df


if __name__ == "__main__":
    # Test the function
    df = structure_data()
    print(f"Number of records: {len(df)}")
    print("\nDataFrame columns:")
    print(df.columns.tolist())
    print("\nFirst few rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
    print("\nBasic statistics:")
    print(df.describe(include='all'))
    
    # Save to CSV
    output_file = 'structured_studies.csv'
    df.to_csv(output_file, index=False)
    print(f"\nData saved to '{output_file}'")
    
    # Display some additional insights
    print("\n--- Data Summary ---")
    print(f"Total studies: {len(df)}")
    print(f"Studies with DOI: {df['doi'].notna().sum()}")
    print(f"Studies with abstracts: {df['abstract'].notna().sum()}")
    print(f"Average author count: {df['author_count'].mean():.2f}")
    print(f"\nCitation types:")
    print(df['citation_type'].value_counts())
    print(f"\nTop journals:")
    print(df['journal'].value_counts().head())
