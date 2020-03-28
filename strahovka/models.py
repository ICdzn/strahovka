from .common import db
from py4web import Field
import datetime


#идентификаторы компании
db.define_table('company_identifier',
                Field('name'),
                Field('code'))

db.define_table('company',
                Field('IAN_FULL_NAME'),
                Field('FIN_TYPE'),
                Field('IM_NUMIDENT', 'integer', length=8),
                Field('IAN_RO_SERIA'),
                Field('IAN_RO_CODE'),
                Field('IAN_RO_DT',type='datetime'),
                Field('DIC_NAME'),
                Field('F_ADR'),
                Field('IA_PHONE_CODE'),
                Field('IA_PHONE'),
                Field('IA_EMAIL'),
                Field('IND_OBL'),
                Field('K_NAME'),
                Field('abbreviation'),
                Field('position'),
                Field('update_date', type='datetime', default= datetime.datetime.now()),
                Field('changes'),
                Field('company_identifier','reference company_identifier'))

#лицензии
db.define_table('license',
                Field('NFS_CODE'),
                Field('NFS_NAME'),
                Field('LT_NNR2'),
                Field('LT_NAME'),
                Field('IL_NAME'),
                Field('IL_NUMBER'),
                Field('IL_DATE',type='datetime'),
                Field('IL_DATE_BEGIN',type='datetime'),
                Field('IL_DATE_END',type='datetime'),
                Field('IL_DATE_NULLIFY',type='datetime'),
                Field('IL_TERM'),
                Field('IL_DUPLICAT_DATE',type='datetime'),
                Field('IL_DUPLICAT_NO'),
                Field('LT_NNR_DUPL'),
                Field('IL_REREG_DATE',type='datetime'),
                Field('IL_REREG_NO'),
                Field('LT_NNR_REREG'),
                Field('IL_SUSPEND_DATE',type='datetime'),
                Field('LT_NNR_SUSPEND'),
                Field('IL_RESUME_DATE',type='datetime'),
                Field('LT_NNR_RESUME'),
                Field('IL_NULLIFY_NO'),
                Field('LT_BOOL'),
                Field('IL_APPOINTMENT'),
                Field('ILD_LRO_DATE',type='datetime'),
                Field('ILD_AOC_NUM'),
                Field('ILD_AOC_DATE',type='datetime'),
                Field('ILD_AOSRS_NUM'),
                Field('ILD_AOSRS_DATE',type='datetime'),
                Field('company_id','reference company'))
#подразрделы
db.define_table('unit',
                Field('IM_NUMIDENT'),
                Field('IAN_FULL_NAME',type='integer'),
                Field('IA_FULL'),
                Field('IA_PHONE_CODE'),
                Field('IA_PHONE'),
                Field('IND_OBL'),
                Field('FIO'),
                Field('ST_NAME'),
                Field('IM',default='Детально'),
                Field('company_id','reference company'))

#юзеры
db.define_table('user',
                Field('first_name'),
                Field('last_name'),
                Field('mobile_phone'),
                Field('work_phone'),
                Field('email1'),
                Field('email2'),
                Field('auth_user','reference auth_user'))

#журнал загрузок
db.define_table('download',
                Field('name'),
                Field('data'),
                Field('quarter_num'),
                Field('user','reference user'),
                Field('company_id','reference company'))


#пользователи компании
db.define_table('company_user',
                Field('user','reference user'),
                Field('company_identifier','reference company_identifier'),
                )
#журнал виплат
db.define_table('payout',
                Field('insurance_type'),
                Field('contract_num'),
                Field('case_num'),
                Field('insurance_case_date'),
                Field('statement_date'),
                Field('requirement_date'),
                Field('insurance_act_date'),
                Field('insurance_payment_date'),
                Field('insurance_payment_size'),
                Field('settlement_costs'),
                Field('reserve_size'),
                Field('company_id','reference company'))

