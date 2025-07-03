import os
import csv
import xml.etree.ElementTree as ET

#10443
# Set your folder path
folder_path = '2021_TEOS_XML'
output_csv = '2021schedI_all.csv'

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
    'GrantRecordsMaintainedInd', 'Total501c3OrgCnt', 'TotalOtherOrgCnt', 'FormAndLineReferenceDesc', 'ExplanationTxt',
    'RecipientBusinessName', 'USAddress_AddressLine1Txt', 'USAddress_CityNm', 'USAddress_StateAbbreviationCd',
    'USAddress_ZIPCd', 'ForeignAddress_AddressLine1Txt', 'ForeignAddress_CityNm', 'ForeignAddress_ProvinceOrStateNm', 'ForeignAddress_CountryCd',
    'ForeignAddress_ForeignPostalCd', 'RecipientEIN', 'IRCSectionDesc', 'CashGrantAmt',
    'NonCashAssistanceAmt', 'ValuationMethodUsedDesc', 'NonCashAssistanceDesc', 'PurposeOfGrantTxt'
]

def extract_id_from_filename(filename):
    basename = os.path.basename(filename)
    if '_public.xml' in basename:
        return basename.split('_public.xml')[0]
    return ''

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
                
                schedule_i = root.find('.//irs:IRS990ScheduleI', ns)

                if schedule_i is not None:
                    base_common_data = [
                        extract_id_from_filename(filename),
                        findtext('.//irs:Filer/irs:EIN'),
                        findtext('.//irs:Filer/irs:BusinessName/irs:BusinessNameLine1Txt'),
                        findtext('.//irs:Filer/irs:BusinessNameControlTxt'),

                        findtext('.//irs:IRS990ScheduleI/irs:GrantRecordsMaintainedInd'),
                        findtext('.//irs:IRS990ScheduleI/irs:Total501c3OrgCnt'),
                        findtext('.//irs:IRS990ScheduleI/irs:TotalOtherOrgCnt'),
                    ]

                    supplemental_entries = schedule_i.findall('.//irs:SupplementalInformationDetail', ns)
                    supplemental_data = []

                    if supplemental_entries:
                        for detail in supplemental_entries:
                            form_line_ref = detail.find('irs:FormAndLineReferenceDesc', ns)
                            explanation = detail.find('irs:ExplanationTxt', ns)
                            supplemental_data.append([
                                form_line_ref.text if form_line_ref is not None else '',
                                explanation.text if explanation is not None else ''
                            ])
                    else:
                        # At least one blank supplemental if none exist
                        supplemental_data.append(['', ''])

                    recipient_entries = schedule_i.findall('.//irs:RecipientTable', ns)
                    recipient_data = []
                    if recipient_entries:
                        for detail in recipient_entries:
                            recipient_data.append([
                                (detail.find('irs:RecipientBusinessName/irs:BusinessNameLine1Txt', ns).text if detail.find('irs:RecipientBusinessName/irs:BusinessNameLine1Txt', ns) is not None else ''),
                                (detail.find('irs:USAddress/irs:AddressLine1Txt', ns).text if detail.find('irs:USAddress/irs:AddressLine1Txt', ns) is not None else ''),
                                (detail.find('irs:USAddress/irs:CityNm', ns).text if detail.find('irs:USAddress/irs:CityNm', ns) is not None else ''),
                                (detail.find('irs:USAddress/irs:StateAbbreviationCd', ns).text if detail.find('irs:USAddress/irs:StateAbbreviationCd', ns) is not None else ''),
                                (detail.find('irs:USAddress/irs:ZIPCd', ns).text if detail.find('irs:USAddress/irs:ZIPCd', ns) is not None else ''),
                                (detail.find('irs:ForeignAddress/irs:AddressLine1Txt', ns).text if detail.find('irs:ForeignAddress/irs:AddressLine1Txt', ns) is not None else ''),
                                (detail.find('irs:ForeignAddress/irs:CityNm', ns).text if detail.find('irs:ForeignAddress/irs:CityNm', ns) is not None else ''),
                                (detail.find('irs:ForeignAddress/irs:ProvinceOrStateNm', ns).text if detail.find('irs:ForeignAddress/irs:ProvinceOrStateNm', ns) is not None else ''),
                                (detail.find('irs:ForeignAddress/irs:CountryCd', ns).text if detail.find('irs:ForeignAddress/irs:CountryCd', ns) is not None else ''),
                                (detail.find('irs:ForeignAddress/irs:ForeignPostalCd', ns).text if detail.find('irs:ForeignAddress/irs:ForeignPostalCd', ns) is not None else ''),
                                (detail.find('irs:RecipientEIN', ns).text if detail.find('irs:RecipientEIN', ns) is not None else ''),
                                (detail.find('irs:IRCSectionDesc', ns).text if detail.find('irs:IRCSectionDesc', ns) is not None else ''),
                                (detail.find('irs:CashGrantAmt', ns).text if detail.find('irs:CashGrantAmt', ns) is not None else ''),
                                (detail.find('irs:NonCashAssistanceAmt', ns).text if detail.find('irs:NonCashAssistanceAmt', ns) is not None else ''),
                                (detail.find('irs:ValuationMethodUsedDesc', ns).text if detail.find('irs:ValuationMethodUsedDesc', ns) is not None else ''),
                                (detail.find('irs:NonCashAssistanceDesc', ns).text if detail.find('irs:NonCashAssistanceDesc', ns) is not None else ''),
                                (detail.find('irs:PurposeOfGrantTxt', ns).text if detail.find('irs:PurposeOfGrantTxt', ns) is not None else '')
                            ])

                    else:
                        # No recipients: just append one blank recipient row with base info
                        recipient_data.append([''] * 17)

                    for supp in supplemental_data:
                        for recip in recipient_data:
                            row = base_common_data + supp + recip
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