#!/usr/bin/env python3

# external modules

# my modules
import PERM

debug = False

# Data structure definition:
# ObjSel : will the criteria and actions be applied to this object?
#   Criteria : Object Selection Criteria
#           
# ObjAct : dictionary containing object criteria and actions
#   Criteria : object change criteria. If met changes will be made to objects
#   Action : object change actions
#           Defined actions are:    'SetOwner' : set new owner
#                                   'AddKeyword' : Append a string to keywords
#                                   'DelKeyword' : Remove string from keywords
#                                   'RepTitle' : Replace the document title
#                                   'RepTmtNum' : Replace the tmt number
#                                   'Message' : Print a message
# PermSel : dictionary containing permissions criteria to decide if PermAct will be considered
#   Criteria : permissions criteria list (all items must be True in order to pass)
# PermAct : dictionary containing permissions criteria and actions
#   Criteria : permission change criteria. If met changes will be made to permissions
#   Action : permission change actions
#           Defined Actions are: 'Add','Change','Remove', or 'Message'
#               'Add' requires 'Handle' and 'Perms' to be defined
#               'Change' requires 'Perms' to be defined
#               'Remove' does not require additional arguments
#               'Message' requires 'Message' to be defined
# 
# crit_act_set = {'obj_sel' : parse_dict, 
#             'obj' : [ list of dicts of {'obj_crit' : parse_dict, 'obj_act' : obj_act_dict}, {...} ]
#             'perm' : [ list of dicts of {'perm_crit' : parse_dict , 'perm_act' : perm_act_dict}, {...} ]  

PERM_R = {'Read':True}
PERM_RW = {'Read':True, 'Write':True}
PERM_RWM = {'Read':True, 'Write':True, 'Manage':True}

REMOVE = {'Action' : 'Remove'}
CHANGE_R = {'Action' : 'Change', 'Perms' : PERM_R}
CHANGE_RW = {'Action' : 'Change', 'Perms' : PERM_RW}
CHANGE_RWM = {'Action' : 'Change', 'Perms' : PERM_RWM}

# Defs for Basic dictionary functionality
def chk_dict(k,v,m): return({'InDict' : {'key' : k, 'val' : v, 'match' : m}})
def chk_list(v,l,m): return({'InList' : {'val' : v, 'list' : l, 'match' : m}})
def dic_handle_eq(hdl): return(chk_dict('handle',hdl,'eq'))
def dic_handle_in(hdl): return(chk_dict('handle',hdl,'in'))
def dic_handle_not_eq(hdl): return({'NOT' : dic_handle_eq(hdl)})
def dic_handle_not_in(hdl): return({'NOT' : dic_handle_in(hdl)})

# Individual user perm defs (both Criteria and Action)
def dict_crit_act(criteria, action): return({'Criteria' : criteria, 'Action' : action})
def remove_user(user): return(dict_crit_act(dic_handle_eq(user), REMOVE))
def add_user(user,perms): return({  'Action': {'Action' : 'Add', 'Handle' : user, 'Perms' : perms},
                                    'Criteria': {'NOT' : dic_handle_eq(user)}})
def remove_user_ifperms(user, perms): return(dict_crit_act({'AND' : [perms, dic_handle_eq(user)]}, REMOVE))

# Defs used with Criteria dictionary field
def check_user_perms(user, perms): return({'AND' : [dic_handle_eq(user), perms]})
def excl_crit_user(user): return({'NOT' : dic_handle_eq( user )})

def remove_user_if_group(s, set, grp_handle, perms):
    ghs = PERM.get_group_handles(s, grp_handle)
    for gh in ghs:
        set['PermAct'].append(remove_user_ifperms(gh, perms)) 

user_handle = dic_handle_in('User-')
group_handle = dic_handle_in('Group-')
doc_handle = dic_handle_in('Document-')
col_handle = dic_handle_in('Collection-')
docORcol = {'OR' : [doc_handle, col_handle]}

read_true = chk_dict('Read', True, 'eq')
write_true = chk_dict('Write', True, 'eq')
manage_true = chk_dict('Manage', True, 'eq')
RWM_true = {'AND' : [read_true, write_true, manage_true]}
RW_true = {'AND' : [read_true, write_true]}

