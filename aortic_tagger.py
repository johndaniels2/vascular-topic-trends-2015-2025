import pandas as pd
import re
import os

# --- 1. Define your Aortic Disease Keywords ---
# All terms are converted to lowercase for case-insensitive matching.
# r'\b...\b' ensures whole word matching where applicable,
# preventing partial matches (e.g., 'aorta' not matching 'aortitis' unless specifically intended).
# Regular expressions are powerful; you can make them more flexible if needed (e.g., 'aneurysm\w*' to catch 'aneurysms').

aortic_keywords = [
    # Diseases/Conditions
    r'\bacute aortic syndrome\b',
    r'\baortic dissection\b',
    r'\bdissection, abdominal aorta\b',
    r'\babdominal aortic dissection\b',
    r'\bdissection, thoracoabdominal aorta\b',
    r'\bthoracoabdominal aortic dissection\b',
    r'\bdissection, thoracic aorta\b',
    r'\baortic arch dissection\b',
    r'\bdescending aorta dissection\b',
    r'\bdescending thoracic aortic dissection\b',
    r'\bdissection, aortic arch\b',
    r'\bdissection, descending aorta\b',
    r'\bdissection, descending thoracic aorta\b',
    r'\bthoracic aorta dissection\b',
    r'\bthoracic aortic dissection\b',
    r'\baortic intramural hematoma\b',
    r'\bintramural hematoma aorta\b',
    r'\bpenetrating atherosclerotic ulcer\b',
    r'\baortic penetrating ulcer\b',
    r'\bpenetrating aortic ulcer\b',
    r'\bpenetrating ulcer\b', # Be cautious: 'penetrating ulcer' alone can be general. Consider if context is needed.
    r'\bpenetrating ulcer aorta\b',
    r'\baortic aneurysm\b',
    r'\baortic aneurysm, abdominal\b',
    r'\babdominal aorta aneurysm\b',
    r'\babdominal aortic aneurysm\b',
    r'\baneurysm, abdominal aorta\b',
    r'\baneurysm, abdominal aortic\b',
    r'\baortic aneurysm, thoracoabdominal\b',
    r'\btaa thoracoabdominal aortic aneurysm\b',
    r'\bthoracoabdominal aortic aneurysm\b',
    r'\baortic aneurysm, thoracic\b',
    r'\baneurysm, aortic arch\b',
    r'\baortic arch aneurysm\b',
    r'\baortic root aneurysm\b',
    r'\baneurysm, aortic root\b',
    r'\baneurysm, ascending aorta\b',
    r'\baaa ascending aorta aneurysm\b',
    r'\bascending aorta aneurysm\b',
    r'\bascending aortic aneurysm\b',
    r'\bdescending thoracic aortic aneurysm\b',
    r'\baneurysm, descending thoracic aorta\b',
    r'\baneurysm, thoracic aorta\b',
    r'\baneurysm, thoracic aortic\b',
    r'\bthoracic aorta aneurysm\b',
    r'\bthoracic aortic aneurysm\b',
    r'\baortic rupture\b',
    r'\baortic aneurysm, ruptured\b',
    r'\bruptured aortic aneurysm\b',
    r'\bloeys-dietz syndrome\b',
    r'\bloeys-dietz aortic aneurysm syndrome\b',
    r'\bloeys-dietz syndrome, type 1a\b',
    r'\bmarfan syndrome\b',
    r'\baortic arch syndromes\b',
    r'\btakayasu arteritis\b',
    r'\baortitis syndrome\b',
    r'\barteritis, takayasu\'?s\b', # Added '?' for optional apostrophe
    r'\bpulseless disease\b',
    r'\btakayasu disease\b',
    r'\btakayasu syndrome\b',
    r'\btakayasu\'?s arteritis\b', # Added '?' for optional apostrophe
    r'\byoung female arteritis\b',
    r'\bvascular ring\b',
    r'\bdouble aortic arch\b',
    r'\bright aortic arch syndrome\b',
    r'\bright aortic arch with left ligamentum arteriosum\b',
    r'\baortitis\b',
    r'\bleriche\'?s syndrome\b', # Added '?' for optional apostrophe
    r'\baortic valve disease\b', # Added as per your last list
    
    # Procedures related to Aortic Disease (expanded and specific)
    r'\baortic aneurysm repair\b', # Direct match
    r'\baortocaval fistula repair\b', # Specific to aorta
    r'\baortoenteric fistula repair\b', # Specific to aorta
    r'\bceliac artery bypass\b', # Major aortic branch
    r'\bmesenteric artery bypass\b', # Major aortic branch
    r'\brenal artery bypass\b', # Major aortic branch
    r'\brenal artery endarterectomy\b', # Major aortic branch
    r'\bstenting to repair aneurysms\b', # Often aortic
    r'\bvascular stenting\b', # Broad, but can be aortic, consider context.
                               # For this model, if it appears with "aortic" elsewhere, it's covered.
                               # Otherwise, it will just tag if 'vascular stenting' is literally in title
    
    # Acronyms and specific procedures from previous discussions
    r'\bbevar\b', # Branched Endovascular Aneurysm Repair
    r'\bbranched endovascular aneurysm repair\b',
    r'\bendovascular aortic repair\b',
    r'\bendovascular stent grafting\b',
    r'\bfevar\b', # Fenestrated Endovascular Aneurysm Repair
    r'\bfenestrated endovascular aneurysm repair\b',
    r'\btevar\b', # Thoracic Endovascular Aneurysm Repair / Aortic Repair
    r'\bthoracic endovascular aneurysm repair\b',
    r'\bthoracic endovascular aortic repair\b',
    r'\bthoracic endovascular repair\b',
    r'\bopen aortic repair\b',
    r'\bhybrid aortic repair\b',
    r'\bdebranching\b', # Often associated with aortic arch procedures
    r'\baortic reconstruction\b',
    r'\baortic surgery\b',
    r'\baortic repair\b',
    r'\baortic replacement\b',
    r'\baortic graft\b',
    r'\baortography\b',
    r'\bspinal cord ischemia\b' # Common complication of aortic surgery
]

