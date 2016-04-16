from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

import string
import requests
import json
from datetime import datetime
import calendar
import time


'''
	This file contains ORM Models for Result & Query
'''


class Result(models.Model):
	
	QueryStr = models.CharField(max_length=500)
	TotalOpenIssues = models.IntegerField(default=0)
	OpenIssues1Day = models.IntegerField(default=0)
	OpenIssues1to7Days = models.IntegerField(default=0)
	OpenIssues7orMoreDay = models.IntegerField(default=0)
	ErrorMsg = models.CharField(max_length=200, default="")

	'''
		Check for error response in GitHub response like "API rate limit exceeded"
	'''
	def __verifyResult(self, content):

		tempDict = json.loads(content)
		if 'message' in tempDict:
			self.ErrorMsg = tempDict['message']
			return False
		else:
			return True

	'''
		Process the response JSON string and count specific types of issues
	'''
	def __processResults(self, url):
		res = requests.get(url)
		if self.__verifyResult(res.content) == False:
			return False;

		issues = json.loads(res.content)

		for issue in issues:

			self.TotalOpenIssues += 1;

			utc_dt = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
			issueTimestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
			currentTimestamp = calendar.timegm(time.gmtime())
			daysOld = (currentTimestamp - issueTimestamp)/(60*60*24)

			if daysOld <= 1:
				self.OpenIssues1Day += 1;
			elif daysOld >= 1 and daysOld <= 7:
				self.OpenIssues1to7Days += 1;
			elif daysOld > 7:
				self.OpenIssues7orMoreDay += 1;

	'''
		"createResult" method is the only public method in Result class, that handles result generation for outside world
	'''
	def createResult(self):
		
		# Setting per_page to max possible value, to minimize the number of times, requests (for each page) are made to GitHub
		url = self.QueryStr + "&page=1&per_page=100"	

		self.OpenIssues1Day = self.OpenIssues1to7Days = self.OpenIssues7orMoreDay = self.TotalOpenIssues = 0;

		# It's a good idea to check for errors along with counting issues.
		if (self.__processResults(url) == False):
			return False

		# Now Handle pagination in Github's response, if there are more pages (more than 50 results)
		r = requests.head(url=url)
		
		while 'next' in r.links and r.links['next']['url'] != r.links['last']['url']:
			url = r.links['next']['url']
			
			if (self.__processResults(url) == False):
				return False

			r = requests.head(url=url)


class Query(models.Model):

	userName = models.ForeignKey('auth.User')
	query_date = models.DateTimeField(default=timezone.now)
	GitHubPublicRepo = models.CharField(max_length=500)
	restQry = models.CharField(max_length=500)

	'''
		Takes a public GitHub repo string from user, and convert it to REST API callable string
	'''
	def CreateQuery(self, option):
		new_str = string.replace(self.GitHubPublicRepo, 'http:', 'https:').rstrip('/')
		new_str = string.replace(new_str, 'github.com', 'api.github.com/repos')

		switcher = {
        	"openIssues": "issues?state=open",
        	"closedIssues": "issues?state=closed",
    	}

		self.restQry = new_str + '/' + switcher.get(option, "issues")
		return new_str

	'''
	Just a method for intermidiate testing
	'''
	def __str__(self):
		return self.restQry

	