# The following will work correctly if the perm keys are not defined (i.e. no Write key means Write False)
read_false = {'NOT' : read_true}
write_false = {'NOT' : write_true}
manage_false = {'NOT' : manage_true}
WM_false = {'AND' : [write_false, manage_false]}

user_read_only = {'AND' : [user_handle, read_true, write_false, manage_false]}
user_RWM = {'AND': [user_handle, read_true, write_true, manage_true]}
group_read_only = {'AND' : [group_handle, read_true, write_false, manage_false]}
perm_none = {'AND' : [read_false, write_false, manage_false]}
perm_write_only = {'AND' : [read_false, write_true, manage_false]}
perm_W_or_M_no_R = {'AND' : [read_false, {'OR' : [write_true, manage_true]}]}
user_manage_false = {'AND' : [user_handle, manage_false]}

SE_doc = chk_dict('tmtnum', '.SEN.', 'in')
STR_doc = chk_dict('tmtnum', '.STR.', 'in')
CTR_doc = chk_dict('tmtnum', '.CTR.', 'in')
OPT_doc = chk_dict('tmtnum', '.OPT.', 'in')
TEL_doc = chk_dict('tmtnum', '.TEL.', 'in')
INST_doc = chk_dict('tmtnum', '.INS.', 'in')

inactive_user = chk_dict('name','INACTIVE','in')
remove_inactive = dict_crit_act(inactive_user, REMOVE)

remove_perm_none = dict_crit_act(perm_none,REMOVE)

# Groups
grp_all_users = 'Group-4'
grp_all_noEAR = 'Group-33'
grp_Isbrucker = 'Group-536'
grp_SE_readership = 'Group-325'
grp_M1CS_obs = 'Group-641'
grp_STR_managers = 'Group-655'
grp_IRIS_team = 'Group-54'
grp_IRIS_managers = 'Group-666'
grp_WFOS_managers = 'Group-815'

usr_sr_admin = 'User-1083'
usr_holly = 'User-21'
usr_site_admin = 'User-2'
usr_lindquist = 'User-120'
usr_peter_gray = 'User-383'
usr_christophe = 'User-1167'
usr_matthias = 'User-18'
usr_crampton = 'User-38'
usr_lianqi = 'User-407'

# TMT Instrumentation Members
usr_simard = 'User-241'
usr_ellerbroek = 'User-29'

# IRIS Subsystem Team Members
usr_wright = 'User-753'
usr_larkin = 'User-218'
usr_moore = 'User-458'
usr_ryugi = 'User-572'
usr_lu = 'User-556'
grp_IRIS_MANAGE = 'Group-666'

# structures group
usr_chylek = 'User-1165'
usr_amir = 'User-573'
usr_kyle = 'User-1087'

# inactive users
usr_szeto = 'User-138'
usr_taylor = 'User-53'
usr_hubin = 'User-300'
usr_erickson = 'User-135'
usr_britton = 'User-119'
usr_augusto = 'User-213'
usr_ford = 'User-123'
usr_miska = 'User-305'
usr_elias = 'User-133'
grp_EAP = 'Group-66'
usr_mclean = 'User-236'
usr_bauman = 'User-467'
usr_macintosh = 'User-63'
usr_phillips = 'User-145'


REMOVE_INACTIVE =   [remove_user(usr_szeto), 
                    remove_user(usr_taylor), 
                    remove_user(usr_britton),
                    remove_user(usr_augusto),
                    remove_user(usr_miska),
                    remove_user(usr_ford)]

# EAR Groups
grp_EAR_JPN_IRIS = 'Group-453'
grp_EAR_CHINA_SAC = 'Group-122'
grp_EAR_IN_SAC = 'Group-123'
grp_EAR_JP_SAC = 'Group-124'
grp_EAR_IN_BOARD = 'Group-120'
grp_EAR_JP_BOARD = 'Group-121'

grp_EAR_perm = {'OR' :  [dic_handle_eq(grp_EAR_JPN_IRIS),
                    dic_handle_eq(grp_EAR_CHINA_SAC),
                    dic_handle_eq(grp_EAR_IN_SAC),
                    dic_handle_eq(grp_EAR_JP_SAC),
                    dic_handle_eq(grp_EAR_IN_BOARD),
                    dic_handle_eq(grp_EAR_JP_BOARD)]}
                    
