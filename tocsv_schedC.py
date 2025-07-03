import os
import csv
import xml.etree.ElementTree as ET

# Set your folder path
folder_path = '2021_TEOS_XML'
output_csv = '2021schedC_all.csv'

# Define namespaces
ns = {
    'irs': 'http://www.irs.gov/efile',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# List to collect all rows
rows = []

# Header for CSV
header = [
    'ID', 'FilerEIN', 'BusinessNameLine1Txt', 'BusinessNameControlTxt',
    'PoliticalExpendituresAmt', 'VolunteerHoursCnt', 'FormAndLineReferenceDesc', 'ExplanationTxt'
]

# Parse each XML file
def process_folder(folder_path):
    print(f"Processing folder {folder_path}...")
    for root_dir, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.xml'):
                filepath = os.path.join(root_dir, filename)
                try:
                    tree = ET.parse(filepath)
                except ET.ParseError as e:
                    print(f"Skipping file {filename} due to parsing error: {e}")
                    continue  # or handle it differently
                root = tree.getroot()

                def find(path):
                    return root.find(path, ns)

                def findtext(path):
                    el = root.find(path, ns)
                    return el.text if el is not None else ''
                
                # Extract ReturnTypeCd first
                return_type_cd = findtext('.//irs:ReturnTypeCd')
                irs_return_tag = f"irs:IRS{return_type_cd}"  # e.g., 'irs:IRS990EZ'

                # Helper to find a child inside the dynamic IRS tag
                def find_in_return_tag(tag_name):
                    return root.find(f'.//{irs_return_tag}/irs:{tag_name}', ns)

                def findtext_in_return_tag(tag_name):
                    el = find_in_return_tag(tag_name)
                    return el.text if el is not None else ''
                
                def extract_id_from_filename(filename):
                    basename = os.path.basename(filename)
                    if '_public.xml' in basename:
                        return basename.split('_public.xml')[0]
                    return ''
                schedule_c = root.find('.//irs:IRS990ScheduleC', ns)

                #202300129349303035
                if schedule_c is not None:
                    common_data = [
                        extract_id_from_filename(filename),
                        findtext('.//irs:Filer/irs:EIN'),
                        findtext('.//irs:Filer/irs:BusinessName/irs:BusinessNameLine1Txt'),
                        findtext('.//irs:Filer/irs:BusinessNameControlTxt'),

                        findtext('.//irs:IRS990ScheduleC/irs:PoliticalExpendituresAmt'),
                        findtext('.//irs:IRS990ScheduleC/irs:VolunteerHoursCnt')
                    ]
                    details = schedule_c.findall('.//irs:SupplementalInformationDetail', ns)
                    if not details:
                        row = common_data + ['', '']
                        rows.append(row)
                    else:
                        for detail in details:  
                            form_line_ref = detail.find('irs:FormAndLineReferenceDesc', ns)
                            explanation = detail.find('irs:ExplanationTxt', ns)
                            
                            # Create a new row for each detail
                            row = common_data + [
                                form_line_ref.text if form_line_ref is not None else '',
                                explanation.text if explanation is not None else ''
                            ]
                            rows.append(row)

for i in range(1, 2):
    folder = f'download990xml_2021_{str(i)}'
    if os.path.exists(folder):
        print(f"Processing folder {folder}...")
        process_folder(folder)
    else:
        print(f"Folder {folder} not found, skipping.")

# Write to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f'All Data extracted to {output_csv}')