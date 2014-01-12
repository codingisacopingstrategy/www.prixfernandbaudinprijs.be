# -*- coding: utf-8 -*-
import csv

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
    response = HttpResponse(content_type='text/plain')
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
    persons = FernandUser.objects.filter(email_invalid=False, subscribed_to_mailing=True)
    for i, p in enumerate(persons):
        query = u"INSERT INTO `pommo_subscriber_data` (`value`, `field_id`, `subscriber_id`) SELECT '%s', 1, subscriber_id FROM `pommo_subscribers` WHERE `email` = '%s';\n" % (p.language_id, p.email)
        response.write(query.encode("utf-8"))
    return response
