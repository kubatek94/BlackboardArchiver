import re
import unicodedata

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return unicode(re.sub('[-\s]+', '-', value))


class AttachmentService(object):
    attachments = {'resource/x-bb-file': True, 'resource/x-bb-document': True}
    recaps = {'ppto-PanoptoCourseToolApp': True}

    @staticmethod
    def recursive_scan(items):
        for item in items:
            if item['linktype'] in AttachmentService.attachments:
                try:
                    attachments = item.attachments.attachment
                except IndexError:
                    continue
                for attachment in attachments:
                    yield {
                        'type': 'attachment',
                        'content': attachment
                    }

            if item['linktype'] in AttachmentService.recaps:
                yield {
                    'type': 'recap',
                    'url': item['viewurl']
                }

            if item['isfolder'] == 'false': continue

            for child in AttachmentService.recursive_scan(item.children):
                yield child


    @classmethod
    def extract(cls, course):
        items = course.get_items()
        for item in AttachmentService.recursive_scan(items):
            if item['type'] == 'attachment':
                yield {
                    'type': 'attachment',
                    'name': item['content']['linkLabel'],
                    'url': course.root_url + item['content']['url']
                }
            else:
                yield item