#розділ 3 і 4
db.define_table('type',
                Field('name'),
                Field('gross_receipts'),
                Field('from_residents'),
                Field('rfrom_insurers_individuals'),
                Field('rfrom_insurers_legal_entities'),
                Field('rfrom_reinsurers'),
                Field('from_non_residents'),
                Field('nfrom_insurers_individuals'),
                # Field('nfrom_insurers_legal_entities'),
                # Field('nfrom_reinsurers',type='integer'),
                # Field('payments_return_to_insurers',type='integer'),
                # Field('payments_return_to_residents',type='integer'),
                # Field('rpayments_return_to_individuals',type='integer'),
                # Field('rpayments_return_to_legal_entities',type='integer'),
                # Field('rpayments_return_to_reinsurers',type='integer'),
                # Field('payments_return_to_non_residents',type='integer'),
                # Field('npayments_return_to_individuals',type='integer'),
                # Field('npayments_return_to_legal_entities',type='integer'),
                # Field('npayments_return_to_reinsurers',type='integer'),
                # Field('payments_paid_to_reinsurers',type='integer'),
                # Field('payments_paid_to_reinsurers_non_resident',type='integer'),
                # Field('unearned_premiums',type='integer'),
                # Field('unearned_premiums_reinsurers',type='integer'),
                # Field('unearned_premiums_reinsurers_non_resident',type='integer'),
                # Field('technical_reserves',type='integer'),
                # Field('reported_unpaid_losses',type='integer'),
                # Field('unreported_losses',type='integer'),
                # Field('catastrophe_reserve',type='integer'),
                # Field('loss_reserve_fluctuations',type='integer'),
                # Field('share_of_reinsurers_unearned_premiums',type='integer'),
                # Field('share_of_reinsurers_unearned_premiums_non_resident',type='integer'),
                # Field('insurance_cases_payments',type='integer'),
                # Field('insurance_payments',type='integer'),
                # Field('insurance_payments_residents',type='integer'),
                # Field('rinsurance_payments_individuals',type='integer'),
                # Field('rinsurance_payments_legal_entities',type='integer'),
                # Field('rinsurance_payments_reinsurers',type='integer'),
                # Field('insurance_payments_non_residents',type='integer'),
                # Field('ninsurance_payments_individuals', type='integer'),
                # Field('ninsurance_payments_legal_entities', type='integer'),
                # Field('ninsurance_payments_reinsurers', type='integer'),
                # Field('payments_offset_by_reinsurers',type='integer'),
                # Field('payments_offset_by_reinsurers_non_resident',type='integer'),
                # Field('maximum_insurance_payment',type='integer'),
                # Field('agency_fees',type='integer'),
                # Field('agency_fees_non_resident',type='integer'),
                # Field('costs_reinsurance_contracts',type='integer'),
                # Field('rewards_brokers',type='integer'),
                # Field('rewards_brokers_non_resident',type='integer'),
                # Field('commissions_for_reinsurer',type='integer'),
                # Field('commissions_for_reinsurer_non_resident',type='integer'),
                # Field('regulation_of_insured_events_in',type='integer'),
                # Field('legal_costs_in',type='integer'),
                # Field('expert_work_in',type='integer'),
                # Field('emergency_commissioners_in',type='integer'),
                # Field('expert_work_in',type='integer'),
                # Field('assistance_agencies_in',type='integer'),
                # Field('assistance_agencies_in_non_resident',type='integer'),
                # Field('regulation_of_insured_events_previous',type='integer'),
                # Field('legal_costs_previous',type='integer'),
                # Field('expert_work_previous',type='integer'),
                # Field('emergency_commissioners_previous',type='integer'),
                # Field('expert_work_previous',type='integer'),
                # Field('assistance_agencies_previous',type='integer'),
                # Field('assistance_agencies_previous_non_resident',type='integer'),
                # Field('number_of_insurance_contracts',type='integer'),
                # Field('number_contracts_individuals',type='integer'),
                # Field('number_contracts_legal_entities',type='integer'),
                # Field('minimum_insurance_amount',type='integer'),
                # Field('number_of_contracts_not_executed',type='integer'),
                # Field('number_of_contracts_not_executed_individuals',type='integer'),
                # Field('total_responsibility',type='integer'),
                # Field('payables',type='integer'),
                Field('company_id','reference company'))


db.commit()