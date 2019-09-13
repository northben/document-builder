from mailmerge import MailMerge
from cloner_utils import *
from urllib import unquote_plus, quote_plus
from urlparse import parse_qsl
import json

import splunk

logger = setup_logger('document_builder')

class MergeDocument(splunk.rest.BaseRestHandler):

    base_dir = os.path.dirname(os.path.realpath(__file__))
    template = base_dir + "/../templates/" + "input.docx"
    output = base_dir + "/../output/" + "output.docx"

    def handle_POST(self):
        logger.info("in merge document post!")

        payload = unquote_plus(self.request['payload'])
        # logger.info(payload)
        payload = dict(parse_qsl(payload))

        with MailMerge(self.template) as document:

            # print document.get_merge_fields()
            logger.info("merging document")

            logger.info(payload)
            document.merge(**payload)

            for merge_row in json.loads(payload['merge_rows']):
                logger.info("merging: {}".format(merge_row))
                for key, values in merge_row.items():
                    document.merge_rows(key, values)
            document.write(self.output)
        self.response.write("All done")