INS_doc = chk_dict('tmtnum', '.INS.', 'in')

TELDEPT_doc = {'OR' : [STR_doc, CTR_doc, OPT_doc, TEL_doc]}

no_se_readership = {'NOT' : dic_handle_eq( grp_SE_readership )}
no_IRIS_team = {'NOT' : dic_handle_eq( grp_IRIS_team )}
no_str_managers = {'NOT' : dic_handle_eq( grp_STR_managers )}

exclude_grp_se_readership = dic_handle_not_in(grp_SE_readership)
exclude_grp_all_users = dic_handle_not_in(grp_all_users)

add_R_grp_se_readership = {'Action' : 'Add', 'Handle' : grp_SE_readership, 'Perms' : {'Read' : True}}
add_RWM_grp_str_managers = {'Action' : 'Add', 'Handle' : grp_STR_managers, 'Perms' : {'Read' : True, 'Write' : True, 'Manage' : True}}

handle_sr_admin = dic_handle_eq('usr_sr_admin')

# Set A
obj_sel = {}
perm_sel = {}
obj_criteria_dict = {}
obj_actions_dict = {}

# PermAct definitions
# Remove any read_only users (they should be in groups)
PERMACT_REMOVE_ro_users = dict_crit_act(user_read_only, REMOVE)

# Remove read_only groups (except SE readership all)

PERMACT_REMOVE_ro_groups_except_IRIS_SEread = dict_crit_act({'AND' : [group_read_only, no_se_readership, no_IRIS_team]}, REMOVE)

# Remove group or user with no Read, but Write and/or Manage
PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R = dict_crit_act(perm_W_or_M_no_R, REMOVE)

PERMACT_REMOVE_grp_usr_perm_none = dict_crit_act(perm_none, REMOVE)

# Change permissions to add Read in cases where there is Write Only
PERMACT_CHANGE_W_to_RW = dict_crit_act(perm_write_only, CHANGE_RW)

# Add SE readership all if not already there
PERMACT_ADD_se_readership = dict_crit_act(no_se_readership, add_R_grp_se_readership)

# Add STR Managers all if not already there
PERMACT_ADD_str_managers = dict_crit_act(no_str_managers, add_RWM_grp_str_managers)

# Change SE readership no read or write/manage to read only
se_readership_noRead_or_WM = {'AND' : [dic_handle_eq(grp_SE_readership), {'OR' : [read_false, write_true, manage_true]}]}
PERMACT_CHANGE_se_readership_RO = dict_crit_act(se_readership_noRead_or_WM, CHANGE_R)

PERMACT_REMOVE_dumas_ro = dict_crit_act({'AND' : [user_read_only, dic_handle_eq(usr_christophe)]}, REMOVE)
PERMACT_REMOVE_mathias_manage_false = dict_crit_act({'AND' : [manage_false, dic_handle_eq(usr_matthias)]}, REMOVE)
# PERMACT_REMOVE_szeto = dict_crit_act(dic_handle_eq(usr_szeto), REMOVE)
PERMACT_REMOVE_szeto = remove_user(usr_szeto)

usr_str_managers = {'OR' : [dic_handle_eq(usr_chylek), dic_handle_eq(usr_amir), dic_handle_eq(usr_kyle)]}

PERMACT_REMOVE_ro_groups_except_se_reader = dict_crit_act({'AND' : [group_read_only, no_se_readership]}, REMOVE)

SET_SE_READERSHIP = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermAct'   : [ PERMACT_ADD_se_readership,
                        PERMACT_CHANGE_se_readership_RO,
                        PERMACT_REMOVE_ro_users,
                        PERMACT_REMOVE_ro_groups_except_se_reader,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R,
                        PERMACT_REMOVE_grp_usr_perm_none,
                        remove_inactive,
                        remove_user(grp_all_noEAR)]} 

# HIA Staff_AO_CAN_(EAR) (Group-685, DocuShare)
# NFIRAOS FDR Reveiw Team_OBSERVERS (Group-1004, DocuShare)
# NFIRAOS FDR Review Team_EXTERNAL (Group-1003, DocuShare)
# NFIRAOS FDR Review Team_INTERNAL (Group-1002, DocuShare)
grp_NFIRAOS_ext = 'Group-1003'
grp_NFIRAOS_obs = 'Group-1004'
grp_NFIRAOS_int = 'Group-1002'
grp_HIA_AO_Staff = 'Group-685'

