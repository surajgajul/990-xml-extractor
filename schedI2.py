import os
import csv
import xml.etree.ElementTree as ET

# Set your folder path
folder_path = '2024_TEOS_XML_01A'
output_csv = 'schedI2.csv'

# Define namespaces
ns = {
    'irs': 'http://www.irs.gov/efile',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# List to collect all rows
rows = []

# Header for CSV
header = [
    'ID', 'FilerEIN', 'BusinessNameLine1Txt', 'BusinessNameControlTxt', 'InCareofNm',
    'GrantRecordsMaintainedInd', 'Total501c3OrgCnt', 'TotalOtherOrgCnt', 'FormAndLineReferenceDesc', 'ExplanationTxt'
]

def extract_id_from_filename(filename):
            basename = os.path.basename(filename)
            if '_public.xml' in basename:
                return basename.split('_public.xml')[0]
            return ''

# Parse each XML file
for filename in os.listdir(folder_path):
    if filename.endswith('.xml'):
        filepath = os.path.join(folder_path, filename)
        tree = ET.parse(filepath)
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
        
        schedule_i = root.find('.//irs:IRS990ScheduleI', ns)

        if schedule_i is not None:
            common_data = [
                extract_id_from_filename(filename),
                findtext('.//irs:Filer/irs:EIN'),
                findtext('.//irs:Filer/irs:BusinessName/irs:BusinessNameLine1Txt'),
                findtext('.//irs:Filer/irs:BusinessNameControlTxt'),
                findtext('.//irs:Filer/irs:InCareOfNm'),

                findtext('.//irs:IRS990ScheduleI/irs:GrantRecordsMaintainedInd'),
                findtext('.//irs:IRS990ScheduleI/irs:Total501c3OrgCnt'),
                findtext('.//irs:IRS990ScheduleI/irs:TotalOtherOrgCnt'),

                # findtext('.//irs:IRS990ScheduleI/irs:SupplementalInformationDetail/irs:FormAndLineReferenceDesc'),
                # findtext('.//irs:IRS990ScheduleI/irs:SupplementalInformationDetail/irs:ExplanationTxt')
            ]
            if not schedule_i.findall('.//irs:SupplementalInformationDetail', ns):
                row = common_data + ['', '']
                rows.append(row)
            else:
                for detail in schedule_i.findall('.//irs:SupplementalInformationDetail', ns):  
                    form_line_ref = detail.find('irs:FormAndLineReferenceDesc', ns)
                    explanation = detail.find('irs:ExplanationTxt', ns)
                    
                    # Create a new row for each detail
                    row = common_data + [
                        form_line_ref.text if form_line_ref is not None else '',
                        explanation.text if explanation is not None else ''
                    ]
                    rows.append(row)

# Write to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f'Data extracted to {output_csv}')