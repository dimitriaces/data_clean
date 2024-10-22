# Data Clean App

## Overview
The `data_clean` app is designed to process and clean data related to businesses, primarily focused on the vaping and smoke industry. This application simplifies the task of preparing data for analysis or web scraping, ensuring that only the relevant information is retained.

## Data Types Processed
The app cleans data that typically includes the following fields:
- **Business Name**: The name of the vape shop or business.
- **Website**: The official website URL of the business.
- **Address**: Full address of the business including street, city, state, and postal code.
- **Phone Number**: Contact numbers for reaching the business.
- **Operational Hours**: Information on when the business is open.
- **Ratings**: Customer ratings based on review aggregations.
- **Reviews**: Customer feedback and comments about their experiences.

## Cleaning Processes
The `data_clean` app performs the following cleaning operations:

1. **Row Validation**: 
   - Removes any rows that do not have both 'Name' and 'Website', ensuring that only valid entries are processed.

2. **Column Filtering**: 
   - When the data is designated for web scraping, the app retains only the following columns:
     - `Name`
     - `Website`
     - `Emails` (added as an empty column for future use)

3. **Empty Column Initialization**:
   - Adds an 'Emails' column initialized to blank for convenience, allowing for future email scraping tasks.

4. **Output Configuration**:
   - Depending on the user's response regarding the purpose of the data cleaning, the app prefixes the output filenames to distinguish between cleaned data for web scraping and for other uses:
     - For web scraping, files are prefixed with `clean_web_`.
     - For other purposes, files are prefixed with `cleaned_`.

## Saving Process
The cleaned data is saved in designated directories based on the user's choice:
- For web scraping: `cleaned_data/for_web_data`
- For other processes: `cleaned_data/processed_data`

The data is saved in CSV format with an append mode, allowing new entries to be added without overwriting existing files.

## Usage
1. **Installation Requirements**:
   - Ensure that you have the required libraries installed:
     ```bash
     pip install pandas tqdm colorama
     ```
   
2. **Running the App**:
   - You can execute the app via the command line:
     ```bash
     python data_clean.py
     ```

3. **Follow Prompts**:
   - The application will guide you through selecting a CSV file to clean, and whether the data is intended for web scraping.

## Contribution
Contributions to improve the `data_clean` app are welcome. Feel free to fork the repository and submit pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details. 
