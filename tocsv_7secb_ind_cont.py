import os
import csv
import xml.etree.ElementTree as ET

# Set your folder path
folder_path = '2021_TEOS_XML'
output_csv = '2021part7secb_indp_cont_all.csv'

# Define namespaces
ns = {
    'irs': 'http://www.irs.gov/efile',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# List to collect all rows
rows = []

# Header for CSV
header = [
    'ID', 'CntrctRcvdGreaterThan100KCnt', 'PersonNm', 'BusinessName', 'AddressLine1Txt',
    'CityNm', 'StateAbbreviationCd', 'ZIPCd', 'ForeignAddress_AddressLine1Txt', 'ForeignAddress_CityNm', 'ForeignAddress_ProvinceOrStateNm',
    'ForeignAddress_CountryCd', 'ForeignPostalCd', 'ServicesDesc', 'CompensationAmt'
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


                common_data = [
                    extract_id_from_filename(filename),
                    findtext_in_return_tag('CntrctRcvdGreaterThan100KCnt'),
                ]
                schedule_990 = root.find(f'.//{irs_return_tag}', ns)

                if not schedule_990.findall('.//irs:ContractorCompensationGrp', ns):
                    row = common_data + ['', '', '', '', '', '', '', '', '', '', '', '', '']
                    rows.append(row)
                else:
                    for detail in schedule_990.findall('.//irs:ContractorCompensationGrp', ns):
                        PersonNm = detail.find('irs:ContractorName/irs:PersonNm', ns)
                        BusinessName = detail.find('irs:ContractorName/irs:BusinessName/irs:BusinessNameLine1Txt', ns)
                        AddressLine1Txt = detail.find('irs:ContractorAddress/irs:USAddress/irs:AddressLine1Txt', ns)
                        CityNm = detail.find('irs:ContractorAddress/irs:USAddress/irs:CityNm', ns)
                        StateAbbreviationCd = detail.find('irs:ContractorAddress/irs:USAddress/irs:StateAbbreviationCd', ns)
                        ZIPCd = detail.find('irs:ContractorAddress/irs:USAddress/irs:ZIPCd', ns)
                        ForeignAddress_AddressLine1Txt = detail.find('irs:ContractorAddress/irs:ForeignAddress/irs:AddressLine1Txt', ns)
                        ForeignAddress_CityNm= detail.find('irs:ContractorAddress/irs:ForeignAddress/irs:CityNm', ns)
                        ForeignAddress_ProvinceOrStateNm = detail.find('irs:ContractorAddress/irs:ForeignAddress/irs:ProvinceOrStateNm', ns)
                        ForeignAddress_CountryCd = detail.find('irs:ContractorAddress/irs:ForeignAddress/irs:CountryCd', ns)
                        ForeignPostalCd = detail.find('irs:ContractorAddress/irs:ForeignAddress/irs:ForeignPostalCd', ns)
                        ServicesDesc = detail.find('irs:ServicesDesc', ns)
                        CompensationAmt = detail.find('irs:CompensationAmt', ns)

                        row = common_data + [
                            PersonNm.text if PersonNm is not None else '',
                            BusinessName.text if BusinessName is not None else '',
                            AddressLine1Txt.text if AddressLine1Txt is not None else '',
                            CityNm.text if CityNm is not None else '',
                            StateAbbreviationCd.text if StateAbbreviationCd is not None else '',
                            ZIPCd.text if ZIPCd is not None else '',
                            ForeignAddress_AddressLine1Txt.text if ForeignAddress_AddressLine1Txt is not None else '',
                            ForeignAddress_CityNm.text if ForeignAddress_CityNm is not None else '',
                            ForeignAddress_ProvinceOrStateNm.text if ForeignAddress_ProvinceOrStateNm is not None else '',
                            ForeignAddress_CountryCd.text if ForeignAddress_CountryCd is not None else '',
                            ForeignPostalCd.text if ForeignPostalCd is not None else '',
                            ServicesDesc.text if ServicesDesc is not None else '',
                            CompensationAmt.text if CompensationAmt is not None else '',
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