import untangle
import config
from account import User

class School(object):
    def __init__(self, bb, id, name, url):
        self.bb = bb
        self.id = id
        self.url = url
        self.name = name

    def signIn(self, username, password):
        #confirm the school selection
        self.bb.get(config.POSTLOGIN_URL.format(self.id))

        #login the user
        r = self.bb.post(config.SCHOOL_SIGNIN_URL.format(self.url), data={'username':username, 'password':password})
        r.raise_for_status()

        #if response was ok, we can read the xml body and parse it
        result = untangle.parse(r.text).mobileresponse
        if result['status'] != 'OK':
            raise Exception('Result is not OK', result)

        user = User(self.bb, result['userid'], result['batch_uid'], self)
        self.bb.set_user(user)
        self.bb.set_school(self)
        return user

    def __str__(self):
        return '%s [%s]' % (self.name, self.id)


class SchoolFinder(object):
    def __init__(self, bb):
        self.bb = bb

    def find(self, query):
        url = config.SCHOOL_FINDER_URL.format(query)
        r = self.bb.get(url)
        r.raise_for_status()

        result = untangle.parse(r.text)
        return [School(self.bb, uni.id.cdata, uni.name.cdata, uni.b2_url.cdata) for uni in result.data.s]