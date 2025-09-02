import pandas as pd



# Load the Excel file
df = pd.read_csv('/Users/shiva/Downloads/MinStaffingComments.csv')


#converts all text to lowercase
df['bin1_cleaned'] = df['Comment'].str.lower().str.replace(r'[^\w\s]', ' ')

#Removes punctuation and special charecters
df['bin1_cleaned'] = df['bin1_cleaned'].str.replace(r'[^\w\s]', '', regex=True)


# Print the first few rows to inspect the data
print(df.head())

# Check for missing values and general information about the DataFrame
print(df.info())

#getting rid of missing values:
df.dropna(subset=['Comment'], inplace=True)

bin1_keywords = ['social', 'mental']
df['bin1'] = df['bin1_cleaned'].apply(lambda x: any(keyword in x for keyword in bin1_keywords))

# Create a DataFrame with all comments that fall into Bin 1
bin1 = df[df['bin1']]
print(bin1.head())

bin1.to_csv('/Users/shiva/Desktop/bin1_comments.csv', index=False)


template_keywords = {
    'Staffing Standards Bin': ['minimum staffing', 'staffing standards', 'nurse staffing', 'staff shortages', 'staff ratios'],
    'Dear Administrator Bin': ['dear administrator', 'to whom it may concern', 'as an administrator', 'facility management', 'administrator request'],
    'Social Worker Bin': ['social worker', 'mental health', 'social services', 'interdisciplinary team', 'psychosocial needs'],
    'Long Term Care Bin': ['long term care', 'nursing homes', 'skilled nursing facility', 'elder care', 'geriatric care']
}
# Function to check if a comment matches a template based on keywords
def matches_template(comment, keywords):
    return any(keyword in comment for keyword in keywords)

# For each template (bin), create a new column in the DataFrame indicating if the comment matches that bin
for template, keywords in template_keywords.items():
    # Apply the matching function and create new columns
    bin1[template] = bin1['bin1_cleaned'].apply(lambda x: matches_template(x, keywords))



# Save the results to a new CSV file
output_file = '/Users/shiva/Desktop/bin1_classified_with_5_bins.csv'
bin1.to_csv(output_file, index=False)

# Re-read the CSV to confirm changes
bin1_reloaded = pd.read_csv(output_file)


# Check if the file was saved successfully
print(f"File saved to: {output_file}")