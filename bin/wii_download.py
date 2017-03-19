#!/user/bin/env python

# Filename: wii_download.py
# Author: @inigo-benavides
# Date: 03-19-17
# Description: Downloads data from Wii using AWS

import pandas as pd
import string
import os
import datetime
import boto3

# Define path
today = datetime.datetime.today()
month, day, year = today.strftime('%m'), today.strftime('%d'), today.strftime('%y')
env_date = today.strftime('%m_%d_%y')
base_path = '/Users/miguelbenavides/Desktop/mynt/data/main/wii_data_dumps/{0}/'.format(env_date)

# Create path if not exists
if not os.path.exists(base_path):
	os.makedirs(base_path)

# Download S3 data using boto3
s3 = boto3.client('s3')
print "Downloading s3://fusereports/wii/daily_data_dump/FuseReport20{0}{1}{2}v2.csv".format(year, month, day), base_path + '{0}{1}{2}_Data_Dump.csv'.format(year, month, day)
s3.download_file('fusereports', 'wii/daily_data_dump/FuseReport20{0}{1}{2}v2.csv'.format(year, month, day), base_path + '{0}{1}{2}_Data_Dump.csv'.format(year, month, day))

# Load DataFrame
df = pd.read_csv(base_path + '{0}{1}{2}_Data_Dump.csv'.format(year, month, day), low_memory=False)

# Remove escape characters that may interfere with formatting
for field in df.columns:
	df[field] = df[field].apply(lambda x: x.replace('\n', '') if isinstance(x, basestring) else x)
	df[field] = df[field].apply(lambda x: x.replace('\r', '') if isinstance(x, basestring) else x)
	df[field] = df[field].apply(lambda x: x.replace('\n', '') if isinstance(x, basestring) else x)

# Translate Excel column convention to index
# string.uppercase.index('A') returns 0

def xl2index(x):
	if len(x) == 1:
		return string.uppercase.index(x)
	else:
		x1 = 26 * string.uppercase.index(x[0]) + 26
		x2 = string.uppercase.index(x[1])
		return x1 + x2


# Define table ranges
table_dict = {
			'loans': ['A', 'BO'],
			'applications': ['BP', 'DO'],
			'business_loans': ['DP', 'EY'],
			'personal_references': ['EZ', 'FQ'],
			'financial_details': ['FR', 'GX'],
			'trade_references': ['GY', 'HI'],
			'client_references': ['HJ', 'HP'],
			'supplier_references': ['HQ', 'HX']}

# Transform product_id
product_id_dict = {
					0: 'test',
					1: 'sparkloan',
					2: 'puhunan_plus',
					3: 'fbl',
					4: 'payday_advance',
					5: 'instaloan',
					6: 'goloan'}
	

df.product_id = df.product_id.apply(lambda x: product_id_dict[x])

# Transform status and last_form_type
status_dict = {
		0: "test",
		1: "Pending",
		2: "Cancelled",
		3: "Incomplete",
		4: "Processing",
		5: "Draft",
		6: "Rejected",
		7: "Approved",
		8: "Implemented",
		9: "Dropped",
		10: "In Queue"}


form_type_dict = {
	0 : "Not Submitted", 
	1 : "Personal Details", 
	2 : "Business Details", 
	3 : "Financial Details", 
	4 : "Required Documents", 
	5 : "References", 
	6 : "Verification and Summary", 
	7 : "Credit Scoring"}

df.status = df.status.apply(lambda x: status_dict[x])
df.last_form_type = df.last_form_type.apply(lambda x: form_type_dict[x])

# Disaggregate tables