no_NFDRext_readership = {'NOT' : dic_handle_eq( grp_NFIRAOS_ext )}
no_NFDRobs_readership = {'NOT' : dic_handle_eq( grp_NFIRAOS_obs )}
no_NFDRint_readership = {'NOT' : dic_handle_eq( grp_NFIRAOS_int )}

# Add SE readership all if not already there
add_R_grp_NFDRext_readership = {'Action' : 'Add', 'Handle' : grp_NFIRAOS_ext, 'Perms' : {'Read' : True}}
add_R_grp_NFDRobs_readership = {'Action' : 'Add', 'Handle' : grp_NFIRAOS_obs, 'Perms' : {'Read' : True}}
add_R_grp_NFDRint_readership = {'Action' : 'Add', 'Handle' : grp_NFIRAOS_int, 'Perms' : {'Read' : True}}

PERMACT_ADD_NFIRAOSFDRext_readership = dict_crit_act(no_NFDRext_readership, add_R_grp_NFDRext_readership)
PERMACT_ADD_NFIRAOSFDRobs_readership = dict_crit_act(no_NFDRobs_readership, add_R_grp_NFDRobs_readership)
PERMACT_ADD_NFIRAOSFDRint_readership = dict_crit_act(no_NFDRobs_readership, add_R_grp_NFDRint_readership)

SET_ADDPANEL_NFIRAOS_FDR = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : [],
        'PermAct'   : [ PERMACT_ADD_NFIRAOSFDRext_readership,
                        PERMACT_ADD_NFIRAOSFDRobs_readership,
                        PERMACT_ADD_NFIRAOSFDRint_readership]} 
                        
SET_REMPANEL_NFIRAOS_FDR = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : [],
        'PermAct'   : [ remove_user(grp_NFIRAOS_ext),
                        remove_user(grp_NFIRAOS_obs),
                        remove_user(grp_NFIRAOS_int)]} 

SET_FIXEAR_NFIRAOS_FDR = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : [],
        'PermSel'   : { 'Criteria' : [check_user_perms(grp_all_noEAR,read_true)]},
        'PermAct'   : [ PERMACT_ADD_se_readership,
                        PERMACT_CHANGE_se_readership_RO,
                        PERMACT_REMOVE_ro_users,
                        PERMACT_REMOVE_ro_groups_except_se_reader,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R,
                        PERMACT_REMOVE_grp_usr_perm_none,
                        remove_inactive,
                        remove_user(grp_all_noEAR)]}                     
                        
SET_FIX_NFIRAOS_FDR = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : [],
        'PermSel'   : {'Criteria' : [check_user_perms(grp_HIA_AO_Staff,RW_true)]},
        'PermAct'   : []} 
                        
SET_LGSF = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermSel'   : { 'Criteria' : [check_user_perms(grp_all_noEAR,read_true)]},
        'PermAct'   : [ PERMACT_ADD_se_readership,
                        PERMACT_CHANGE_se_readership_RO,
                        PERMACT_REMOVE_ro_users,
                        PERMACT_REMOVE_ro_groups_except_se_reader,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R,
                        PERMACT_REMOVE_grp_usr_perm_none,
                        remove_inactive,
                        remove_user(grp_all_noEAR)]} 

grp_NRCTC_ext = 'Group-644'
grp_NRCTC_obs = 'Group-647'
grp_NFIRAOS_team = 'Group-128'

PERMACT_REMOVE_ro_groups_NRTC = dict_crit_act({'AND' : [ group_read_only, 
                                                        excl_crit_user(grp_SE_readership),  
                                                        excl_crit_user(grp_NRCTC_ext),
                                                        excl_crit_user(grp_NRCTC_obs), 
                                                        excl_crit_user(grp_NFIRAOS_team)
                                                        ]},REMOVE)

SET_PERM_NRTCPDR = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermAct'   : [ PERMACT_ADD_se_readership,
                        PERMACT_CHANGE_se_readership_RO,
                        PERMACT_REMOVE_ro_users,
                        PERMACT_REMOVE_ro_groups_NRTC,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R,
                        PERMACT_REMOVE_grp_usr_perm_none,
                        remove_inactive,
                        remove_user(grp_all_noEAR)]} 

