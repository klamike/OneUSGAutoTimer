## Configuration file for oneusg.py

MINS_TO_CLOCK = 8 * 60

USERNAME = 'USERNAME_HERE'
PASSWORD = 'PASSWORD_HERE'

ONEUSG_REPO_PATH  = "/PATH/TO/OneUSGAutoTimer"
CHROMEDRIVER_PATH = "/PATH/TO/chromedriver" # usually /usr/bin/chromedriver, to check run `which chromedriver`

IN_PING_URL   = 'CLOCK_IN_PING_URL_HERE' # from https://healthchecks.io
OUT_PING_URL  = 'CLOCK_OUT_PING_URL_HERE'
FAIL_PING_URL = 'FAILURE_PING_URL_HERE' # including the /fail at the end

URA_LOGIN_URL  = 'https://selfservice.hprod.onehcm.usg.edu/psc/hprodsssso_newwin/HCMSS/HRMS/c/TL_EMPLOYEE_FL.TL_RPT_TIME_FLU.GBL?EMPDASHBD=Y&tW=1&tH=1&ICDoModeless=1&ICGrouplet=3&bReload=y&nWidth=236&nHeight=163&TL_JOB_CHAR=0'
UTA_LOGIN_URL  = 'https://selfservice.hprod.onehcm.usg.edu/psc/hprodsssso_newwin/HCMSS/HRMS/c/TL_EMPLOYEE_FL.TL_RPT_TIME_FLU.GBL?EMPDASHBD=Y&tW=1&tH=1&ICDoModeless=1&ICGrouplet=3&bReload=y&nWidth=236&nHeight=163&TL_JOB_CHAR=1'
# if you work multiple jobs through OneUSG, the number at the end of the URL below corresponds to the job's position in the dropdown.
# to double check, you can inspect element and see the "value" attribute of the corresponding dropdown option.
