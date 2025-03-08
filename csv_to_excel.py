#!/usr/bin/env python3
"""
CSV to Excel Converter

This script converts the comparison_table.csv file to an Excel (xlsx) format.
"""

import os
import pandas as pd
from datetime import datetime

def convert_csv_to_excel(csv_file, excel_file=None):
    """
    Convert a CSV file to Excel format.
    
    Args:
        csv_file (str): Path to the input CSV file
        excel_file (str, optional): Path to the output Excel file. 
                                   If not provided, will use the CSV filename with .xlsx extension.
    
    Returns:
        str: Path to the created Excel file
    """
    # Check if CSV file exists
    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    
    # If excel_file is not specified, create one based on the CSV filename
    if not excel_file:
        excel_file = os.path.splitext(csv_file)[0] + '.xlsx'
    
    # Read the CSV file
    try:
        print(f"Reading CSV file: {csv_file}")
        df = pd.read_csv(csv_file)
        
        # Create Excel writer
        print(f"Converting to Excel and saving as: {excel_file}")
        writer = pd.ExcelWriter(excel_file, engine='openpyxl')
        
        # Write the data to Excel
        df.to_excel(writer, index=False, sheet_name='Comparison Table')
        
        # Auto-adjust columns' width
        worksheet = writer.sheets['Comparison Table']
        for idx, col in enumerate(df.columns):
            # Find the maximum length in the column
            max_len = max(
                df[col].astype(str).apply(len).max(),  # Length of data
                len(str(col))  # Length of column name
            ) + 2  # Adding a little extra space
            
            # Set the column width
            worksheet.column_dimensions[chr(65 + idx)].width = max_len
        
        # Save the Excel file
        writer.close()
        
        print(f"Conversion completed successfully!")
        return excel_file
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        csv_file = "comparison_table.csv"
        output_file = f"comparison_table_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        excel_file = convert_csv_to_excel(csv_file, output_file)
        print(f"Excel file created: {excel_file}")
    except Exception as e:
        print(f"Error: {str(e)}") 