import pandas as pd
import os
import sys
from tqdm import tqdm
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

def load_data(file_path):
    """Load the CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def clean_data_for_web_scraping(df):
    """Clean the DataFrame for web scraping purposes."""
    df_cleaned = df.dropna(subset=['Name', 'Website'])
    df_cleaned = df_cleaned[['Name', 'Website']]
    df_cleaned['Emails'] = ""  # Add an empty column for Emails
    return df_cleaned

def clean_data_for_phone_numbers(df):
    """Clean the DataFrame to retain only Name and Phone Number columns, removing rows without phone numbers."""
    df_cleaned = df[['Name', 'Phone Number']].copy()
    df_cleaned = df_cleaned.dropna(subset=['Phone Number'])  # Remove rows without phone numbers
    return df_cleaned

def save_data(df, file_path):
    """Save the cleaned data to a CSV file."""
    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

def main():
    raw_data_directory = 'raw_data'
    processed_files_record = 'processed_files.txt'

    # Load the list of processed files and their processing types
    processed_files = {}
    if os.path.exists(processed_files_record):
        with open(processed_files_record, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(':')
                    filename = parts[0].strip()
                    processing_type = parts[1].strip()
                    if filename in processed_files:
                        processed_files[filename].add(processing_type)
                    else:
                        processed_files[filename] = set([processing_type])
    else:
        processed_files = {}

    # Check the raw_data folder for files
    all_files = [f for f in os.listdir(raw_data_directory) if f.endswith('.csv')]
    # Filter out files that have been processed for both web scraping and phone numbers
    new_files = []
    for f in all_files:
        processed_types = processed_files.get(f, set())
        if len(processed_types) < 2:
            new_files.append(f)

    if new_files:
        input_file = os.path.join(raw_data_directory, new_files[0])
        print(f"Using new file for cleaning: {input_file}")
    else:
        input_file = input("Please enter the path to the CSV file you want to clean: ").strip()

    try:
        # Load data
        raw_data = load_data(input_file)

        # Get the base filename
        base_filename = os.path.basename(input_file)
        # Get the set of processing types already done for this file
        processed_types = processed_files.get(base_filename, set())

        # Determine how to clean the data based on previous
        # Determine how to clean the data based on previous processing
        if "Processed for Web Scraping" in processed_types and "Processed for Phone Numbers" in processed_types:
            print(Fore.YELLOW + "This file has already been processed for both web scraping and phone numbers. Skipping...")
            return

        # Ask user what processing to perform
        print("Processing options:")
        print("1. Web Scraping")
        print("2. Phone Numbers")
        processing_choice = input("Choose processing option (1 or 2): ").strip()

        if processing_choice == '1':
            processing_log = "Processed for Web Scraping"
            if processing_log in processed_types:
                print(Fore.YELLOW + "This file has already been processed for web scraping. Skipping...")
                return
            cleaned_data = clean_data_for_web_scraping(raw_data)
            output_dir = 'cleaned_data/for_web_data'
            file_prefix = 'clean_web_'  # Filename prefix for web scraping
        elif processing_choice == '2':
            processing_log = "Processed for Phone Numbers"
            if processing_log in processed_types:
                print(Fore.YELLOW + "This file has already been processed for phone numbers. Skipping...")
                return
            cleaned_data = clean_data_for_phone_numbers(raw_data)
            output_dir = 'cleaned_data/for_phone_numbers'  # Directory for phone numbers
            file_prefix = 'clean_phone_'  # Prefix for phone number data
        else:
            print("Invalid choice. No data has been processed.")
            return  # Exit the program if no processing is needed

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Prepare the output file path with the new naming convention
        output_file = os.path.join(output_dir, f"{file_prefix}{base_filename}")

        # Show progress bar during saving
        for _ in tqdm(range(1), desc="Saving Data", bar_format='{l_bar}{bar} | {n_fmt}/{total_fmt}'):
            save_data(cleaned_data, output_file)

        # Update processed files log including processing type
        with open(processed_files_record, 'a') as f:
            f.write(f"{base_filename}: {processing_log}\n")

        print(Fore.GREEN + "Data cleaning completed successfully!")

    except FileNotFoundError:
        print(Fore.RED + f"The file {input_file} does not exist. Please check the file path and try again.")
    except KeyboardInterrupt:
        print(Fore.YELLOW + "Program was interrupted. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}. Exiting program.")

if __name__ == "__main__":
    main()