SET_REMOVE_RO_IF_SE_READERSHIP = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : [{'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict}],
        'PermSel'   : { 'Criteria' : [check_user_perms(grp_SE_readership,read_true)]},
        'PermAct'   : [ PERMACT_CHANGE_se_readership_RO,
                        PERMACT_REMOVE_ro_users,
                        PERMACT_REMOVE_ro_groups_except_se_reader,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R,
                        PERMACT_REMOVE_grp_usr_perm_none,
                        remove_user(grp_all_noEAR)]} 

grp_naocEAR = 'Group-380'
grp_niaotEAR = 'Group-386'
grp_optics = 'Group-72'

SET_M1S_Suijian = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermAct'   : [ add_user(grp_naocEAR,PERM_R),
                        add_user(grp_niaotEAR,PERM_RW)
                            ]} 
grp_CryoTeam = 'Group-670'
grp_CryoManager = 'Group-671'             
               
SET_CRYO = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermAct'   : [ remove_user(usr_crampton),
                        remove_user('User-2'),
                        add_user(grp_CryoTeam,PERM_RW),
                        add_user(grp_CryoManager,PERM_RWM),
                        PERMACT_ADD_se_readership,
                        PERMACT_CHANGE_se_readership_RO,
                        PERMACT_REMOVE_ro_users,
                        PERMACT_REMOVE_ro_groups_except_se_reader,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R,
                        PERMACT_REMOVE_grp_usr_perm_none,
                        remove_user(grp_all_noEAR)]} 
                        
SET_EMPTY = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermAct'   : [ ]} 
                    
if_user_print_message = dict_crit_act(
                dic_handle_in('User-'),
                {'Action' : 'Message', 'Message' : '*** Permissions Match Criteria'})

if_owner_roberts_change_rogers = dict_crit_act(
                chk_dict('owner-userid','User-513','eq'),
                {'Action' : 'SetOwner', 'Owner' : 'User-50'})
                
add_published_keyword = dict_crit_act(
                {'NOT' : chk_dict('keywords','TMTPublished','in')},
                {'Action' : 'AddKeyword', 'Keyword' : 'TMTPublished '})
                
chk_confidential_keyword = dict_crit_act(
                chk_dict('keywords','Confidential','in'),
                {'Action' : 'Message', 'Message' : '*** Confidential keyword exists'})
                
chk_published_keyword = dict_crit_act(
                chk_dict('keywords','TMTPublished','in'),
                {'Action' : 'Message', 'Message' : '*** TMTPublished keyword exists'})
                
chk_published_keyword_false = dict_crit_act(
                {'NOT' : chk_dict('keywords','TMTPublished','in')},
                {'Action' : 'Message', 'Message' : '*** WARNING: TMTPublished keyword DOES NOT exist'})
                
remove_published_keyword = dict_crit_act(
                chk_dict('keywords','TMTPublished','in'),
                {'Action' : 'DelKeyword', 'Keyword' : 'TMTPublished'})
                
replace_title = dict_crit_act(
                chk_dict('keywords','TMTPublished','in'),
                {'Action' : 'RepTitle', 'Title' : 'test form Published'})
                
replace_tmtnum = dict_crit_act(
                chk_dict('keywords','TMTPublished','in'),
                {'Action' : 'RepTmtNum', 'TmtNum' : 'TMT.SEN.COR.14.001.DRF02'})
                
tmtnum_message = dict_crit_act(
                chk_dict('tmtnum','DRF','in'),
                {'Action' : 'Message', 'Message' : '>>> This is a Draft Document'})

SET_TEST = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : [ if_owner_roberts_change_rogers,
                        add_published_keyword,
                        remove_published_keyword,
                        replace_title,
                        replace_tmtnum,
                        tmtnum_message],
        'PermAct'   : [if_user_print_message]} 
        

SET_PUBLISHED = {
        'ObjSel'    : { 'Criteria' : {'AND' : [docORcol, {'NOT' : chk_dict('keywords','Confidential','in')}]}},
        'ObjAct'    : [],
        'PermAct'   : [ PERMACT_ADD_se_readership,
                        PERMACT_CHANGE_se_readership_RO,
                        PERMACT_REMOVE_ro_users,
                        PERMACT_REMOVE_ro_groups_except_se_reader,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R,
                        PERMACT_REMOVE_grp_usr_perm_none,
                        remove_user(grp_all_noEAR)] 
                        }

