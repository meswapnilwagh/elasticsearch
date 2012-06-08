# Copyright (C) 2011, 2012 9apps B.V.
# 
# This file is part of Redis for AWS.
# 
# Redis for AWS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Redis for AWS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Redis for AWS. If not, see <http://www.gnu.org/licenses/>.

import os, sys
import json, urllib2

from boto.ec2.regioninfo import RegionInfo

from route53 import Route53Zone

try:
	url = "http://169.254.169.254/latest/"

	userdata = json.load(urllib2.urlopen(url + "user-data"))
	hostname = urllib2.urlopen(url + "meta-data/public-hostname/").read()
	instance_id = urllib2.urlopen(url + "meta-data/instance-id/").read()
except Exception as e:
	exit( "We couldn't get user-data or other meta-data...")

if __name__ == '__main__':
	r53_zone = Route53Zone(userdata['access_key'], userdata['secret_key'],
							userdata['hosted_zone_id'])

	name = "{0}.{1}".format(userdata['name'], userdata['hosted_zone'].rstrip('.'))
	value = hostname
	identifier = instance_id

	if True:
		r53_zone.create_record(name, value, identifier, 100)
	#except:
	#	r53_zone.update_record(name, value, identifier, 100)
