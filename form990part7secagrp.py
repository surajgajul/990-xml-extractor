import os
import csv
import xml.etree.ElementTree as ET

# Set your folder path
folder_path = '2021_TEOS_XML'
output_csv = '2021form990part7secagrp_all.csv'

# Define namespaces
ns = {
    'irs': 'http://www.irs.gov/efile',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# List to collect all rows
rows = []

# Header for CSV
header = [
    'ID', 'Form990PartVIISectionAGrp_PersonNm', 'BusinessName', 'TitleTxt', 'AverageHoursPerWeekRt',
    'AverageHoursPerWeekRltdOrgRt', 'IndividualTrusteeOrDirectorInd', 'InstitutionalTrusteeInd', 'OfficerInd',
    'KeyEmployeeInd', 'HighestCompensatedEmployeeInd', 'FormerOfcrDirectorTrusteeInd',
    'ReportableCompFromOrgAmt', 'ReportableCompFromRltdOrgAmt', 'OtherCompensationAmt'
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
                    continue
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


                common_data = [
                    extract_id_from_filename(filename),
                ]
                schedule_990 = root.find(f'.//{irs_return_tag}', ns)

                if not schedule_990.findall('.//irs:Form990PartVIISectionAGrp', ns):
                    row = common_data + ['', '', '', '', '', '', '', '', '', '', '', '', '', '']
                    rows.append(row)
                else:
                    for detail in schedule_990.findall('.//irs:Form990PartVIISectionAGrp', ns):
                        PersonNm = detail.find('irs:PersonNm', ns)
                        BusinessName = detail.find('irs:BusinessName', ns)
                        TitleTxt = detail.find('irs:TitleTxt', ns)
                        AverageHoursPerWeekRt = detail.find('irs:AverageHoursPerWeekRt', ns)
                        AverageHoursPerWeekRltdOrgRt = detail.find('irs:AverageHoursPerWeekRltdOrgRt', ns)
                        IndividualTrusteeOrDirectorInd = detail.find('irs:IndividualTrusteeOrDirectorInd', ns)
                        InstitutionalTrusteeInd = detail.find('irs:InstitutionalTrusteeInd', ns)
                        OfficerInd = detail.find('irs:OfficerInd', ns)
                        KeyEmployeeInd = detail.find('irs:KeyEmployeeInd', ns)
                        HighestCompensatedEmployeeInd = detail.find('irs:HighestCompensatedEmployeeInd', ns)
                        FormerOfcrDirectorTrusteeInd = detail.find('irs:FormerOfcrDirectorTrusteeInd', ns)
                        ReportableCompFromOrgAmt = detail.find('irs:ReportableCompFromOrgAmt', ns)
                        ReportableCompFromRltdOrgAmt = detail.find('irs:ReportableCompFromRltdOrgAmt', ns)
                        OtherCompensationAmt = detail.find('irs:OtherCompensationAmt', ns)

                        row = common_data + [
                            PersonNm.text if PersonNm is not None else '',
                            BusinessName.text if BusinessName is not None else '',
                            TitleTxt.text if TitleTxt is not None else '',
                            AverageHoursPerWeekRt.text if AverageHoursPerWeekRt is not None else '',
                            AverageHoursPerWeekRltdOrgRt.text if AverageHoursPerWeekRltdOrgRt is not None else '',
                            IndividualTrusteeOrDirectorInd.text if IndividualTrusteeOrDirectorInd is not None else '',
                            InstitutionalTrusteeInd.text if InstitutionalTrusteeInd is not None else '',
                            OfficerInd.text if OfficerInd is not None else '',
                            KeyEmployeeInd.text if KeyEmployeeInd is not None else '',
                            HighestCompensatedEmployeeInd.text if HighestCompensatedEmployeeInd is not None else '',
                            FormerOfcrDirectorTrusteeInd.text if FormerOfcrDirectorTrusteeInd is not None else '',
                            ReportableCompFromOrgAmt.text if ReportableCompFromOrgAmt is not None else '',
                            ReportableCompFromRltdOrgAmt.text if ReportableCompFromRltdOrgAmt is not None else '',
                            OtherCompensationAmt.text if OtherCompensationAmt is not None else '',
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