SET_REMOVE_INACTIVE = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermAct'   : [ remove_inactive,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R,
                        remove_perm_none,
                        remove_user(usr_hubin),
                        remove_user(usr_elias),
                        remove_user(grp_EAP),
                        remove_user(usr_mclean),
                        remove_user(usr_bauman), 
                        remove_user(usr_macintosh),   
                        remove_user(usr_phillips),
                        remove_user('User-1083')                                   
                         ]}

SET_IRIS_REMOVEUSERS_2 = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermAct'   : [ remove_user(usr_matthias),
                        remove_user(usr_lianqi)]}      
                        
SET_IRIS_REMOVE_MATTHIAS_MANAGE_FALSE = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermAct'   : [ PERMACT_REMOVE_mathias_manage_false ]}                   


#         'ObjSel'    : { 'Criteria' : {'AND': [doc_handle, {'NOT' : INS_doc}]}},


SET_IRIS_REMOVE_ISBRUCKER = {
        'ObjSel'    : { 'Criteria' : docORcol},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermAct'   : [remove_user(grp_Isbrucker)]} 


Astrometry = {'OR' : [chk_dict('title','astrometry','in'), chk_dict('title','Astrometry','in')]}
grp_IRIS_READ = {'AND' : [dic_handle_eq(grp_IRIS_team), read_true]}

SET_IRIS_REMOVE_MATTHIAS = {
        'ObjSel'    : { 'Criteria' : {'AND' : [docORcol, Astrometry]}},
        'ObjAct'    : { 'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermSel'   : {'Criteria' : [grp_IRIS_READ]},
        'PermAct'   : [remove_user(usr_matthias)]}


SE_read_OR_M1CS_obs = {'OR' : [dic_handle_eq(grp_SE_readership), dic_handle_eq(grp_M1CS_obs)]}

SET_M1CS_PDR = {
        'ObjSel'    : {'Criteria' : docORcol},
        'ObjAct'    : {'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermSel'   : {'Criteria' : [SE_read_OR_M1CS_obs]},
        'PermAct'   : [PERMACT_REMOVE_dumas_ro,
                       remove_user(usr_szeto)]}
                       
# For STR group documents, add group 'structure managers'.
# Remove members of structure managers group from individual permissions.
SET_STR_MANAGERS = {
        'ObjSel'    : {'Criteria' : STR_doc},
        'ObjAct'    : {'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermSel'   : {'Criteria' : [usr_str_managers]},
        'PermAct'   : [ PERMACT_ADD_str_managers,
                        remove_user(usr_chylek),
                        remove_user(usr_amir),
                        remove_user(usr_kyle)]}
                        
# For non-STR, optics and controls group documents, remove group 'structure managers'.
# Remove members of structure managers group from individual permissions.


SET_REMOVE_STR_MANAGERS = {
        'ObjSel'    : {'Criteria' : {'AND' : [docORcol, {'NOT' : STR_doc}]}},
        'ObjAct'    : [{'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict}],
        'PermSel'   : {'Criteria' : [usr_str_managers]},
        'PermAct'   : [ remove_user(usr_chylek),
                        remove_user(usr_amir),
                        remove_user(usr_kyle),
                        remove_inactive,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R,  
                        remove_perm_none]}
                        
SET_REMOVE_WFOS_IRIS_MANAGERS = {
        'ObjSel'    : {'Criteria' : {'AND' : [docORcol, {'NOT' : INST_doc}]}},
        'ObjAct'    : [{'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict}],
        'PermSel'   : {'Criteria' : [{'OR' : [dic_handle_eq(grp_IRIS_managers), dic_handle_eq(grp_WFOS_managers)]}]},
        'PermAct'   : [ remove_user(grp_WFOS_managers),
                        remove_user(grp_IRIS_managers)]}

grp_noEAR_READ = {'AND' : [dic_handle_eq(grp_all_noEAR), read_true]}
 
# Change IRIS Team read only or RWM to RW
IRIS_team_NotRW = {'AND' : [dic_handle_eq(grp_IRIS_team), {'OR' : [read_false, write_false, manage_true]}]}
PERMACT_CHANGE_IRIS_team = dict_crit_act(IRIS_team_NotRW, CHANGE_RW)

SET_REPLACE_IRIS_EAR_WITH_ALL = {
        'ObjSel'    : {'Criteria' : docORcol},
        'ObjAct'    : {'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermSel'   : {'Criteria' : [grp_EAR_perm]},
        'PermAct'   : [ PERMACT_CHANGE_IRIS_team,
                        PERMACT_ADD_se_readership,
                        PERMACT_CHANGE_se_readership_RO,
                        PERMACT_REMOVE_ro_users,
                        PERMACT_REMOVE_ro_groups_except_IRIS_SEread,
                        PERMACT_REMOVE_grp_usr_perm_W_or_M_no_R]}
  
SET_ADD_IRIS_MANAGER = {
        'ObjSel'    : {'Criteria' : docORcol},
        'ObjAct'    : {'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermSel'   : {'Criteria' : [check_user_perms(usr_moore,RWM_true),
                                    check_user_perms(usr_larkin,RWM_true),
                                    check_user_perms(usr_wright,RWM_true)]},
        'PermAct'   : [ add_user(grp_IRIS_MANAGE, PERM_RWM) ]}
        
SET_IRIS_TEAM = {
        'ObjSel'    : {'Criteria' : docORcol},
        'ObjAct'    : {'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict},
        'PermSel'   : {'Criteria' : [check_user_perms(grp_IRIS_team,RW_true)]},
        'PermAct'   : []}

# add_altec_ifnoSEread = dict_crit_act(dic_handle_not_eq(grp_SE_readership),{'Action': {'Action' : 'Add', 'Handle' : 'Group-679', 'Perms' : {'Read' : True}}})


# add_altec_ifnoSEread = dict_crit_act({'NOT':check_user_perms(grp_SE_readership,read_true)},{'Action': {'Action' : 'Add', 'Handle' : 'Group-679', 'Perms' : {'Read' : True}}})

no_se_readership_read = {'NOT' : {'AND' : [dic_handle_eq( grp_SE_readership), read_true ]}}
# no_se_readership_read = {'AND' : [dic_handle_eq( grp_SE_readership), read_true ]}

add_R_grp_altec = {'Action' : 'Add', 'Handle' : 'Group-679', 'Perms' : {'Read' : True}}
PERMACT_ADD_altec = dict_crit_act(no_se_readership_read, add_R_grp_altec)
# PERMACT_ADD_altec

SET_ENC_CONSTRUCTION = {
                    'ObjSel'    : { 'Criteria' : docORcol},
                    'ObjAct'    : [{'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict}],
                    'PermSel'   : {'Criteria' : [{'AND':[dic_handle_eq('Group-507'), read_true]}, no_se_readership_read]},
                    'PermAct'   : [ add_user('Group-679', {'Read' : True}),
                                    PERMACT_REMOVE_grp_usr_perm_none,
                                    remove_inactive]}
     
# SET_ENC_CONSTRUCTION = {
#                     'ObjSel'    : { 'Criteria' : docORcol},
#                     'ObjAct'    : [{'Criteria' : obj_criteria_dict, 'Action' : obj_actions_dict}],
#                     'PermSel'   : {'Criteria' : [{'AND' : [dic_handle_eq('Group-507'), read_true]},
#                                         {'NOT': check_user_perms(grp_SE_readership,read_true)}]},
#                     'PermAct'   : [ add_user('Group-679',{'Read' : True}),
#                                     PERMACT_REMOVE_grp_usr_perm_none,
#                                     remove_inactive]}

        
# if __name__ == '__main__':
#     print("Running module test code for",__file__)
# 
#     print(PERMACT_ADD_se_readership)
#     
#     print(PERMACT_REMOVE_ro_users)
#     
#     print(PERMACT_CHANGE_se_readership_RO)
#     print(dic_handle_eq('Group-507'))
#     
#     print(read_true)
    
#     print({'AND' : [dic_handle_eq('Group-507'), read_true]})
#     print(check_user_perms(grp_SE_readership,read_true))
#     print(add_user('Group-679',{'Read' : True}))
    
#     print({'Criteria' : [{'AND':[dic_handle_eq('Group-507'), read_true]}, no_se_readership_read]})
    

    
