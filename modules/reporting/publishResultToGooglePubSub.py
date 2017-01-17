# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import json
import logging
from google.cloud import pubsub
#import pdb

from lib.cuckoo.common.abstracts import Report
from lib.cuckoo.common.exceptions import CuckooReportError

log = logging.getLogger(__name__)

class PublishResultToGooglePubSub(Report):
    """Saves analysis results in JSON format."""

    def run(self, results):
        """Publishes to google pubsub results topic
        @param results: Cuckoo results dict.
        @raise CuckooReportError: if fails.
        """
 

        try:
           completed_msg_id = results["info"]["options"].get("pubsub_msg_id", None)
           if (completed_msg_id != None):
              pubsub_client = pubsub.Client()

              sample_sha256 = results["target"]["file"]["sha256"]
              analysis_path = self.analysis_path
              os.system("python utils/networkIOCFromCuckooReport.py " + analysis_path + "/reports/report.json | grep -vf utils/networkWhiteList.txt | sed -e \"s/\./\.\./g\" > " + self.analysis_path + "/networkIOC.txt")
              os.system("gsutil cp -r " + analysis_path + "/* gs://a1s-zoombox/zOOmed/" + sample_sha256[0:2] + "/" + sample_sha256[2:4] +  "/" + sample_sha256 + "/")




              #publish completion message to topic
              topic = pubsub_client.topic(self.options['pubsub_topic'])
              message_id = topic.publish(u'Detonation complete. Results uploaded for:', completed_msg_id = completed_msg_id)

              log.info(u"Message published to pubsub with message_id %s" % message_id)
        except (UnicodeError, TypeError, IOError) as e:
           raise CuckooReportError("Failed to publish results: %s" % e)
