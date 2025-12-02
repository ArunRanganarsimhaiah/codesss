import xmltodict
import pandas as pd
from datetime import datetime


def structure_data():
    """
    Extract fields from studies.xml and create a structured dataframe.
    
    Returns:
        pd.DataFrame: A dataframe with columns: doi, publication_date, title, abstract
    """
    # Read the XML file
    with open('./data/studies.xml', 'r', encoding='utf-8') as file:
        xml_content = file.read()
    
    # Parse XML to dictionary
    data_dict = xmltodict.parse(xml_content)
    
    # Extract items from the dataset
    items = data_dict['bibdataset']['item']
    
    # If items is not a list (single item), make it a list
    if not isinstance(items, list):
        items = [items]
    
    # Lists to store extracted data
    doi_list = []
    publication_date_list = []
    title_list = []
    abstract_list = []
    
    # Process each item
    for item in items:
        try:
            # Extract DOI from <ce:doi> tag
            bibrecord = item.get('bibrecord', {})
            item_info = bibrecord.get('item-info', {})
            itemidlist = item_info.get('itemidlist', {})
            doi = itemidlist.get('ce:doi', '')
            
            # Extract publication date and convert to YYYY-MM-DD format
            head = bibrecord.get('head', {})
            source = head.get('source', {})
            pub_date = source.get('publicationdate', {})
            
            if pub_date:
                year = pub_date.get('year', '')
                month = pub_date.get('month', '01')
                day = pub_date.get('day', '01')
                
                # Pad month and day with zeros if needed
                month = str(month).zfill(2)
                day = str(day).zfill(2)
                
                publication_date = f"{year}-{month}-{day}"
            else:
                publication_date = ''
            
            # Extract title from <titletext> tag
            citation_title = head.get('citation-title', {})
            title = citation_title.get('titletext', '')
            
            # If titletext is a dict (has attributes), get the text content
            if isinstance(title, dict):
                title = title.get('#text', '')
            
            # Extract abstract from <ce-para> tag
            abstracts = head.get('abstracts', {})
            abstract = abstracts.get('abstract', {})
            ce_para = abstract.get('ce:para', '')
            
            # Append to lists
            doi_list.append(doi)
            publication_date_list.append(publication_date)
            title_list.append(title)
            abstract_list.append(ce_para)
            
        except Exception as e:
            print(f"Error processing item: {e}")
            continue
    
    # Create dataframe
    df = pd.DataFrame({
        'doi': doi_list,
        'publication_date': publication_date_list,
        'title': title_list,
        'abstract': abstract_list
    })
    
    # Convert publication_date to datetime type
    df['publication_date'] = pd.to_datetime(df['publication_date'], format='%Y-%m-%d')
    
    return df
