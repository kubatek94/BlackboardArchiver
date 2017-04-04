import random

BASE_HOST = 'https://mlcs.medu.com'
DEVICE_ID = str(random.randint(863285036011320, 963285036011320))
API_URL = BASE_HOST + '/api'

SCHOOL_FINDER_URL = API_URL + '/b2_registration/match_schools?q={}&platform=ANDROID&device_name=BlackboardArchiver&carrier_name=0&carrier_code=0&device_id=' + DEVICE_ID
POSTLOGIN_URL = API_URL + '/learn/post_login?registration_id={}&platform=ANDROID&device_name=BlackboardArchiver&device_id=' + DEVICE_ID
SCHOOL_SIGNIN_URL = '{}sslUserLogin?v=1'
USER_ENROLLMENTS_URL = '{}enrollments?course_type=ALL&include_grades=false&v=1'
COURSE_MAP_URL = '{}courseMap?course_id={}&v=1'