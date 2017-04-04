#!/usr/bin/env python

from bb import Blackboard
from bb.organisation import SchoolFinder
from bb.utils import AttachmentService, slugify
import os
import argparse

parser = argparse.ArgumentParser(description='Download attachments for each course from your blackboard account.')
parser.add_argument('username', help='Your BB username')
parser.add_argument('password', help='Your BB password')
parser.add_argument('school', help='Your school name visible in Blackboard')
args = parser.parse_args()

blackboard = Blackboard()
schoolFinder = SchoolFinder(blackboard)

schools = schoolFinder.find(args.school)
nSchools = len(schools)

# pick school
if nSchools > 1:
    school = None
    while school is None:
        choices = ['%d.%s' % (i+1, schools[i]) for i in range(0, nSchools)]
        result = raw_input('\nPlease select your school:\n' + '\n'.join(choices) + '\n\n>> ')
        try:
            pos = int(result) - 1
            if pos >= 0 and pos < nSchools:
                school = schools[pos]
        except Exception:
            print 'Please select school from the list...'
elif nSchools == 1:
    school = schools[0]
else:
    raise Exception('School [%s] was not found...' % args.school)

print 'Selected school: %s' % school

# log in
user = school.signIn(args.username, args.password)

# get user courses
courses = user.get_enrollments()

# download attachments for each course
for course in courses:
    try:
        # create folder for the course
        directory = os.path.join('out', slugify(course.courseid + '_' + course.name))
        if not os.path.exists(os.path.join(directory, 'attachments')):
            os.makedirs(os.path.join(directory, 'attachments'))

        print 'Downloading attachments for ', course.courseid, course.name

        with open(os.path.join(directory, 'course.xml'), 'w') as f:
            f.write(course.get_raw())

        for attachment in AttachmentService.extract(course):
            if attachment['type'] == 'attachment':
                print 'Save attachment ', attachment['name']

                try:
                    with open(os.path.join(directory, 'attachments', attachment['name']), 'wb') as f:
                        f.write(blackboard.get(attachment['url']).content)
                except Exception as e:
                    print 'Failed with exception ', e.message

    except Exception as e:
        print 'Failed with exception on course ', course.id, e.message
