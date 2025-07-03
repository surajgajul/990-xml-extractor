import os
import csv
import xml.etree.ElementTree as ET
import requests
import zipfile

# Set your folder path
folder_path = '2021_TEOS_XML'
output_csv = '2021output_all.csv'

urls = [
    f"https://apps.irs.gov/pub/epostcard/990/xml/2021/download990xml_2021_{str(i)}.zip"
    for i in range(1, 9)
]

for url in urls:
    zip_filename = url.split('/')[-1]
    folder_name = zip_filename.replace('.zip', '')
    
    # Skip if already extracted
    if os.path.exists(folder_name):
        print(f"Folder {folder_name} already exists, skipping download.")
        continue
    
    print(f"Downloading {zip_filename}...")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad HTTP status
        with open(zip_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Download failed for {zip_filename}: {e}")
        continue

    print(f"Extracting {zip_filename}...")
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(folder_name)
    except zipfile.BadZipFile as e:
        print(f"Extraction failed for {zip_filename}: {e}")
        continue

    os.remove(zip_filename)

    # response = requests.get(url)
    # with open(zip_filename, 'wb') as f:
    #     f.write(response.content)
    
    # print(f"Extracting {zip_filename}...")
    # with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
    #     zip_ref.extractall(folder_name)

    # os.remove(zip_filename) 

# Define namespaces
ns = {
    'irs': 'http://www.irs.gov/efile',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# List to collect all rows
rows = []

# Header for CSV
header = [
    'ID', 'ReturnTs', 'TaxPeriodBeginDt', 'TaxPeriodEndDt', 'ReturnTypeCd', 'TaxYr',
    'Filer_EIN', 'BusinessNameLine1Txt', 'BusinessNameControlTxt',
    'File_AddressLine1Txt', 'Filer_CityNm', 'Filer_StateAbbreviationCd', 'Filer_ZIPCd',
    'ForeignAddress_AddressLine1Txt', 'ForeignAddress_CityNm', 'ForeignAddress_ProvinceOrStateNm',
    'ForeignAddress_CountryCd', 'ForeignAddress_ForeignPostalCd',
    'IRS990ScheduleC', 'IRS990ScheduleD', 'IRS990ScheduleI', 'IRS990ScheduleO',
    'InitialReturnInd', 'FinalReturnInd', 'AmendedReturnInd', 'DoingBusinessAsName', 
    'GroupReturnForAffiliatesInd', 'Organization501c3Ind', 'Organization501cInd',
    'Organization501cTypeTxt', 'Organization4947a1NotPFInd', 'Organization527Ind',
    'WebsiteAddressTxt', 'TypeOfOrganizationCorpInd', 'TypeOfOrganizationTrustInd',
    'TypeOfOrganizationAssocInd', 'TypeOfOrganizationOtherInd', 'OtherOrganizationDsc',
    'FormationYr', 'LegalDomicileStateCd', 'LegalDomicileCountryCd', 'ActivityOrMissionDesc',
    'VotingMembersGoverningBodyCnt', 'VotingMembersIndependentCnt', 'TotalEmployeeCnt', 'TotalVolunteersCnt',
    'TotalGrossUBIAmt', 'NetUnrelatedBusTxblIncmAmt', 'PYContributionsGrantsAmt', 'CYContributionsGrantsAmt',
    'PYProgramServiceRevenueAmt', 'CYProgramServiceRevenueAmt', 'PYInvestmentIncomeAmt',
    'CYInvestmentIncomeAmt', 'PYOtherRevenueAmt', 'CYOtherRevenueAmt',
    'PYTotalRevenueAmt', 'CYTotalRevenueAmt', 'PYGrantsAndSimilarPaidAmt',
    'CYGrantsAndSimilarPaidAmt', 'PYBenefitsPaidToMembersAmt', 'CYBenefitsPaidToMembersAmt', 'PYSalariesCompEmpBnftPaidAmt',
    'CYSalariesCompEmpBnftPaidAmt', 'PYTotalProfFndrsngExpnsAmt', 'CYTotalProfFndrsngExpnsAmt', 'CYTotalFundraisingExpenseAmt',
    'PYOtherExpensesAmt', 'CYOtherExpensesAmt', 'PYTotalExpensesAmt', 'CYTotalExpensesAmt', 'PYRevenuesLessExpensesAmt',
    'CYRevenuesLessExpensesAmt', 'TotalAssetsBOYAmt', 'TotalAssetsEOYAmt', 'TotalLiabilitiesBOYAmt',
    'TotalLiabilitiesEOYAmt', 'NetAssetsOrFundBalancesBOYAmt', 'NetAssetsOrFundBalancesEOYAmt',
    'MissionDesc', 'SignificantNewProgramSrvcInd', 'SignificantChangeInd',
    'ActivityCd', 'ExpenseAmt', 'GrantAmt', 'RevenueAmt', 'Desc', 'ProgSrvcAccomActy2Grp_ActivityCd', 'ProgSrvcAccomActy2Grp_ExpenseAmt',
    'ProgSrvcAccomActy2Grp_GrantAmt', 'ProgSrvcAccomActy2Grp_RevenueAmt', 'ProgSrvcAccomActy2Grp_Desc',
    'ProgSrvcAccomActy3Grp_ActivityCd', 'ProgSrvcAccomActy3Grp_ExpenseAmt',
    'ProgSrvcAccomActy3Grp_GrantAmt', 'ProgSrvcAccomActy3Grp_RevenueAmt', 'ProgSrvcAccomActy3Grp_Desc',
    'ProgSrvcAccomActyOtherGrp_ActivityCd', 'ProgSrvcAccomActyOtherGrp_ExpenseAmt',
    'ProgSrvcAccomActyOtherGrp_GrantAmt', 'ProgSrvcAccomActyOtherGrp_RevenueAmt', 'ProgSrvcAccomActyOtherGrp_Desc',
    'TotalOtherProgSrvcExpenseAmt', 'TotalOtherProgSrvcGrantAmt', 'TotalOtherProgSrvcRevenueAmt', 'TotalProgramServiceExpensesAmt',
    'NoListedPersonsCompensatedInd', 'TotalReportableCompFromOrgAmt', 'TotReportableCompRltdOrgAmt',
    'TotalOtherCompensationAmt', 'IndivRcvdGreaterThan100KCnt', 'FormerOfcrEmployeesListedInd',
    'TotalCompGreaterThan150KInd', 'CompensationFromOtherSrcsInd',
    'GrossReceiptsAmt', 'TotalRevenueAmt', 'TotalExpensesAmt'
]

# Parse each XML file
def process_folder(folder_path):
    print(f"Processing folder {folder_path}...")
    for root_dir, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.xml'):
                filepath = os.path.join(root_dir, filename)
                # print(f"Found file: {filename}")
                # tree = ET.parse(filepath)
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
                irs_return_tag = f"irs:IRS{return_type_cd}" 

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
                    findtext('.//irs:ReturnTs'),
                    findtext('.//irs:TaxPeriodBeginDt'),
                    findtext('.//irs:TaxPeriodEndDt'),
                    findtext('.//irs:ReturnTypeCd'),
                    findtext('.//irs:TaxYr'),

                    findtext('.//irs:Filer/irs:EIN'),
                    findtext('.//irs:Filer/irs:BusinessName/irs:BusinessNameLine1Txt'),
                    findtext('.//irs:Filer/irs:BusinessNameControlTxt'),

                    findtext('.//irs:Filer/irs:USAddress/irs:AddressLine1Txt'),
                    findtext('.//irs:Filer/irs:USAddress/irs:CityNm'),
                    findtext('.//irs:Filer/irs:USAddress/irs:StateAbbreviationCd'),
                    findtext('.//irs:Filer/irs:USAddress/irs:ZIPCd'),

                    findtext('.//irs:Filer/irs:ForeignAddress/irs:AddressLine1Txt'),
                    findtext('.//irs:Filer/irs:ForeignAddress/irs:CityNm'),
                    findtext('.//irs:Filer/irs:ForeignAddress/irs:ProvinceOrStateNm'),
                    findtext('.//irs:Filer/irs:ForeignAddress/irs:CountryCd'),
                    findtext('.//irs:Filer/irs:ForeignAddress/irs:ForeignPostalCd'),

                    has_schedule('IRS990ScheduleC', ns),
                    has_schedule('IRS990ScheduleD', ns),
                    has_schedule('IRS990ScheduleI', ns),
                    has_schedule('IRS990ScheduleO', ns),

                    findtext_in_return_tag('InitialReturnInd'),
                    findtext_in_return_tag('FinalReturnInd'),
                    findtext_in_return_tag('AmendedReturnInd'),
                    findtext_in_return_tag('DoingBusinessAsName/irs:BusinessNameLine1Txt'),

                    findtext_in_return_tag('GroupReturnForAffiliatesInd'),
                    findtext_in_return_tag('Organization501c3Ind'),
                    findtext_in_return_tag('Organization501cInd'),
                    findtext_in_return_tag('Organization501cTypeTxt'),
                    findtext_in_return_tag('Organization4947a1NotPFInd'),
                    findtext_in_return_tag('Organization527Ind'),
                    findtext_in_return_tag('WebsiteAddressTxt'),
                    findtext_in_return_tag('TypeOfOrganizationCorpInd'),
                    findtext_in_return_tag('TypeOfOrganizationTrustInd'),
                    findtext_in_return_tag('TypeOfOrganizationAssocInd'),
                    findtext_in_return_tag('TypeOfOrganizationOtherInd'),
                    findtext_in_return_tag('OtherOrganizationDsc'),
                    findtext_in_return_tag('FormationYr'),
                    findtext_in_return_tag('LegalDomicileStateCd'),
                    findtext_in_return_tag('LegalDomicileCountryCd'),
                    findtext_in_return_tag('ActivityOrMissionDesc'),

                    findtext_in_return_tag('VotingMembersGoverningBodyCnt'),
                    findtext_in_return_tag('VotingMembersIndependentCnt'),
                    findtext_in_return_tag('TotalEmployeeCnt'),
                    findtext_in_return_tag('TotalVolunteersCnt'),
                    findtext_in_return_tag('TotalGrossUBIAmt'),
                    findtext_in_return_tag('NetUnrelatedBusTxblIncmAmt'),
                    findtext_in_return_tag('PYContributionsGrantsAmt'),
                    findtext_in_return_tag('CYContributionsGrantsAmt'),
                    findtext_in_return_tag('PYProgramServiceRevenueAmt'),
                    findtext_in_return_tag('CYProgramServiceRevenueAmt'),
                    findtext_in_return_tag('PYInvestmentIncomeAmt'),
                    findtext_in_return_tag('CYInvestmentIncomeAmt'),
                    findtext_in_return_tag('PYOtherRevenueAmt'),
                    findtext_in_return_tag('CYOtherRevenueAmt'),
                    findtext_in_return_tag('PYTotalRevenueAmt'),
                    findtext_in_return_tag('CYTotalRevenueAmt'),
                    findtext_in_return_tag('PYGrantsAndSimilarPaidAmt'),
                    findtext_in_return_tag('CYGrantsAndSimilarPaidAmt'),
                    findtext_in_return_tag('PYBenefitsPaidToMembersAmt'),
                    findtext_in_return_tag('CYBenefitsPaidToMembersAmt'),
                    findtext_in_return_tag('PYSalariesCompEmpBnftPaidAmt'),
                    findtext_in_return_tag('CYSalariesCompEmpBnftPaidAmt'),
                    findtext_in_return_tag('PYTotalProfFndrsngExpnsAmt'),
                    findtext_in_return_tag('CYTotalProfFndrsngExpnsAmt'),
                    findtext_in_return_tag('CYTotalFundraisingExpenseAmt'),
                    findtext_in_return_tag('PYOtherExpensesAmt'),
                    findtext_in_return_tag('CYOtherExpensesAmt'),
                    findtext_in_return_tag('PYTotalExpensesAmt'),
                    findtext_in_return_tag('CYTotalExpensesAmt'),
                    findtext_in_return_tag('PYRevenuesLessExpensesAmt'),
                    findtext_in_return_tag('CYRevenuesLessExpensesAmt'),
                    findtext_in_return_tag('TotalAssetsBOYAmt'),
                    findtext_in_return_tag('TotalAssetsEOYAmt'),
                    findtext_in_return_tag('TotalLiabilitiesBOYAmt'),
                    findtext_in_return_tag('TotalLiabilitiesEOYAmt'),
                    findtext_in_return_tag('NetAssetsOrFundBalancesBOYAmt'),
                    findtext_in_return_tag('NetAssetsOrFundBalancesEOYAmt'),

                    findtext_in_return_tag('MissionDesc'),
                    findtext_in_return_tag('SignificantNewProgramSrvcInd'),
                    findtext_in_return_tag('SignificantChangeInd'),
                    findtext_in_return_tag('ActivityCd'),
                    findtext_in_return_tag('ExpenseAmt'),
                    findtext_in_return_tag('GrantAmt'),
                    findtext_in_return_tag('RevenueAmt'),
                    findtext_in_return_tag('Desc'),
                    findtext_in_return_tag('ProgSrvcAccomActy2Grp/irs:ActivityCd'),
                    findtext_in_return_tag('ProgSrvcAccomActy2Grp/irs:ExpenseAmt'),
                    findtext_in_return_tag('ProgSrvcAccomActy2Grp/irs:GrantAmt'),
                    findtext_in_return_tag('ProgSrvcAccomActy2Grp/irs:RevenueAmt'),
                    findtext_in_return_tag('ProgSrvcAccomActy2Grp/irs:Desc'),
                    findtext_in_return_tag('ProgSrvcAccomActy3Grp/irs:ActivityCd'),
                    findtext_in_return_tag('ProgSrvcAccomActy3Grp/irs:ExpenseAmt'),
                    findtext_in_return_tag('ProgSrvcAccomActy3Grp/irs:GrantAmt'),
                    findtext_in_return_tag('ProgSrvcAccomActy3Grp/irs:RevenueAmt'),
                    findtext_in_return_tag('ProgSrvcAccomActy3Grp/irs:Desc'),
                    findtext_in_return_tag('ProgSrvcAccomActyOtherGrp/irs:ActivityCd'),
                    findtext_in_return_tag('ProgSrvcAccomActyOtherGrp/irs:ExpenseAmt'),
                    findtext_in_return_tag('ProgSrvcAccomActyOtherGrp/irs:GrantAmt'),
                    findtext_in_return_tag('ProgSrvcAccomActyOtherGrp/irs:RevenueAmt'),
                    findtext_in_return_tag('ProgSrvcAccomActyOtherGrp/irs:Desc'),
                    findtext_in_return_tag('TotalOtherProgSrvcExpenseAmt'),
                    findtext_in_return_tag('TotalOtherProgSrvcGrantAmt'),
                    findtext_in_return_tag('TotalOtherProgSrvcRevenueAmt'),
                    findtext_in_return_tag('TotalProgramServiceExpensesAmt'),

                    findtext_in_return_tag('NoListedPersonsCompensatedInd'),
                    findtext_in_return_tag('TotalReportableCompFromOrgAmt'),
                    findtext_in_return_tag('TotReportableCompRltdOrgAmt'),
                    findtext_in_return_tag('TotalOtherCompensationAmt'),
                    findtext_in_return_tag('IndivRcvdGreaterThan100KCnt'),
                    findtext_in_return_tag('FormerOfcrEmployeesListedInd'),
                    findtext_in_return_tag('TotalCompGreaterThan150KInd'),
                    findtext_in_return_tag('CompensationFromOtherSrcsInd'),

                    findtext_in_return_tag('GrossReceiptsAmt'),
                    findtext_in_return_tag('TotalRevenueAmt'),
                    findtext_in_return_tag('TotalExpensesAmt'),
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