# Compile all regex patterns for efficiency
compiled_aortic_patterns = [re.compile(pattern) for pattern in aortic_keywords]

# --- 2. Categorization Function ---
def categorize_title_as_aortic(title):
    """
    Checks if a given title contains any of the defined aortic disease keywords.

    Args:
        title (str): The research title to categorize.

    Returns:
        str: 'Aortic Disease' if any keyword is found, 'Other' otherwise.
    """
    if not isinstance(title, str):
        return 'Other' # Handle non-string titles (e.g., empty cells)

    title_lower = title.lower()
    
    for pattern in compiled_aortic_patterns:
        if pattern.search(title_lower):
            return 'Aortic Disease'
            
    return 'Other'

# --- 3. Main Script Execution ---
if __name__ == "__main__":
    # Define your input and output file names
    # IMPORTANT: Export your Google Sheet to a CSV file first and place it in the same directory as this script.
    # Make sure your titles are in a column named 'Title' or adjust 'title_column_name' below.
    input_csv_filename = 'your_titles.csv'  # <--- RENAME THIS TO YOUR CSV FILE NAME
    output_csv_filename = 'categorized_vascular_titles.csv' # Output file

    # --- Instructions for Google Sheets Export ---
    # 1. Open your Google Sheet.
    # 2. Go to File > Download > Comma Separated Values (.csv) or Microsoft Excel (.xlsx).
    # 3. Save the downloaded file to the same folder where you saved this Python script.
    # 4. If you download as .xlsx, change `pd.read_csv` to `pd.read_excel` below,
    #    and ensure you specify the sheet name if needed (e.g., `sheet_name='Sheet1'`).

    # Check if the input file exists
    if not os.path.exists(input_csv_filename):
        print(f"Error: Input file '{input_csv_filename}' not found.")
        print("Please export your Google Sheet as a CSV or XLSX and place it in the same directory.")
        print("Remember to rename the file to match 'input_csv_filename' in the script if necessary.")
    else:
        print(f"Loading titles from '{input_csv_filename}'...")
        try:
            # Load the data
            # Adjust 'header=0' if your first row is not the header
            # If using .xlsx: df = pd.read_excel(input_csv_filename, engine='openpyxl')
            df = pd.read_csv(input_csv_filename)

            # Assuming your column with titles is named 'Title'
            # If your column has a different name (e.g., 'Meeting Abstract Title'), change this:
            title_column_name = 'Title' # <--- ADJUST THIS IF YOUR TITLE COLUMN HAS A DIFFERENT NAME

            if title_column_name not in df.columns:
                print(f"Error: Column '{title_column_name}' not found in your CSV.")
                print("Please check your CSV file's column names or adjust 'title_column_name' in the script.")
            else:
                # Apply the categorization function
                print("Categorizing titles...")
                df['Aortic Disease Category'] = df[title_column_name].apply(categorize_title_as_aortic)

                # Save the results to a new CSV file
                df.to_csv(output_csv_filename, index=False)
                print(f"Categorization complete! Results saved to '{output_csv_filename}'")
                print("\nHere's a preview of the categorization:")
                print(df[[title_column_name, 'Aortic Disease Category']].head(10)) # Show first 10 rows

                print("\nValue counts for the 'Aortic Disease Category':")
                print(df['Aortic Disease Category'].value_counts())

        except Exception as e:
            print(f"An error occurred during file processing: {e}")
            print("Please ensure your CSV/XLSX file is correctly formatted and not open in another program.")
