import os
import csv
import xml.etree.ElementTree as ET

# Set your folder path
folder_path = '2021_TEOS_XML'
output_csv = '2021part8_stat_of_rev_all.csv'

# Define namespaces
ns = {
    'irs': 'http://www.irs.gov/efile',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# List to collect all rows
rows = []

# Header for CSV
header = [
    'ID', 'FederatedCampaignsAmt', 'MembershipDuesAmt', 'FundraisingAmt', 'RelatedOrganizationsAmt',
    'GovernmentGrantsAmt', 'AllOtherContributionsAmt', 'NoncashContributionsAmt', 'TotalContributionsAmt', 'TotalProgramServiceRevenueAmt',
    'InvestmentIncomeGrp_TotalRevenueColumnAmt', 'InvestmentIncomeGrp_RelatedOrExemptFuncIncomeAmt', 'InvestmentIncomeGrp_UnrelatedBusinessRevenueAmt', 'InvestmentIncomeGrp_ExclusionAmt',
    'IncmFromInvestBondProceedsGrp_TotalRevenueColumnAmt', 'IncmFromInvestBondProceedsGrp_RelatedOrExemptFuncIncomeAmt', 'IncmFromInvestBondProceedsGrp_UnrelatedBusinessRevenueAmt', 'IncmFromInvestBondProceedsGrp_ExclusionAmt',
    'RoyaltiesRevenueGrp_TotalRevenueColumnAmt', 'RoyaltiesRevenueGrp_RelatedOrExemptFuncIncomeAmt', 'RoyaltiesRevenueGrp_UnrelatedBusinessRevenueAmt', 'RoyaltiesRevenueGrp_ExclusionAmt',
    'NetRentalIncomeOrLossGrp_TotalRevenueColumnAmt', 'NetRentalIncomeOrLossGrp_RelatedOrExemptFuncIncomeAmt', 'NetRentalIncomeOrLossGrp_UnrelatedBusinessRevenueAmt', 'NetRentalIncomeOrLossGrp_ExclusionAmt',
    'NetGainOrLossInvestmentsGrp_TotalRevenueColumnAmt', 'NetGainOrLossInvestmentsGrp_RelatedOrExemptFuncIncomeAmt', 'NetGainOrLossInvestmentsGrp_UnrelatedBusinessRevenueAmt', 'NetGainOrLossInvestmentsGrp_ExclusionAmt',
    'NetIncmFromFundraisingEvtGrp_TotalRevenueColumnAmt', 'NetIncmFromFundraisingEvtGrp_UnrelatedBusinessRevenueAmt', 'NetIncmFromFundraisingEvtGrp_ExclusionAmt',
    'NetIncomeFromGamingGrp_TotalRevenueColumnAmt', 'NetIncomeFromGamingGrp_RelatedOrExemptFuncIncomeAmt', 'NetIncomeFromGamingGrp_UnrelatedBusinessRevenueAmt', 'NetIncomeFromGamingGrp_ExclusionAmt',
    'NetIncomeOrLossGrp_TotalRevenueColumnAmt', 'NetIncomeOrLossGrp_RelatedOrExemptFuncIncomeAmt', 'NetIncomeOrLossGrp_UnrelatedBusinessRevenueAmt', 'NetIncomeOrLossGrp_ExclusionAmt',
    'OtherRevenueTotalAmt', 'TotalRevenueGrp_TotalRevenueColumnAmt', 'TotalRevenueGrp_RelatedOrExemptFuncIncomeAmt', 'TotalRevenueGrp_UnrelatedBusinessRevenueAmt', 'TotalRevenueGrp_ExclusionAmt'
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
                
                def has_schedule(schedule_tag, ns):
                    return root.find(f'.//irs:{schedule_tag}', ns) is not None

                common_data = [
                    extract_id_from_filename(filename),

                    findtext_in_return_tag('FederatedCampaignsAmt'),
                    findtext_in_return_tag('MembershipDuesAmt'),
                    findtext_in_return_tag('FundraisingAmt'),
                    findtext_in_return_tag('RelatedOrganizationsAmt'),
                    findtext_in_return_tag('GovernmentGrantsAmt'),
                    findtext_in_return_tag('AllOtherContributionsAmt'),
                    findtext_in_return_tag('NoncashContributionsAmt'),
                    findtext_in_return_tag('TotalContributionsAmt'),
                    findtext_in_return_tag('TotalProgramServiceRevenueAmt'),

                    findtext_in_return_tag('InvestmentIncomeGrp/irs:TotalRevenueColumnAmt'),
                    findtext_in_return_tag('InvestmentIncomeGrp/irs:RelatedOrExemptFuncIncomeAmt'),
                    findtext_in_return_tag('InvestmentIncomeGrp/irs:UnrelatedBusinessRevenueAmt'),
                    findtext_in_return_tag('InvestmentIncomeGrp/irs:ExclusionAmt'),

                    findtext_in_return_tag('IncmFromInvestBondProceedsGrp/irs:TotalRevenueColumnAmt'),
                    findtext_in_return_tag('IncmFromInvestBondProceedsGrp/irs:RelatedOrExemptFuncIncomeAmt'),
                    findtext_in_return_tag('IncmFromInvestBondProceedsGrp/irs:UnrelatedBusinessRevenueAmt'),
                    findtext_in_return_tag('IncmFromInvestBondProceedsGrp/irs:ExclusionAmt'),

                    findtext_in_return_tag('RoyaltiesRevenueGrp/irs:TotalRevenueColumnAmt'),
                    findtext_in_return_tag('RoyaltiesRevenueGrp/irs:RelatedOrExemptFuncIncomeAmt'),
                    findtext_in_return_tag('RoyaltiesRevenueGrp/irs:UnrelatedBusinessRevenueAmt'),
                    findtext_in_return_tag('RoyaltiesRevenueGrp/irs:ExclusionAmt'),

                    findtext_in_return_tag('NetRentalIncomeOrLossGrp/irs:TotalRevenueColumnAmt'),
                    findtext_in_return_tag('NetRentalIncomeOrLossGrp/irs:RelatedOrExemptFuncIncomeAmt'),
                    findtext_in_return_tag('NetRentalIncomeOrLossGrp/irs:UnrelatedBusinessRevenueAmt'),
                    findtext_in_return_tag('NetRentalIncomeOrLossGrp/irs:ExclusionAmt'),

                    findtext_in_return_tag('NetGainOrLossInvestmentsGrp/irs:TotalRevenueColumnAmt'),
                    findtext_in_return_tag('NetGainOrLossInvestmentsGrp/irs:RelatedOrExemptFuncIncomeAmt'),
                    findtext_in_return_tag('NetGainOrLossInvestmentsGrp/irs:UnrelatedBusinessRevenueAmt'),
                    findtext_in_return_tag('NetGainOrLossInvestmentsGrp/irs:ExclusionAmt'),

                    findtext_in_return_tag('NetIncmFromFundraisingEvtGrp/irs:TotalRevenueColumnAmt'),
                    findtext_in_return_tag('NetIncmFromFundraisingEvtGrp/irs:UnrelatedBusinessRevenueAmt'),
                    findtext_in_return_tag('NetIncmFromFundraisingEvtGrp/irs:ExclusionAmt'),

                    findtext_in_return_tag('NetIncomeFromGamingGrp/irs:TotalRevenueColumnAmt'),
                    findtext_in_return_tag('NetIncomeFromGamingGrp/irs:RelatedOrExemptFuncIncomeAmt'),
                    findtext_in_return_tag('NetIncomeFromGamingGrp/irs:UnrelatedBusinessRevenueAmt'),
                    findtext_in_return_tag('NetIncomeFromGamingGrp/irs:ExclusionAmt'),

                    findtext_in_return_tag('NetIncomeOrLossGrp/irs:TotalRevenueColumnAmt'),
                    findtext_in_return_tag('NetIncomeOrLossGrp/irs:RelatedOrExemptFuncIncomeAmt'),
                    findtext_in_return_tag('NetIncomeOrLossGrp/irs:UnrelatedBusinessRevenueAmt'),
                    findtext_in_return_tag('NetIncomeOrLossGrp/irs:ExclusionAmt'),

                    findtext_in_return_tag('OtherRevenueTotalAmt'),
                    findtext_in_return_tag('TotalRevenueGrp/irs:TotalRevenueColumnAmt'),
                    findtext_in_return_tag('TotalRevenueGrp/irs:RelatedOrExemptFuncIncomeAmt'),
                    findtext_in_return_tag('TotalRevenueGrp/irs:UnrelatedBusinessRevenueAmt'),
                    findtext_in_return_tag('TotalRevenueGrp/irs:ExclusionAmt'),
                ]
                rows.append(common_data)

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

print(f'Data extracted to {output_csv}')