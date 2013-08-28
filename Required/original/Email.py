## Copyright (c) 2011 Astun Technology

## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.

### Email.py - Class to send emails from a python script using smtplib

# import modules
import smtplib
from email.MIMEText import MIMEText

#Astun
import OutPut, ConfigParse

class sendEmail():

	def __init__(self, Out):
		
		opts = ConfigParse.OptParser()
		
		#Output
		self.out = Out
		
	def sendEmail(self, email_subject, email_body):
		""" Function for sending email given a sender, recipient, reply-to, subject, and body"""
		
		try:
			self.emailcreds = opts.ConfigSectionMap('Email')
			self.email_sender = self.emailcreds['email_sender']
			self.email_recip = self.emailcreds['email_recip']
			self.smtp_address = self.emailcreds['smtp_address']
	
			msg = MIMEText(email_body)
			msg['Subject'] = email_subject
			msg['From'] = self.email_sender
			msg['Reply-to'] = self.email_sender
			msg['To'] = self.email_recip
	
			# Establish an SMTP object and connect to mail server
			s = smtplib.SMTP(self.smtp_address)  

			# Send the email
			try:
				s.sendmail(self.email_sender,self.email_recip, msg.as_string())
				s.quit()
				print "Successfully sent email", email_subject
			except:
   				print "Error: unable to send email", email_subject
		except:
			self.out.OutputInfo("No email settings defined")
		





