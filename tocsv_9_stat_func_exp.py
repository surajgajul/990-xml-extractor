import os
import csv
import xml.etree.ElementTree as ET

# Set your folder path
folder_path = '2021_TEOS_XML'
output_csv = '2021part9_stat_func_exp_all.csv'

# Define namespaces
ns = {
    'irs': 'http://www.irs.gov/efile',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# List to collect all rows
rows = []

# Header for CSV
header = [
    'ID', 'InfoInScheduleOPartIXInd', 'GrantsToDomesticOrgsGrp_TotalAmt', 'GrantsToDomesticOrgsGrp_ProgramServicesAmt', 'GrantsToDomesticIndividualsGrp_TotalAmt', 'GrantsToDomesticIndividualsGrp_ProgramServicesAmt',
    'ForeignGrantsGrp_TotalAmt', 'ForeignGrantsGrp_ProgramServicesAmt', 'BenefitsToMembersGrp_TotalAmt', 'BenefitsToMembersGrp_ProgramServicesAmt',
    'CompCurrentOfcrDirectorsGrp_TotalAmt', 'CompCurrentOfcrDirectorsGrp_ProgramServicesAmt', 'CompCurrentOfcrDirectorsGrp_ManagementAndGeneralAmt', 'CompCurrentOfcrDirectorsGrp_FundraisingAmt',
    'CompDisqualPersonsGrp_TotalAmt', 'CompDisqualPersonsGrp_ProgramServicesAmt', 'CompDisqualPersonsGrp_ManagementAndGeneralAmt', 'CompDisqualPersonsGrp_FundraisingAmt',
    'OtherSalariesAndWagesGrp_TotalAmt', 'OtherSalariesAndWagesGrp_ProgramServicesAmt', 'OtherSalariesAndWagesGrp_ManagementAndGeneralAmt', 'OtherSalariesAndWagesGrp_FundraisingAmt',
    'PensionPlanContributionsGrp_TotalAmt', 'PensionPlanContributionsGrp_ProgramServicesAmt', 'PensionPlanContributionsGrp_ManagementAndGeneralAmt', 'PensionPlanContributionsGrp_FundraisingAmt',
    'OtherEmployeeBenefitsGrp_TotalAmt', 'OtherEmployeeBenefitsGrp_ProgramServicesAmt', 'OtherEmployeeBenefitsGrp_ManagementAndGeneralAmt', 'OtherEmployeeBenefitsGrp_FundraisingAmt',
    'PayrollTaxesGrp_TotalAmt', 'PayrollTaxesGrp_ProgramServicesAmt', 'PayrollTaxesGrp_ManagementAndGeneralAmt', 'PayrollTaxesGrp_FundraisingAmt',
    'FeesForServicesManagementGrp_TotalAmt', 'FeesForServicesManagementGrp_ProgramServicesAmt', 'FeesForServicesManagementGrp_ManagementAndGeneralAmt', 'FeesForServicesManagementGrp_FundraisingAmt',
    'FeesForServicesLegalGrp_TotalAmt', 'FeesForServicesLegalGrp_ProgramServicesAmt', 'FeesForServicesLegalGrp_ManagementAndGeneralAmt', 'FeesForServicesLegalGrp_FundraisingAmt',
    'FeesForServicesAccountingGrp_TotalAmt', 'FeesForServicesAccountingGrp_ProgramServicesAmt', 'FeesForServicesAccountingGrp_ManagementAndGeneralAmt', 'FeesForServicesAccountingGrp_FundraisingAmt',
    'FeesForServicesLobbyingGrp_TotalAmt', 'FeesForServicesLobbyingGrp_ProgramServicesAmt', 'FeesForServicesLobbyingGrp_ManagementAndGeneralAmt', 'FeesForServicesLobbyingGrp_FundraisingAmt',
    'FeesForServicesProfFundraising_TotalAmt', 'FeesForServicesProfFundraising_FundraisingAmt',
    'FeesForSrvcInvstMgmntFeesGrp_TotalAmt', 'FeesForSrvcInvstMgmntFeesGrp_ProgramServicesAmt', 'FeesForSrvcInvstMgmntFeesGrp_ManagementAndGeneralAmt', 'FeesForSrvcInvstMgmntFeesGrp_FundraisingAmt',
    'FeesForServicesOtherGrp_TotalAmt', 'FeesForServicesOtherGrp_ProgramServicesAmt', 'FeesForServicesOtherGrp_ManagementAndGeneralAmt', 'FeesForServicesOtherGrp_FundraisingAmt',
    'AdvertisingGrp_TotalAmt', 'AdvertisingGrp_ProgramServicesAmt', 'AdvertisingGrp_ManagementAndGeneralAmt', 'AdvertisingGrp_FundraisingAmt',
    'OfficeExpensesGrp_TotalAmt', 'OfficeExpensesGrp_ProgramServicesAmt', 'OfficeExpensesGrp_ManagementAndGeneralAmt', 'OfficeExpensesGrp_FundraisingAmt',
    'InformationTechnologyGrp_TotalAmt', 'InformationTechnologyGrp_ProgramServicesAmt', 'InformationTechnologyGrp_ManagementAndGeneralAmt', 'InformationTechnologyGrp_FundraisingAmt',
    'RoyaltiesGrp_TotalAmt', 'RoyaltiesGrp_ProgramServicesAmt', 'RoyaltiesGrp_ManagementAndGeneralAmt', 'RoyaltiesGrp_FundraisingAmt',
    'OccupancyGrp_TotalAmt', 'OccupancyGrp_ProgramServicesAmt', 'OccupancyGrp_ManagementAndGeneralAmt', 'OccupancyGrp_FundraisingAmt',
    'TravelGrp_TotalAmt', 'TravelGrp_ProgramServicesAmt', 'TravelGrp_ManagementAndGeneralAmt', 'TravelGrp_FundraisingAmt',
    'PymtTravelEntrtnmntPubOfclGrp_TotalAmt', 'PymtTravelEntrtnmntPubOfclGrp_ProgramServicesAmt', 'PymtTravelEntrtnmntPubOfclGrp_ManagementAndGeneralAmt', 'PymtTravelEntrtnmntPubOfclGrp_FundraisingAmt',
    'ConferencesMeetingsGrp_TotalAmt', 'ConferencesMeetingsGrp_ProgramServicesAmt', 'ConferencesMeetingsGrp_ManagementAndGeneralAmt', 'ConferencesMeetingsGrp_FundraisingAmt',
    'InterestGrp_TotalAmt', 'InterestGrp_ProgramServicesAmt', 'InterestGrp_ManagementAndGeneralAmt', 'InterestGrp_FundraisingAmt',
    'PaymentsToAffiliatesGrp_TotalAmt', 'PaymentsToAffiliatesGrp_ProgramServicesAmt', 'PaymentsToAffiliatesGrp_ManagementAndGeneralAmt', 'PaymentsToAffiliatesGrp_FundraisingAmt',
    'DepreciationDepletionGrp_TotalAmt', 'DepreciationDepletionGrp_ProgramServicesAmt', 'DepreciationDepletionGrp_ManagementAndGeneralAmt', 'DepreciationDepletionGrp_FundraisingAmt',
    'InsuranceGrp_TotalAmt', 'InsuranceGrp_ProgramServicesAmt', 'InsuranceGrp_ManagementAndGeneralAmt', 'InsuranceGrp_FundraisingAmt',
    'AllOtherExpensesGrp_TotalAmt', 'AllOtherExpensesGrp_ProgramServicesAmt', 'AllOtherExpensesGrp_ManagementAndGeneralAmt', 'AllOtherExpensesGrp_FundraisingAmt',
    'TotalFunctionalExpensesGrp_TotalAmt', 'TotalFunctionalExpensesGrp_ProgramServicesAmt',
    'TotalJointCostsGrp_TotalAmt', 'TotalJointCostsGrp_ProgramServicesAmt', 'TotalJointCostsGrp_ManagementAndGeneralAmt', 'TotalJointCostsGrp_FundraisingAmt', 'JointCostsInd'
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
                    findtext_in_return_tag('InfoInScheduleOPartIXInd'),

                    findtext_in_return_tag('GrantsToDomesticOrgsGrp/irs:TotalAmt'),
                    findtext_in_return_tag('GrantsToDomesticOrgsGrp/irs:ProgramServicesAmt'),

                    findtext_in_return_tag('GrantsToDomesticIndividualsGrp/irs:TotalAmt'),
                    findtext_in_return_tag('GrantsToDomesticIndividualsGrp/irs:ProgramServicesAmt'),

                    findtext_in_return_tag('ForeignGrantsGrp/irs:TotalAmt'),
                    findtext_in_return_tag('ForeignGrantsGrp/irs:ProgramServicesAmt'),

                    findtext_in_return_tag('BenefitsToMembersGrp/irs:TotalAmt'),
                    findtext_in_return_tag('BenefitsToMembersGrp/irs:ProgramServicesAmt'),

                    findtext_in_return_tag('CompCurrentOfcrDirectorsGrp/irs:TotalAmt'),
                    findtext_in_return_tag('CompCurrentOfcrDirectorsGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('CompCurrentOfcrDirectorsGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('CompCurrentOfcrDirectorsGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('CompDisqualPersonsGrp/irs:TotalAmt'),
                    findtext_in_return_tag('CompDisqualPersonsGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('CompDisqualPersonsGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('CompDisqualPersonsGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('OtherSalariesAndWagesGrp/irs:TotalAmt'),
                    findtext_in_return_tag('OtherSalariesAndWagesGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('OtherSalariesAndWagesGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('OtherSalariesAndWagesGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('PensionPlanContributionsGrp/irs:TotalAmt'),
                    findtext_in_return_tag('PensionPlanContributionsGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('PensionPlanContributionsGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('PensionPlanContributionsGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('OtherEmployeeBenefitsGrp/irs:TotalAmt'),
                    findtext_in_return_tag('OtherEmployeeBenefitsGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('OtherEmployeeBenefitsGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('OtherEmployeeBenefitsGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('PayrollTaxesGrp/irs:TotalAmt'),
                    findtext_in_return_tag('PayrollTaxesGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('PayrollTaxesGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('PayrollTaxesGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('FeesForServicesManagementGrp/irs:TotalAmt'),
                    findtext_in_return_tag('FeesForServicesManagementGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('FeesForServicesManagementGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('FeesForServicesManagementGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('FeesForServicesLegalGrp/irs:TotalAmt'),
                    findtext_in_return_tag('FeesForServicesLegalGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('FeesForServicesLegalGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('FeesForServicesLegalGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('FeesForServicesAccountingGrp/irs:TotalAmt'),
                    findtext_in_return_tag('FeesForServicesAccountingGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('FeesForServicesAccountingGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('FeesForServicesAccountingGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('FeesForServicesLobbyingGrp/irs:TotalAmt'),
                    findtext_in_return_tag('FeesForServicesLobbyingGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('FeesForServicesLobbyingGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('FeesForServicesLobbyingGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('FeesForServicesProfFundraising/irs:TotalAmt'),
                    findtext_in_return_tag('FeesForServicesProfFundraising/irs:FundraisingAmt'),

                    findtext_in_return_tag('FeesForSrvcInvstMgmntFeesGrp/irs:TotalAmt'),
                    findtext_in_return_tag('FeesForSrvcInvstMgmntFeesGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('FeesForSrvcInvstMgmntFeesGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('FeesForSrvcInvstMgmntFeesGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('FeesForServicesOtherGrp/irs:TotalAmt'),
                    findtext_in_return_tag('FeesForServicesOtherGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('FeesForServicesOtherGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('FeesForServicesOtherGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('AdvertisingGrp/irs:TotalAmt'),
                    findtext_in_return_tag('AdvertisingGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('AdvertisingGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('AdvertisingGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('OfficeExpensesGrp/irs:TotalAmt'),
                    findtext_in_return_tag('OfficeExpensesGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('OfficeExpensesGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('OfficeExpensesGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('InformationTechnologyGrp/irs:TotalAmt'),
                    findtext_in_return_tag('InformationTechnologyGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('InformationTechnologyGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('InformationTechnologyGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('RoyaltiesGrp/irs:TotalAmt'),
                    findtext_in_return_tag('RoyaltiesGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('RoyaltiesGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('RoyaltiesGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('OccupancyGrp/irs:TotalAmt'),
                    findtext_in_return_tag('OccupancyGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('OccupancyGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('OccupancyGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('TravelGrp/irs:TotalAmt'),
                    findtext_in_return_tag('TravelGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('TravelGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('TravelGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('PymtTravelEntrtnmntPubOfclGrp/irs:TotalAmt'),
                    findtext_in_return_tag('PymtTravelEntrtnmntPubOfclGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('PymtTravelEntrtnmntPubOfclGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('PymtTravelEntrtnmntPubOfclGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('ConferencesMeetingsGrp/irs:TotalAmt'),
                    findtext_in_return_tag('ConferencesMeetingsGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('ConferencesMeetingsGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('ConferencesMeetingsGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('InterestGrp/irs:TotalAmt'),
                    findtext_in_return_tag('InterestGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('InterestGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('InterestGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('PaymentsToAffiliatesGrp/irs:TotalAmt'),
                    findtext_in_return_tag('PaymentsToAffiliatesGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('PaymentsToAffiliatesGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('PaymentsToAffiliatesGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('DepreciationDepletionGrp/irs:TotalAmt'),
                    findtext_in_return_tag('DepreciationDepletionGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('DepreciationDepletionGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('DepreciationDepletionGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('InsuranceGrp/irs:TotalAmt'),
                    findtext_in_return_tag('InsuranceGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('InsuranceGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('InsuranceGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('AllOtherExpensesGrp/irs:TotalAmt'),
                    findtext_in_return_tag('AllOtherExpensesGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('AllOtherExpensesGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('AllOtherExpensesGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('TotalFunctionalExpensesGrp/irs:TotalAmt'),
                    findtext_in_return_tag('TotalFunctionalExpensesGrp/irs:ProgramServicesAmt'),

                    findtext_in_return_tag('TotalJointCostsGrp/irs:TotalAmt'),
                    findtext_in_return_tag('TotalJointCostsGrp/irs:ProgramServicesAmt'),
                    findtext_in_return_tag('TotalJointCostsGrp/irs:ManagementAndGeneralAmt'),
                    findtext_in_return_tag('TotalJointCostsGrp/irs:FundraisingAmt'),

                    findtext_in_return_tag('JointCostsInd'),
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

print(f'All Data extracted to {output_csv}')