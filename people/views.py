# -*- coding: utf-8 -*-
import csv
from datetime import datetime

from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from people.models import FernandUser


@staff_member_required
def email_export(request):
    response = HttpResponse(content_type='text/plain')
    persons = FernandUser.objects.filter(email_invalid=False, subscribed_to_mailing=True)
    
    for i, p in enumerate(persons):
        response.write(p.email.encode("utf-8"))
        response.write('\n')
    
    return response

@staff_member_required
def email_export_detail(request):
    now = datetime.now()
    insert_time = now.strftime("%Y-%m-%d %H:%M:%S") # '2014-03-12 19:55:19'
    
    persons = FernandUser.objects.filter(email_invalid=False, subscribed_to_mailing=True)
    
    response = HttpResponse(content_type='text/plain')
    response.write("""--
-- Table structure for table `pommo_subscribers`
--

DROP TABLE IF EXISTS `pommo_subscribers`;
CREATE TABLE IF NOT EXISTS `pommo_subscribers` (
  `subscriber_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` char(60) NOT NULL DEFAULT '',
  `time_touched` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `time_registered` datetime NOT NULL DEFAULT '2013-12-19 13:07:51',
  `flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0: NULL, 1-8: REMOVE, 9: UPDATE',
  `ip` int(10) unsigned DEFAULT NULL COMMENT 'Stored with INET_ATON(), Fetched with INET_NTOA()',
  `status` tinyint(1) NOT NULL DEFAULT '2' COMMENT '0: Inactive, 1: Active, 2: Pending',
  PRIMARY KEY (`subscriber_id`),
  KEY `status` (`status`,`subscriber_id`),
  KEY `status_2` (`status`,`email`),
  KEY `status_3` (`status`,`time_touched`),
  KEY `status_4` (`status`,`time_registered`),
  KEY `status_5` (`status`,`ip`),
  KEY `flag` (`flag`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6898 ;

--
-- Dumping data for table `pommo_subscribers`
--

""")
    response.write("INSERT INTO `pommo_subscribers` (`subscriber_id`, `email`, `time_touched`, `time_registered`, `flag`, `ip`, `status`) VALUES\n")
    for i, p in enumerate(persons):
        if i > 0:
            response.write(",\n")
        query = u"(%s, '%s', '%s', '%s', 9, 3587940515, 1)" % (p.id, p.email, insert_time, insert_time)
        response.write(query.encode("utf-8"))
    response.write(";\n")
    response.write("""
--
-- Tabelstructuur voor tabel `pommo_subscriber_data`
--

DROP TABLE IF EXISTS `pommo_subscriber_data`;
CREATE TABLE IF NOT EXISTS `pommo_subscriber_data` (
  `data_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `field_id` int(10) unsigned NOT NULL DEFAULT '0',
  `subscriber_id` int(10) unsigned NOT NULL DEFAULT '0',
  `value` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`data_id`),
  KEY `subscriber_id` (`subscriber_id`,`field_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2403 ;

--
-- Gegevens worden uitgevoerd voor tabel `pommo_subscriber_data`
--

""")
    for i, p in enumerate(persons):
        query = u"INSERT INTO `pommo_subscriber_data` (`value`, `field_id`, `subscriber_id`) SELECT '%s', 1, subscriber_id FROM `pommo_subscribers` WHERE `email` = '%s';\n" % (p.language_id, p.email)
        response.write(query.encode("utf-8"))
    return response
