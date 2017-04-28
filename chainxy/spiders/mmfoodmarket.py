import scrapy
import json
import csv
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from chainxy.items import ChainItem
import pdb

class MmfoodmarketSpider(scrapy.Spider):
	name = "mmfoodmarket"
	uid_list = []
	domain = "https://www.mmfoodmarket.com/en/"

	def __init__(self):
		place_file = open('citiesusca.json', 'rb')
		self.place_reader = json.load(place_file)

	def start_requests(self):
		for city in self.place_reader:
			info = self.place_reader[city]
			if info['country'] == 'Canada':
				request_url = "https://www.mmfoodmarket.com/en/store-locator"
				form_data = {
					'ctl12_TSSM' : 'Telerik.Sitefinity.Resources, Version=8.1.5800.0, Culture=neutral, PublicKeyToken=b28c218413bdf563:en:f7a2bcfd-9e00-4417-96fe-66024fe072ff:7a90d6a:83fa35c7;Telerik.Web.UI, Version=2015.2.623.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en:158c5a8b-5278-48be-a59f-fbc1676fc61b:580b2269:eb8d8a8e',
					'__EVENTTARGET' : '',
					'__EVENTARGUMENT' : '',
					'__LASTFOCUS' : '',
					"__VIEWSTATE" : "/wEPDwUKMTU2NDIxMDg5OA9kFgICAQ9kFgICAw8WAh4FY2xhc3MFAmVuFgRmDxYCHgdWaXNpYmxlZ2QCAQ9kFhoCAw9kFgQCAQ9kFgJmD2QWAmYPZBYCAgMPZBYCZg9kFgJmD2QWBAIBDw8WAh4LTmF2aWdhdGVVcmwFDH4vZW4vbXktY2FydGRkAgMPFgIeBFRleHQFATBkAgIPZBYCZg9kFgJmD2QWAgICDw9kFgIeBXN0eWxlBQ1kaXNwbGF5Om5vbmU7ZAIHDw8WAh8CBQgvZW4vaG9tZWRkAgkPZBYCAgEPZBYCZg9kFgJmD2QWBAICDw8WAh8BaGRkAgUPZBYKZg9kFgICAQ8WBB4EaHJlZgUML2VuL291ci1mb29kHgZ0YXJnZXRkFgJmDxUBCE91ciBGb29kZAIBD2QWAgIBDxYEHwUFFi9lbi9tZWFsLWlkZWFzLXJlY2lwZXMfBmQWAmYPFQEUTWVhbCBJZGVhcyAmIFJlY2lwZXNkAgIPZBYCAgEPFgQfBQUPL2VuL21heC1yZXdhcmRzHwZkFgJmDxUBC01BWCBSZXdhcmRzZAIDD2QWAgIBDxYEHwUFDy9lbi9mcmFuY2hpc2luZx8GZBYCZg8VAQtGcmFuY2hpc2luZ2QCBA9kFgICAQ8WBB8FBQ4vZW4vV2hvLVdlLUFyZR8GZBYCZg8VAQpXaG8gV2UgQXJlZAILD2QWAgIBD2QWBAIBD2QWAgIBD2QWAmYPZBYCZg9kFhACAQ8PFgIfAgUNfi9lbi9vdXItZm9vZGRkAgMPDxYCHwIFEX4vZW4vb3VyLWZvb2QvbmV3ZGQCBQ8PFgIfAgUcfi9lbi9vdXItZm9vZC9zcGVjaWFsLW9mZmVyc2RkAgkPFgIeC18hSXRlbUNvdW50AgoWFAIBD2QWBmYPFQIYY29sbGFwc2UgQ2F0ZWdvcnlfaW5kaWdvCkFwcGV0aXplcnNkAgEPFgIfBwIOFhwCAQ9kFgICAQ8PFgQfAwUGQ2hlZXNlHwIFIH4vZW4vY2F0ZWdvcnkvL2FwcGV0aXplcnMvY2hlZXNlZGQCAg9kFgICAQ8PFgQfAwUERGlwcx8CBR5+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL2RpcHNkZAIDD2QWAgIBDw8WBB8DBQRNZWF0HwIFHn4vZW4vY2F0ZWdvcnkvL2FwcGV0aXplcnMvbWVhdGRkAgQPZBYCAgEPDxYEHwMFCU1lYXRiYWxscx8CBSN+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL21lYXRiYWxsc2RkAgUPZBYCAgEPDxYEHwMFCVBhcnR5IFBhax8CBSN+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL3BhcnR5LXBha2RkAgYPZBYCAgEPDxYEHwMFBlBhc3RyeR8CBSB+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL3Bhc3RyeWRkAgcPZBYCAgEPDxYEHwMFBVBpenphHwIFH34vZW4vY2F0ZWdvcnkvL2FwcGV0aXplcnMvcGl6emFkZAIID2QWAgIBDw8WBB8DBQVSb2xscx8CBR9+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL3JvbGxzZGQCCQ9kFgICAQ8PFgQfAwUHU2VhZm9vZB8CBSF+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL3NlYWZvb2RkZAIKD2QWAgIBDw8WBB8DBQhUYXJ0L1BpZR8CBSJ+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL3RhcnQtcGllZGQCCw9kFgICAQ8PFgQfAwUKVmVnZXRhYmxlcx8CBSR+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL3ZlZ2V0YWJsZXNkZAIMD2QWAgIBDw8WBB8DBQVXaW5ncx8CBR9+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL3dpbmdzZGQCDQ9kFgICAQ8PFgQfAwUKRmxhdGJyZWFkcx8CBSR+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL2ZsYXRicmVhZHNkZAIOD2QWAgIBDw8WBB8DBQtPbmlvbiBSaW5ncx8CBSV+L2VuL2NhdGVnb3J5Ly9hcHBldGl6ZXJzL29uaW9uLXJpbmdzZGQCAw8PFgIfAgUYfi9lbi9jYXRlZ29yeS9hcHBldGl6ZXJzZGQCAg9kFgZmDxUCFmNvbGxhcHNlIENhdGVnb3J5X3RlYWwHU2VhZm9vZGQCAQ8WAh8HAgIWBAIBD2QWAgIBDw8WBB8DBQtDcnVzdGFjZWFucx8CBSJ+L2VuL2NhdGVnb3J5Ly9zZWFmb29kL2NydXN0YWNlYW5zZGQCAg9kFgICAQ8PFgQfAwUERmlzaB8CBRt+L2VuL2NhdGVnb3J5Ly9zZWFmb29kL2Zpc2hkZAIDDw8WAh8CBRV+L2VuL2NhdGVnb3J5L3NlYWZvb2RkZAIDD2QWBmYPFQIYY29sbGFwc2UgQ2F0ZWdvcnlfcHVycGxlC1RoZSBCdXRjaGVyZAIBDxYCHwcCChYUAgEPZBYCAgEPDxYEHwMFB0NoaWNrZW4fAgUifi9lbi9jYXRlZ29yeS8vdGhlLWJ1dGNoZXIvY2hpY2tlbmRkAgIPZBYCAgEPDxYEHwMFBEJlZWYfAgUffi9lbi9jYXRlZ29yeS8vdGhlLWJ1dGNoZXIvYmVlZmRkAgMPZBYCAgEPDxYEHwMFBFBvcmsfAgUffi9lbi9jYXRlZ29yeS8vdGhlLWJ1dGNoZXIvcG9ya2RkAgQPZBYCAgEPDxYEHwMFBlR1cmtleR8CBSF+L2VuL2NhdGVnb3J5Ly90aGUtYnV0Y2hlci90dXJrZXlkZAIFD2QWAgIBDw8WBB8DBQVLYWJvYh8CBSB+L2VuL2NhdGVnb3J5Ly90aGUtYnV0Y2hlci9rYWJvYmRkAgYPZBYCAgEPDxYEHwMFB0J1cmdlcnMfAgUifi9lbi9jYXRlZ29yeS8vdGhlLWJ1dGNoZXIvYnVyZ2Vyc2RkAgcPZBYCAgEPDxYEHwMFBFJpYnMfAgUffi9lbi9jYXRlZ29yeS8vdGhlLWJ1dGNoZXIvcmlic2RkAggPZBYCAgEPDxYEHwMFB1NhdXNhZ2UfAgUifi9lbi9jYXRlZ29yeS8vdGhlLWJ1dGNoZXIvc2F1c2FnZWRkAgkPZBYCAgEPDxYEHwMFBVN0ZWFrHwIFIH4vZW4vY2F0ZWdvcnkvL3RoZS1idXRjaGVyL3N0ZWFrZGQCCg9kFgICAQ8PFgQfAwUNVmFyaWV0eSBQYWNrcx8CBSd+L2VuL2NhdGVnb3J5Ly90aGUtYnV0Y2hlci92YXJpZXR5LXBhY2tkZAIDDw8WAh8CBRl+L2VuL2NhdGVnb3J5L3RoZS1idXRjaGVyZGQCBA9kFgZmDxUCGmNvbGxhcHNlIENhdGVnb3J5X2RhcmtwaW5rDlByZXBhcmVkIE1lYWxzZAIBDxYCHwcCChYUAgEPZBYCAgEPDxYEHwMFBVBpenphHwIFI34vZW4vY2F0ZWdvcnkvL3ByZXBhcmVkLW1lYWxzL3BpenphZGQCAg9kFgICAQ8PFgQfAwUHTGFzYWduYR8CBSV+L2VuL2NhdGVnb3J5Ly9wcmVwYXJlZC1tZWFscy9sYXNhZ25hZGQCAw9kFgICAQ8PFgQfAwUFUGFzdGEfAgUqfi9lbi9jYXRlZ29yeS8vcHJlcGFyZWQtbWVhbHMvcGFzdGEtc2F1Y2VzZGQCBA9kFgICAQ8PFgQfAwUKQ2Fzc2Vyb2xlcx8CBSh+L2VuL2NhdGVnb3J5Ly9wcmVwYXJlZC1tZWFscy9jYXNzZXJvbGVzZGQCBQ9kFgICAQ8PFgQfAwUNQ2FiYmFnZSBSb2xscx8CBSt+L2VuL2NhdGVnb3J5Ly9wcmVwYXJlZC1tZWFscy9jYWJiYWdlLXJvbGxzZGQCBg9kFgICAQ8PFgQfAwUNSW50ZXJuYXRpb25hbB8CBSt+L2VuL2NhdGVnb3J5Ly9wcmVwYXJlZC1tZWFscy9pbnRlcm5hdGlvbmFsZGQCBw9kFgICAQ8PFgQfAwUJTWVhdCBQaWVzHwIFJ34vZW4vY2F0ZWdvcnkvL3ByZXBhcmVkLW1lYWxzL21lYXQtcGllc2RkAggPZBYCAgEPDxYEHwMFCE1lYXRsb2FmHwIFJn4vZW4vY2F0ZWdvcnkvL3ByZXBhcmVkLW1lYWxzL21lYXRsb2FmZGQCCQ9kFgICAQ8PFgQfAwUFUm9hc3QfAgUjfi9lbi9jYXRlZ29yeS8vcHJlcGFyZWQtbWVhbHMvcm9hc3RkZAIKD2QWAgIBDw8WBB8DBQxDaGlsaSAmIFN0ZXcfAgUjfi9lbi9jYXRlZ29yeS8vcHJlcGFyZWQtbWVhbHMvY2hpbGlkZAIDDw8WAh8CBRx+L2VuL2NhdGVnb3J5L3ByZXBhcmVkLW1lYWxzZGQCBQ9kFgZmDxUCF2NvbGxhcHNlIENhdGVnb3J5X2dyZWVuClZlZ2V0YWJsZXNkAgEPFgIfBwIDFgYCAQ9kFgICAQ8PFgQfAwUKVmVnZXRhYmxlcx8CBSR+L2VuL2NhdGVnb3J5Ly92ZWdldGFibGVzL3ZlZ2V0YWJsZXNkZAICD2QWAgIBDw8WBB8DBQVNaXhlZB8CBR9+L2VuL2NhdGVnb3J5Ly92ZWdldGFibGVzL21peGVkZGQCAw9kFgICAQ8PFgQfAwUGT25pb25zHwIFIH4vZW4vY2F0ZWdvcnkvL3ZlZ2V0YWJsZXMvb25pb25zZGQCAw8PFgIfAgUYfi9lbi9jYXRlZ29yeS92ZWdldGFibGVzZGQCBg9kFgZmDxUCGGNvbGxhcHNlIENhdGVnb3J5X29yYW5nZQVTaWRlc2QCAQ8WAh8HAgIWBAIBD2QWAgIBDw8WBB8DBQhQb3RhdG9lcx8CBR1+L2VuL2NhdGVnb3J5Ly9zaWRlcy9wb3RhdG9lc2RkAgIPZBYCAgEPDxYEHwMFBkdyYWlucx8CBRt+L2VuL2NhdGVnb3J5Ly9zaWRlcy9ncmFpbnNkZAIDDw8WAh8CBRN+L2VuL2NhdGVnb3J5L3NpZGVzZGQCBw9kFgZmDxUCF2NvbGxhcHNlIENhdGVnb3J5X2Jyb3duBkJha2VyeWQCAQ8WAh8HAgEWAgIBD2QWAgIBDw8WBB8DBQVCcmVhZB8CBRt+L2VuL2NhdGVnb3J5Ly9iYWtlcnkvYnJlYWRkZAIDDw8WAh8CBRR+L2VuL2NhdGVnb3J5L2Jha2VyeWRkAggPZBYGZg8VAhZjb2xsYXBzZSBDYXRlZ29yeV9waW5rCERlc3NlcnRzZAIBDxYCHwcCBxYOAgEPZBYCAgEPDxYEHwMFCUljZSBDcmVhbR8CBSF+L2VuL2NhdGVnb3J5Ly9kZXNzZXJ0cy9pY2UtY3JlYW1kZAICD2QWAgIBDw8WBB8DBQRQaWVzHwIFHH4vZW4vY2F0ZWdvcnkvL2Rlc3NlcnRzL3BpZXNkZAIDD2QWAgIBDw8WBB8DBQVDYWtlcx8CBR1+L2VuL2NhdGVnb3J5Ly9kZXNzZXJ0cy9jYWtlc2RkAgQPZBYCAgEPDxYEHwMFBlBhc3RyeR8CBSB+L2VuL2NhdGVnb3J5Ly9kZXNzZXJ0cy9wYXN0cmllc2RkAgUPZBYCAgEPDxYEHwMFB1NxdWFyZXMfAgUffi9lbi9jYXRlZ29yeS8vZGVzc2VydHMvc3F1YXJlc2RkAgYPZBYCAgEPDxYEHwMFBUZydWl0HwIFHX4vZW4vY2F0ZWdvcnkvL2Rlc3NlcnRzL2ZydWl0ZGQCBw9kFgICAQ8PFgQfAwUHQ29va2llcx8CBR9+L2VuL2NhdGVnb3J5Ly9kZXNzZXJ0cy9jb29raWVzZGQCAw8PFgIfAgUWfi9lbi9jYXRlZ29yeS9kZXNzZXJ0c2RkAgkPZBYGZg8VAhZjb2xsYXBzZSBDYXRlZ29yeV9ibHVlDFNpbmdsZSBTZXJ2ZWQCAQ8WAh8HAgUWCgIBD2QWAgIBDw8WBB8DBQRTb3VwHwIFIH4vZW4vY2F0ZWdvcnkvL3NpbmdsZS1zZXJ2ZS9zb3VwZGQCAg9kFgICAQ8PFgQfAwUHRW50csOpZR8CBSN+L2VuL2NhdGVnb3J5Ly9zaW5nbGUtc2VydmUvRW50csOpZWRkAgMPZBYCAgEPDxYEHwMFBEJvd2wfAgUgfi9lbi9jYXRlZ29yeS8vc2luZ2xlLXNlcnZlL2Jvd2xkZAIED2QWAgIBDw8WBB8DBQhNZWF0IFBpZR8CBSR+L2VuL2NhdGVnb3J5Ly9zaW5nbGUtc2VydmUvbWVhdC1waWVkZAIFD2QWAgIBDw8WBB8DBQZRdWljaGUfAgUifi9lbi9jYXRlZ29yeS8vc2luZ2xlLXNlcnZlL3F1aWNoZWRkAgMPDxYCHwIFGn4vZW4vY2F0ZWdvcnkvc2luZ2xlLXNlcnZlZGQCCg9kFgZmDxUCGmNvbGxhcHNlIENhdGVnb3J5X3BlYWdyZWVuE1NhdWNlcyAmIFNlYXNvbmluZ3NkAgEPFgIfBwIBFgICAQ9kFgICAQ8PFgQfAwUGU2F1Y2VzHwIFJ34vZW4vY2F0ZWdvcnkvL3NhdWNlcy1zZWFzb25pbmdzL3NhdWNlc2RkAgMPDxYCHwIFH34vZW4vY2F0ZWdvcnkvc2F1Y2VzLXNlYXNvbmluZ3NkZAINDxYCHwcCCRYSAgEPZBYCAgEPDxYEHwMFD1dlZWtuaWdodCBNZWFscx8CBSZ+L2VuL291ci1mb29kL29jY2FzaW9uL3dlZWtuaWdodC1tZWFsc2RkAgIPZBYCAgEPDxYEHwMFDVF1aWNrIEx1bmNoZXMfAgUkfi9lbi9vdXItZm9vZC9vY2Nhc2lvbi9xdWljay1sdW5jaGVzZGQCAw9kFgICAQ8PFgQfAwUMS2lkIEZyaWVuZGx5HwIFI34vZW4vb3VyLWZvb2Qvb2NjYXNpb24va2lkLWZyaWVuZGx5ZGQCBA9kFgICAQ8PFgQfAwUORmFtaWx5IERpbm5lcnMfAgUlfi9lbi9vdXItZm9vZC9vY2Nhc2lvbi9mYW1pbHktZGlubmVyc2RkAgUPZBYCAgEPDxYEHwMFA0JCUR8CBSN+L2VuL291ci1mb29kL29jY2FzaW9uL2JicS1vY2Nhc2lvbmRkAgYPZBYCAgEPDxYEHwMFD0VsZWdhbnQgRGlubmVycx8CBSZ+L2VuL291ci1mb29kL29jY2FzaW9uL0VsZWdhbnQtRGlubmVyc2RkAgcPZBYCAgEPDxYEHwMFB1BhcnRpZXMfAgUefi9lbi9vdXItZm9vZC9vY2Nhc2lvbi9wYXJ0aWVzZGQCCA9kFgICAQ8PFgQfAwUIUG90bHVja3MfAgUffi9lbi9vdXItZm9vZC9vY2Nhc2lvbi9wb3RsdWNrc2RkAgkPZBYCAgEPDxYEHwMFDUhvbGlkYXkgTWVhbHMfAgUkfi9lbi9vdXItZm9vZC9vY2Nhc2lvbi9ob2xpZGF5LW1lYWxzZGQCEQ8WAh8HAggWEAIBD2QWAgIBDw8WBB8DBQdMb3cgRmF0HwIFG34vZW4vaGVhbHRoeS1lYXRpbmcvbG93LWZhdGRkAgIPZBYCAgEPDxYEHwMFFExvdyBpbiBTYXR1cmF0ZWQgRmF0HwIFKH4vZW4vaGVhbHRoeS1lYXRpbmcvbG93LWluLXNhdHVyYXRlZC1mYXRkZAIDD2QWAgIBDw8WBB8DBQxObyBUcmFucyBGYXQfAgUgfi9lbi9oZWFsdGh5LWVhdGluZy9uby10cmFucy1mYXRkZAIED2QWAgIBDw8WBB8DBRJMb3cgaW4gQ2hvbGVzdGVyb2wfAgUmfi9lbi9oZWFsdGh5LWVhdGluZy9sb3ctaW4tY2hvbGVzdGVyb2xkZAIFD2QWAgIBDw8WBB8DBQ9Tb3VyY2Ugb2YgRmlicmUfAgUjfi9lbi9oZWFsdGh5LWVhdGluZy9zb3VyY2Utb2YtZmlicmVkZAIGD2QWAgIBDw8WBB8DBRBTb2RpdW0gQ29uc2Npb3VzHwIFJH4vZW4vaGVhbHRoeS1lYXRpbmcvc29kaXVtLWNvbnNjaW91c2RkAgcPZBYCAgEPDxYEHwMFEUNhbG9yaWUgQ29uc2Npb3VzHwIFJX4vZW4vaGVhbHRoeS1lYXRpbmcvY2Fsb3JpZS1jb25zY2lvdXNkZAIID2QWAgIBDw8WBB8DBQtHbHV0ZW4gRnJlZR8CBR9+L2VuL2hlYWx0aHktZWF0aW5nL2dsdXRlbi1mcmVlZGQCFQ8WAh8HAgsWFgIBD2QWAgIBDw8WBB8CBSl+L2VuL3Byb2R1Y3Qtc2VhcmNoP0luZ1RvQXZvaWQ9QWxnUGVhbnV0cx8DBQdQZWFudXRzZGQCAg9kFgICAQ8PFgQfAgUtfi9lbi9wcm9kdWN0LXNlYXJjaD9JbmdUb0F2b2lkPUFsZ1Nlc2FtZVNlZWRzHwMFDFNlc2FtZSBTZWVkc2RkAgMPZBYCAgEPDxYEHwIFJn4vZW4vcHJvZHVjdC1zZWFyY2g/SW5nVG9Bdm9pZD1BbGdGaXNoHwMFBEZpc2hkZAIED2QWAgIBDw8WBB8CBSV+L2VuL3Byb2R1Y3Qtc2VhcmNoP0luZ1RvQXZvaWQ9QWxnRWdnHwMFA0VnZ2RkAgUPZBYCAgEPDxYEHwIFJX4vZW4vcHJvZHVjdC1zZWFyY2g/SW5nVG9Bdm9pZD1BbGdTb3kfAwUDU295ZGQCBg9kFgICAQ8PFgQfAgUqfi9lbi9wcm9kdWN0LXNlYXJjaD9JbmdUb0F2b2lkPUFsZ1RyZWVudXRzHwMFCVRyZWUgbnV0c2RkAgcPZBYCAgEPDxYEHwIFK34vZW4vcHJvZHVjdC1zZWFyY2g/SW5nVG9Bdm9pZD1BbGdTaGVsbGZpc2gfAwUJU2hlbGxmaXNoZGQCCA9kFgICAQ8PFgQfAgUmfi9lbi9wcm9kdWN0LXNlYXJjaD9JbmdUb0F2b2lkPUFsZ01pbGsfAwUETWlsa2RkAgkPZBYCAgEPDxYEHwIFKH4vZW4vcHJvZHVjdC1zZWFyY2g/SW5nVG9Bdm9pZD1BbGdHbHV0ZW4fAwUMR2x1dGVuL1doZWF0ZGQCCg9kFgICAQ8PFgQfAgUqfi9lbi9wcm9kdWN0LXNlYXJjaD9JbmdUb0F2b2lkPUFsZ1N1bGZpdGVzHwMFCVN1bHBoaXRlc2RkAgsPZBYCAgEPDxYEHwIFKX4vZW4vcHJvZHVjdC1zZWFyY2g/SW5nVG9Bdm9pZD1BbGdNdXN0YXJkHwMFB011c3RhcmRkZAIZDxYCHwcCBBYIAgEPZBYCAgEPDxYEHwMFDzEwIG1pbnMgb3IgbGVzcx8CBSF+L2VuL2Nvb2tpbmctdGltZS8xMC1taW5zLW9yLWxlc3NkZAICD2QWAgIBDw8WBB8DBQ0xMCB0byAyMCBtaW5zHwIFH34vZW4vY29va2luZy10aW1lLzEwLXRvLTIwLW1pbnNkZAIDD2QWAgIBDw8WBB8DBQ0yMCB0byA0MCBtaW5zHwIFH34vZW4vY29va2luZy10aW1lLzIwLXRvLTQwLW1pbnNkZAIED2QWAgIBDw8WBB8DBQxPdmVyIDQwIG1pbnMfAgUefi9lbi9jb29raW5nLXRpbWUvb3Zlci00MC1taW5zZGQCAw9kFgICAQ9kFgJmD2QWAmYPZBYCZg9kFgICAg8PZBYCHwQFDWRpc3BsYXk6bm9uZTtkAg0PZBYCAgEPZBYEAgEPZBYCAgEPZBYCZg9kFgJmD2QWBgIBDw8WAh8CBRd+L2VuL21lYWwtaWRlYXMtcmVjaXBlc2RkAgUPFgIfBwIIFhACAQ9kFgICAQ8PFgQfAwUKQXBwZXRpemVycx8CBSp+L2VuL21lYWwtaWRlYXMtcmVjaXBlcy9yZWNpcGVzL2FwcGV0aXplcnNkZAICD2QWAgIBDw8WBB8DBQdTZWFmb29kHwIFJ34vZW4vbWVhbC1pZGVhcy1yZWNpcGVzL3JlY2lwZXMvc2VhZm9vZGRkAgMPZBYCAgEPDxYEHwMFC1RoZSBCdXRjaGVyHwIFK34vZW4vbWVhbC1pZGVhcy1yZWNpcGVzL3JlY2lwZXMvdGhlLWJ1dGNoZXJkZAIED2QWAgIBDw8WBB8DBQ5QcmVwYXJlZCBNZWFscx8CBS5+L2VuL21lYWwtaWRlYXMtcmVjaXBlcy9yZWNpcGVzL3ByZXBhcmVkLW1lYWxzZGQCBQ9kFgICAQ8PFgQfAwUKVmVnZXRhYmxlcx8CBSp+L2VuL21lYWwtaWRlYXMtcmVjaXBlcy9yZWNpcGVzL3ZlZ2V0YWJsZXNkZAIGD2QWAgIBDw8WBB8DBQVTaWRlcx8CBSV+L2VuL21lYWwtaWRlYXMtcmVjaXBlcy9yZWNpcGVzL3NpZGVzZGQCBw9kFgICAQ8PFgQfAwUIRGVzc2VydHMfAgUofi9lbi9tZWFsLWlkZWFzLXJlY2lwZXMvcmVjaXBlcy9kZXNzZXJ0c2RkAggPZBYCAgEPDxYEHwMFE1NhdWNlcyAmIFNlYXNvbmluZ3MfAgUxfi9lbi9tZWFsLWlkZWFzLXJlY2lwZXMvcmVjaXBlcy9zYXVjZXMtc2Vhc29uaW5nc2RkAgkPFgIfBwIJFhICAQ9kFgICAQ8PFgQfAwUNSG9saWRheSBNZWFscx8CBTB+L2VuL21lYWwtaWRlYXMtcmVjaXBlcy9tZWFsLWlkZWFzL2hvbGlkYXktbWVhbHNkZAICD2QWAgIBDw8WBB8DBQ9FbGVnYW50IERpbm5lcnMfAgUyfi9lbi9tZWFsLWlkZWFzLXJlY2lwZXMvbWVhbC1pZGVhcy9FbGVnYW50LURpbm5lcnNkZAIDD2QWAgIBDw8WBB8DBQNCQlEfAgUvfi9lbi9tZWFsLWlkZWFzLXJlY2lwZXMvbWVhbC1pZGVhcy9iYnEtb2NjYXNpb25kZAIED2QWAgIBDw8WBB8DBQ9XZWVrbmlnaHQgTWVhbHMfAgUyfi9lbi9tZWFsLWlkZWFzLXJlY2lwZXMvbWVhbC1pZGVhcy93ZWVrbmlnaHQtbWVhbHNkZAIFD2QWAgIBDw8WBB8DBQxLaWQgRnJpZW5kbHkfAgUvfi9lbi9tZWFsLWlkZWFzLXJlY2lwZXMvbWVhbC1pZGVhcy9raWQtZnJpZW5kbHlkZAIGD2QWAgIBDw8WBB8DBQ1RdWljayBMdW5jaGVzHwIFMH4vZW4vbWVhbC1pZGVhcy1yZWNpcGVzL21lYWwtaWRlYXMvcXVpY2stbHVuY2hlc2RkAgcPZBYCAgEPDxYEHwMFDkZhbWlseSBEaW5uZXJzHwIFMX4vZW4vbWVhbC1pZGVhcy1yZWNpcGVzL21lYWwtaWRlYXMvZmFtaWx5LWRpbm5lcnNkZAIID2QWAgIBDw8WBB8DBQhQb3RsdWNrcx8CBSt+L2VuL21lYWwtaWRlYXMtcmVjaXBlcy9tZWFsLWlkZWFzL3BvdGx1Y2tzZGQCCQ9kFgICAQ8PFgQfAwUHUGFydGllcx8CBSp+L2VuL21lYWwtaWRlYXMtcmVjaXBlcy9tZWFsLWlkZWFzL3BhcnRpZXNkZAIDD2QWAgIBD2QWAmYPZBYCZg9kFgJmD2QWAgICDw9kFgIfBAUNZGlzcGxheTpub25lO2QCDw9kFgICAQ9kFgQCAQ9kFgICAQ9kFgJmD2QWAmYPZBYCZg9kFgQCAg8PFgIfAWhkZAIFD2QWBGYPZBYCAgEPFgIfBQUQfi9lbi9tYXgtcmV3YXJkcxYCZg8VAQtNQVggUmV3YXJkc2QCAQ9kFgICAQ8WBB8FBSMvZW4vbWF4LXJld2FyZHMvZXhjaXRpbmctcHJvbW90aW9ucx8GZBYCZg8VARNFeGNpdGluZyBQcm9tb3Rpb25zZAIDD2QWAgIBD2QWAmYPZBYCZg9kFgJmD2QWBGYPDxYCHwFoZGQCBg8PZBYCHwQFDWRpc3BsYXk6bm9uZTtkAhEPZBYCAgEPZBYEAgEPZBYCAgEPZBYCZg9kFgJmD2QWAmYPZBYEAgIPDxYCHwFoZGQCBQ9kFhJmD2QWAgIBDxYCHwUFEH4vZW4vZnJhbmNoaXNpbmcWAmYPFQELRnJhbmNoaXNpbmdkAgEPZBYCAgEPFgQfBQUjL2VuL2ZyYW5jaGlzaW5nL3doeS1tLW0tZm9vZC1tYXJrZXQfBmQWAmYPFQETV2h5IE0mTSBGb29kIE1hcmtldGQCAg9kFgICAQ8WBB8FBSAvZW4vZnJhbmNoaXNpbmcvbmV3LXN0b3JlLWRlc2lnbh8GZBYCZg8VARBOZXcgU3RvcmUgRGVzaWduZAIDD2QWAgIBDxYEHwUFLy9lbi9mcmFuY2hpc2luZy9jdXJyZW50LWZyYW5jaGlzZS1vcHBvcnR1bml0aWVzHwZkFgJmDxUBH0N1cnJlbnQgRnJhbmNoaXNlIE9wcG9ydHVuaXRpZXNkAgQPZBYCAgEPFgQfBQUxL2VuL2ZyYW5jaGlzaW5nL2hvdy10by1iZWNvbWUtYS1mcmFuY2hpc2UtcGFydG5lch8GZBYCZg8VASFIb3cgdG8gQmVjb21lIGEgRnJhbmNoaXNlIFBhcnRuZXJkAgUPZBYCAgEPFgQfBQUeL2VuL2ZyYW5jaGlzaW5nL3RoZS1pbnZlc3RtZW50HwZkFgJmDxUBDlRoZSBJbnZlc3RtZW50ZAIGD2QWAgIBDxYEHwUFGS9lbi9mcmFuY2hpc2luZy9hcHBseS1ub3cfBmQWAmYPFQEJQXBwbHkgTm93ZAIHD2QWAgIBDxYEHwUFIy9lbi9mcmFuY2hpc2luZy9jb250YWN0LWZyYW5jaGlzaW5nHwZkFgJmDxUBCkNvbnRhY3QgVXNkAggPZBYCAgEPFgQfBQUcL2VuL2ZyYW5jaGlzaW5nL3Rlc3RpbW9uaWFscx8GZBYCZg8VAQxUZXN0aW1vbmlhbHNkAgMPZBYCAgEPZBYCZg9kFgICAQ9kFgICAQ9kFgJmD2QWAmYPZBYCZg9kFgRmDw8WAh8BaGRkAgYPD2QWAh8EBQ1kaXNwbGF5Om5vbmU7ZAITD2QWAgIBD2QWBAIBD2QWAgIBD2QWAmYPZBYCZg9kFgJmD2QWBAICDw8WAh8BaGRkAgUPZBYOZg9kFgICAQ8WBB8FBRgvZW4vV2hvLVdlLUFyZS9vdXItc3RvcnkfBmQWAmYPFQEJT3VyIFN0b3J5ZAIBD2QWAgIBDxYEHwUFHS9lbi9XaG8tV2UtQXJlL0Fib3V0LU91ci1Gb29kHwZkFgJmDxUBDkFib3V0IE91ciBGb29kZAICD2QWAgIBDxYEHwUFLS9lbi9XaG8tV2UtQXJlL291ci1zdXN0YWluYWJsZS1zZWFmb29kLXBvbGljeR8GZBYCZg8VAR5PdXIgU3VzdGFpbmFibGUgU2VhZm9vZCBQb2xpY3lkAgMPZBYCAgEPFgQfBQUkL2VuL1doby1XZS1BcmUvc29jaWFsLXJlc3BvbnNpYmlsaXR5HwZkFgJmDxUBFVNvY2lhbCBSZXNwb25zaWJpbGl0eWQCBA9kFgICAQ8WBB8FBRYvZW4vV2hvLVdlLUFyZS9jYXJlZXJzHwZkFgJmDxUBDUpvaW4gT3VyIFRlYW1kAgUPZBYCAgEPFgQfBQUhL2VuL1doby1XZS1BcmUvYXdhcmRzLXJlY29nbml0aW9uHwZkFgJmDxUBFEF3YXJkcyAmIFJlY29nbml0aW9uZAIGD2QWAgIBDxYEHwUFGS9lbi9XaG8tV2UtQXJlL2NvbnRhY3QtdXMfBmQWAmYPFQEKQ29udGFjdCBVc2QCAw9kFgICAQ9kFgJmD2QWBAIBD2QWAgIBD2QWAmYPZBYCZg9kFgJmD2QWAgICDw9kFgIfBAUNZGlzcGxheTpub25lO2QCAw9kFgICAQ9kFgJmD2QWAmYPZBYCZg9kFgRmDw8WAh8BaGRkAgYPD2QWAh8EBQ1kaXNwbGF5Om5vbmU7ZAIVD2QWAmYPZBYCZg9kFgQCAQ8PZBYCHwQFDWRpc3BsYXk6bm9uZTtkAgMPFCsAAhQrAAIPFggeFUVuYWJsZUVtYmVkZGVkU2NyaXB0c2ceHEVuYWJsZUVtYmVkZGVkQmFzZVN0eWxlc2hlZXRnHhJSZXNvbHZlZFJlbmRlck1vZGULKXJUZWxlcmlrLldlYi5VSS5SZW5kZXJNb2RlLCBUZWxlcmlrLldlYi5VSSwgVmVyc2lvbj0yMDE1LjIuNjIzLjQwLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPTEyMWZhZTc4MTY1YmEzZDQBHgtfIURhdGFCb3VuZGdkDxQrAAIUKwACDxYMHwMFBEhvbWUfAgUJfi9lbi9ob21lHgVWYWx1ZQUESG9tZR4HVG9vbFRpcGUeCENzc0NsYXNzBRZzZkJyZWFkY3J1bWJOYXZpZ2F0aW9uHgRfIVNCAgJkZBQrAAIPFgwfAwUNU3RvcmUgTG9jYXRvch8CBRNqYXZhc2NyaXB0OiB2b2lkKDApHwwFDVN0b3JlIExvY2F0b3IfDWUfDgUYc2ZOb0JyZWFkY3J1bWJOYXZpZ2F0aW9uHw8CAmRkDxQrAQJmZhYBBXZUZWxlcmlrLldlYi5VSS5SYWRTaXRlTWFwTm9kZSwgVGVsZXJpay5XZWIuVUksIFZlcnNpb249MjAxNS4yLjYyMy40MCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj0xMjFmYWU3ODE2NWJhM2Q0ZBYEZg8PFgwfAwUESG9tZR8CBQl+L2VuL2hvbWUfDAUESG9tZR8NZR8OBRZzZkJyZWFkY3J1bWJOYXZpZ2F0aW9uHw8CAmRkAgEPDxYMHwMFDVN0b3JlIExvY2F0b3IfAgUTamF2YXNjcmlwdDogdm9pZCgwKR8MBQ1TdG9yZSBMb2NhdG9yHw1lHw4FGHNmTm9CcmVhZGNydW1iTmF2aWdhdGlvbh8PAgJkZAIbD2QWAgIBD2QWAmYPZBYCZg8PFgQfDgWaAXByb2R1Y3Rfc2VhcmNoIGhpZGVvbmRlc2t0b3AgaGlkZW9uZGVza3RvcCBoaWRlb25kZXNrdG9wIGhpZGVvbmRlc2t0b3AgaGlkZW9uZGVza3RvcCBoaWRlb25kZXNrdG9wIGhpZGVvbmRlc2t0b3AgaGlkZW9uZGVza3RvcCBoaWRlb25kZXNrdG9wIGhpZGVvbmRlc2t0b3AfDwICZBYEAgUPZBYMAgUPEA8WBh4NRGF0YVRleHRGaWVsZAUFVGl0bGUeDkRhdGFWYWx1ZUZpZWxkBQdVcmxOYW1lHwtnZBAVBA8xMCBtaW5zIG9yIGxlc3MNMTAgdG8gMjAgbWlucw0yMCB0byA0MCBtaW5zDE92ZXIgNDAgbWlucxUEDzEwLW1pbnMtb3ItbGVzcw0xMC10by0yMC1taW5zDTIwLXRvLTQwLW1pbnMMb3Zlci00MC1taW5zFCsDBGdnZ2dkZAIJDxAPFgYfEAUFVGl0bGUfEQUHVXJsTmFtZR8LZ2QQFQoKQXBwZXRpemVycwdTZWFmb29kC1RoZSBCdXRjaGVyDlByZXBhcmVkIE1lYWxzClZlZ2V0YWJsZXMFU2lkZXMGQmFrZXJ5CERlc3NlcnRzDFNpbmdsZSBTZXJ2ZRNTYXVjZXMgJiBTZWFzb25pbmdzFQoKYXBwZXRpemVycwdzZWFmb29kC3RoZS1idXRjaGVyDnByZXBhcmVkLW1lYWxzCnZlZ2V0YWJsZXMFc2lkZXMGYmFrZXJ5CGRlc3NlcnRzDHNpbmdsZS1zZXJ2ZRFzYXVjZXMtc2Vhc29uaW5ncxQrAwpnZ2dnZ2dnZ2dnZGQCDQ8QDxYGHxAFBVRpdGxlHxEFB1VybE5hbWUfC2dkEBUJD1dlZWtuaWdodCBNZWFscw1RdWljayBMdW5jaGVzDEtpZCBGcmllbmRseQ5GYW1pbHkgRGlubmVycwNCQlEPRWxlZ2FudCBEaW5uZXJzB1BhcnRpZXMIUG90bHVja3MNSG9saWRheSBNZWFscxUJD3dlZWtuaWdodC1tZWFscw1xdWljay1sdW5jaGVzDGtpZC1mcmllbmRseQ5mYW1pbHktZGlubmVycwxiYnEtb2NjYXNpb24PRWxlZ2FudC1EaW5uZXJzB3BhcnRpZXMIcG90bHVja3MNaG9saWRheS1tZWFscxQrAwlnZ2dnZ2dnZ2dkZAIRDw8WAh8CBRh+L2VuL2hlYWx0aHktZWF0aW5nLWluZm9kZAITDxAPFgYfEAUFVGl0bGUfEQUHVXJsTmFtZR8LZ2QQFQgHTG93IEZhdBRMb3cgaW4gU2F0dXJhdGVkIEZhdAxObyBUcmFucyBGYXQSTG93IGluIENob2xlc3Rlcm9sD1NvdXJjZSBvZiBGaWJyZRBTb2RpdW0gQ29uc2Npb3VzEUNhbG9yaWUgQ29uc2Npb3VzC0dsdXRlbiBGcmVlFQgHbG93LWZhdBRsb3ctaW4tc2F0dXJhdGVkLWZhdAxuby10cmFucy1mYXQSbG93LWluLWNob2xlc3Rlcm9sD3NvdXJjZS1vZi1maWJyZRBzb2RpdW0tY29uc2Npb3VzEWNhbG9yaWUtY29uc2Npb3Vz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MTUCMTYCMTcCMTgCMTkCMjAUKwMUZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WMAUuY3RsMDAkQ3VzdG9tQnJlYWRjcnVtYnMkY3RsMDAkY3RsMDAkQnJlYWRjcnVtYgUxY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdFJlYWR5SW4kMAUxY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdFJlYWR5SW4kMQUxY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdFJlYWR5SW4kMgUxY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdFJlYWR5SW4kMwUxY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdFJlYWR5SW4kMwUyY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdENhdGVnb3J5JDAFMmN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RDYXRlZ29yeSQxBTJjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0Q2F0ZWdvcnkkMgUyY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdENhdGVnb3J5JDMFMmN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RDYXRlZ29yeSQ0BTJjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0Q2F0ZWdvcnkkNQUyY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdENhdGVnb3J5JDYFMmN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RDYXRlZ29yeSQ3BTJjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0Q2F0ZWdvcnkkOAUyY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdENhdGVnb3J5JDkFMmN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RDYXRlZ29yeSQ5BTJjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0T2NjYXNpb24kMAUyY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdE9jY2FzaW9uJDEFMmN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RPY2Nhc2lvbiQyBTJjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0T2NjYXNpb24kMwUyY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdE9jY2FzaW9uJDQFMmN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RPY2Nhc2lvbiQ1BTJjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0T2NjYXNpb24kNgUyY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdE9jY2FzaW9uJDcFMmN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RPY2Nhc2lvbiQ4BTJjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0T2NjYXNpb24kOAUwY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEVhdGluZyQwBTBjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0RWF0aW5nJDEFMGN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RFYXRpbmckMgUwY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEVhdGluZyQzBTBjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0RWF0aW5nJDQFMGN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RFYXRpbmckNQUwY3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEVhdGluZyQ2BTBjdGwwMCRQcm9kdWN0c1NlYXJjaCRUMjZFNUU5MjkwNjMkY2hrTHN0RWF0aW5nJDcFMGN0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RFYXRpbmckNwU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkMAU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkMQU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkMgU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkMwU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkNAU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkNQU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkNgU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkNwU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkOAU6Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkOQU7Y3RsMDAkUHJvZHVjdHNTZWFyY2gkVDI2RTVFOTI5MDYzJGNoa0xzdEF2b2lkSW5ncmVkaWVudHMkMTAFO2N0bDAwJFByb2R1Y3RzU2VhcmNoJFQyNkU1RTkyOTA2MyRjaGtMc3RBdm9pZEluZ3JlZGllbnRzJDEw2qQa1Ux7oL3XUg2cZhw7vqOkqvJ8rvr0BW63U4DITiI=",
					'__VIEWSTATEGENERATOR' : '6E96F86F',
					'__EVENTVALIDATION' : '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',
					'ctl00_CustomBreadcrumbs_ctl00_ctl00_Breadcrumb_ClientState' : '',
					'ctl00$ProductsSearch$T26E5E929063$txt_productSearch' : '',
					'ctl00$content$C002$hdnLat' : info['latitude'],
					'ctl00$content$C002$hdnLong' : info['longitude'],
					'ctl00$content$C002$txtPostalCode' : info['zip_code'],
					'ctl00$content$C002$btnPCSubmit' : 'Submit',
					'ctl00$content$C002$drpProvince' : '-1',
					'ctl00$content$C002$drpCity' : '-1'
				}
				request = FormRequest(url=request_url, formdata=form_data, callback=self.parse_store)
				request.meta['state'] = info['state']
				request.meta['zip_code'] = info['zip_code']
				request.meta['latitude'] = info['latitude']
				request.meta['longitude'] = info['longitude']
				yield request

	def parse_store(self, response):
		stores = response.xpath('//div[@class="data"]')
		for store in stores:
			item = ChainItem()
			item['store_name'] = ""
			item['store_number'] = store.xpath('./div[5]/a[1]/@href').extract_first().split('/')[1]
			item['address'] = store.xpath('./div[2]/text()').extract()[1].strip()
			item['address2'] = ""
			item['phone_number'] = store.xpath('./div[2]/text()').extract()[2].strip()
			item['city'] = store.xpath('./div[3]/text()').extract()[1].strip()
			item['state'] = response.meta['state']
			item['zip_code'] = response.meta['zip_code']
			item['country'] = "Canada"
			item['latitude'] = ""
			item['longitude'] = ""
			item['store_hours'] = ""
			#item['store_type'] = info_json["@type"]
			item['other_fields'] = ""
			item['coming_soon'] = 0
			if item['store_number'] != "" and item['store_number'] in self.uid_list:
				continue
			self.uid_list.append(item['store_number'])
			hour_request = scrapy.Request(url=self.domain + store.xpath('./div[5]/a[1]/@href').extract_first(), callback=self.parseHours)			
			hour_request.meta['item'] = item
			yield hour_request

	def parseHours(self, response):
		item = response.meta['item']
		hours = response.xpath('//*[@id="content_C006_Col00"]/div[2]/table//tr')
		item['zip_code'] = response.xpath('//div[@class="store-info store-details"]/p[1]/text()').extract()[1].split()[-1]
		item['state'] = response.xpath('//div[@class="store-info store-details"]/p[1]/text()').extract()[1].split()[-2]
		for hour in hours:
			item['store_hours'] += hour.xpath('./td[1]/text()').extract_first().strip().replace('\n','').replace(' ','') + hour.xpath('./td[2]//text()').extract()[1].strip() + ";"
		yield item
	def validate(self, xpath_obj):
		try:
			return xpath_obj.extract_first().strip().encode('utf8').replace('\xc3\xb4', 'o').replace("&#39", "'").replace('&amp;nbsp;', '').replace('&nbsp;', '')
		except:
			return ""