field_dict = {
	'loans': [
			'id',
			'logs',
			'application_id',
			'product_id',
			'business_loan_id',
			'distributor_id',
			'supplier_ref_id',
			'client_ref_id',
			'personal_ref_id',
			'salary_loan_id',
			'uploaded_by',
			'channel',
			'created_at',
			'updated_at',
			'reference_number',
			'status',
			'last_step',
			'last_form_type',
			'purpose_loan',
			'amount_to_borrow',
			'will_use_loan',
			'is_power_card',
			'loan_term',
			'loan_repayment',
			'total_loan_repayment',
			'pending_tat',
			'processing_tat',
			'draft_tat',
			'pending_updated',
			'processing_updated',
			'draft_updated',
			'loan_code',
			'loan_amount',
			'kyc_checked',
			'dataspark_score',
			'lenddo_score',
			'credit_scoring_type',
			'edo_consent_sent',
			'rejected_code',
			'rejected_remarks',
			'incomplete_code',
			'incomplete_remarks',
			'approval_level',
			'credit_committee',
			'attach_file_process',
			'processing_remarks',
			'approval_remarks',
			'attach_file_approved',
			'privacy_policy_time',
			'terms_condition_time',
			'special_approval',
			'exception_code',
			'credit_evaluation_lead',
			'special_code',
			'interest_rate',
			'lsr',
			'tsh',
			'rsh',
			'lenddo_decision',
			'lenddo_key',
			'date_submitted',
			'date_approved',
			'date_rejected',
			'partner_fee',
			'is_banko',
			'sms_rejection',
			'draft_reminder_sent'
			],
		'applications': [
			'id',
			'acc_number',
			'primary_connum',
			'landline_num',
			'fname',
			'mname',
			'lname',
			'bday',
			'nationality',
			'gender',
			'email',
			'line_one',
			'line_two',
			'region',
			'city',
			'barangay',
			'zipcode',
			'pre_add_yr',
			'per_line_one',
			'per_line_two',
			'per_region',
			'per_city',
			'per_barangay',
			'per_zipcode',
			'home_ownership',
			'rented',
			'spouse_fname',
			'spouse_mname',
			'spouse_lname',
			'm_source_inc',
			'm_inc',
			's_source_inc',
			'sm_inc',
			'acc_oth_bank',
			'created_at',
			'updated_at',
			'token',
			'marital_status',
			'province',
			'per_province',
			'spouse_bday',
			'sms_verfied',
			'email_verified',
			'auth_code',
			'high_edu_attain',
			'num_dependents',
			'pre_months',
			'spouse_source_income',
			'oth_connum',
			'spouse_con',
			'puregold_carded',
			'send_consent_times'
			],
		'business_loans': [
			'id',
			'desired_loan_amount',
			'duration_of_loan',
			'purpose_loan',
			'business_name',
			'business_type',
			'line_one',
			'line_two',
			'region',
			'city',
			'barangay',
			'zipcode',
			'years_of_business',
			'business_operation',
			'existing_loans',
			'loan_id',
			'created_at',
			'updated_at',
			'name',
			'type',
			'industry',
			'years',
			'months',
			'home_floor_number',
			'building_name',
			'poastal_code',
			'opens_at',
			'closes_at',
			'opens_on',
			'total_monthly_income',
			'is_globe_mybusiness',
			'other_bank_loans',
			'goods_sources',
			'puring_card_num',
			'puregold_branch',
			'mybiz_acc_number'
			],
		'personal_references': [
			'id',
			'first_name',
			'middle_name',
			'last_name',
			'line_one',
			'line_two',
			'region',
			'city',
			'barangay',
			'zipcode',
			'relationship',
			'loan_id',
			'created_at',
			'updated_at',
			'name',
			'address',
			'contact_number',
			'alt_contact_number'
			],
		'financial_details': [
			'id',
			'emp_status',
			'm_source_inc',
			's_source_allow_famsupport',
			's_source_remittance',
			's_source_pension',
			's_source_business',
			's_source_commision',
			'acc_oth_bank',
			'acc_oth_bank_type',
			'company_name',
			'position_company',
			'years_company',
			'month_company',
			'tin',
			'gsis_sss',
			'personal_loan',
			'home_loan',
			'pag_ibig_loan',
			'sss_gsis_loan',
			'friend_family',
			'informal_lender_loan',
			'loan_id',
			'created_at',
			'updated_at',
			'monthly_inc',
			's_source_inc',
			'acc_number',
			'prefered_payment_mode',
			'payment_bank',
			'is_gcash_registered',
			'tenure_years',
			'tenure_months'
			],
		'trade_references': [
			'id',
			'loan_id',
			'created_at',
			'updated_at',
			'name',
			'supplier_reference_name',
			'supplier_reference_contact',
			'supplier_reference_address',
			'customer_reference_name',
			'customer_reference_contact',
			'customer_reference_address'
			],
		'client_references': [
			'id',
			'name_of_client',
			'business_address',
			'contact_number',
			'trade_reference_id',
			'created_at',
			'updated_at'
			],
		'supplier_references': [
			'id',
			'name_of_supplier',
			'business_address',
			'contact_number',
			'created_at',
			'updated_at',
			'trade_reference_id',
			'tmp'
			]
 		}


# Instantiate tmp at end of column for range inclusion below
df['tmp'] = ''

# Define function to fix applications.primary_connum
def primary_connum_fix(x):
	if len(str(x)) == 11:
		return x[1:]
	else:
		return x

# Format column names of df
for key, value in table_dict.iteritems():
	starting_index = xl2index(value[0])
	ending_index = xl2index(value[1])
	df_sub = df.iloc[:,starting_index:ending_index+1]
	df_sub.columns = field_dict[key]

	# Drop if id is empty
	df_sub = df_sub[~df_sub['id'].isnull()]

	# Drop duplicated ids
	df_sub = df_sub.drop_duplicates('id')

	# Rename id
	field_dict[key][0] = key[:-1] + '_' 'id'
	df_sub.columns = field_dict[key]

	# Apply primary_connum_fix
	if key == 'applications':
		df_sub.primary_connum = df_sub.primary_connum.apply(lambda x: primary_connum_fix(x))

	# Drop empty columns
	df_sub.dropna(axis = 1, how = 'all', inplace=True)

	# Save to disk
	df_sub.to_csv(base_path + '{0}.csv'.format(key))

	print "Saved ", base_path + '{0}.csv'.format(key)