import untangle
import config

class Course(object):
    def __init__(self, bb, id, courseid, name, is_available=True):
        self.bb = bb
        self.id = id
        self.courseid = courseid
        self.name = name
        self.is_available = is_available
        self.root_url = ''
        self.items = None
        self.raw = None

    def get_raw(self):
        if not self.raw:
            r = self.bb.get(config.COURSE_MAP_URL.format(self.bb.school.url, self.id))
            r.raise_for_status()
            self.raw = r.text.encode('utf-8')
        return self.raw

    def get_items(self):
        if not self.items:
            s = self.get_raw()

            #if response was ok, we can read the xml body and parse it
            result = untangle.parse(s).mobileresponse
            if result['status'] != 'OK':
                raise Exception('Result is not OK', result)

            self.root_url = result['rooturl']
            self.items = result.map.map_item
        return self.items


class User(object):
    def __init__(self, bb, id, batch_uid, school):
        self.bb = bb
        self.id = id
        self.batch_uid = batch_uid
        self.school = school

    def get_enrollments(self):
        r = self.bb.get(config.USER_ENROLLMENTS_URL.format(self.school.url))
        r.raise_for_status()

        #if response was ok, we can read the xml body and parse it
        result = untangle.parse(r.text).mobileresponse
        if result['status'] != 'OK':
            raise Exception('Result is not OK', result)

        for course in result.courses.course:
            yield Course(self.bb, course['bbid'], course['courseid'], course['name'], True if course['isAvail'] == 'true' else False)