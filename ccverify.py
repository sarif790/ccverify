import time
import csv
import argparse
import logging
import os
import sys
import re 

def ParseCommandLine():
	parser = argparse.ArgumentParser('Verify Credit Card')
	parser.add_argument('-v', "--verbose", help="allows progress messages to be displayed", action='store_true')
	parser.add_argument('-s', "--singlecard", required=False,type=str, help="Verify a single Credit Card")
	parser.add_argument('-c', "--cardfile", required=False,type= ValidateFileReadable, help='Verify a file of Credit Cards seperated by newline',)
	parser.add_argument('-o', "--outputPath", required=True, type=ValidateDirectoryWritable, help="Specify output filepath")

	global gl_args
	global gl_cardfile
	global gl_cardlist
	gl_args = parser.parse_args()

	#Check for cardfile
	if gl_args.cardfile:
		#Create a list from input file
		gl_cardfile = gl_args.cardfile
		gl_cardlist = []

		try:
			with open(gl_cardfile) as fp:
				for line in fp:
					gl_cardlist.append(line.strip())
		except:
			logging.error("Failed to read in Cardfile")
			DisplayMessage("Failed to read in Cardfile")
	else:
		gl_cardfile = False

	DisplayMessage("Command line processed: Successfully")


	return


def ValidateDirectoryWritable(theDir):
	if not os.path.isdir(theDir):
		raise argparse.ArgumentTypeError('Directory does not exist')

	if os.access(theDir, os.W_OK):
		return theDir
	else:
		raise argparse.ArgumentTypeError('Directory is not writable')


def ValidateFileReadable(theFile):

	if not os.path.isfile(theFile):
		raise argparse.ArgumentTypeError('File does not exist')

	if os.access(theFile, os.R_OK):
		return theFile

	else:
		raise argparse.ArgumentTypeError('File is not readable')


def DisplayMessage(msg):
	if gl_args.verbose:
		print(msg)
	return

def CreditCardBrand(theCard):
	VISA = 'visa'
	MASTERCARD = 'mastercard'
	AMEX = 'amex'
	DISCOVER = 'discover'
	JCB = 'jcb'
	DINERSCLUB = 'diners club'
	UNKNOWN = u'unknown'

	BRANDS = {
		VISA: re.compile(r'^4\d{12}(\d{3})?$'),
		MASTERCARD: re.compile(r'^(5[1-5]\d{4}|677189)\d{10}$'),
		AMEX: re.compile(r'^3[47]\d{13}$'),
		DISCOVER: re.compile(r'^(6011|65\d{2})\d{12}$'),
		JCB: re.compile(r'^35(28|29|[3-8]d)d{12}$'),
		DINERSCLUB: re.compile(r'^3(0[0-5]|[68]d)d{11}$')
	}

	for brand, regexp in BRANDS.iteritems():
		if regexp.match(theCard):
			return brand
	return UNKNOWN


def isMod10(theCard):
	reverse = [int(ch) for ch in str(theCard)][::-1]
	return (sum(reverse[0::2]) + sum(sum(divmod(d*2,10)) for d in reverse[1::2])) % 10 == 0


def ProcessCards(cardlist):
	oCVS = _CSVWriter(gl_args.outputPath+'CardValidationReport.csv')

	logging.info('Processing Card List')
	cardsProcessed = 0

	for card in cardlist:
		if CreditCardBrand(card) == u'unknown':
			brand = 'UNKNOWN'
			if isMod10(card):
				oCVS.writeCSVRow(card,brand,'VALID')
			else: oCVS.writeCSVRow(card,brand,'INVALID')
		if CreditCardBrand(card) == 'visa':
			brand ='VISA'
			if isMod10(card):
				oCVS.writeCSVRow(card,brand,'VALID')
				
			else: oCVS.writeCSVRow(card,brand,'INVALID')

		if CreditCardBrand(card) == 'mastercard':
			brand ='MASTERCARD'
			if isMod10(card):
				oCVS.writeCSVRow(card,brand,'VALID')
				
			else: oCVS.writeCSVRow(card,brand,'INVALID')

		if CreditCardBrand(card) == 'amex':
			brand ='AMERICAN EXPRESS'
			if isMod10(card):
				oCVS.writeCSVRow(card,brand,'VALID')
				
			else: oCVS.writeCSVRow(card,brand,'INVALID')

		if CreditCardBrand(card) == 'discover':
			brand ='DISCOVER'
			if isMod10(card):
				oCVS.writeCSVRow(card,brand,'VALID')
				
			else: oCVS.writeCSVRow(card,brand,'INVALID')

		if CreditCardBrand(card) == 'jcb':
			brand ='JCB'
			if isMod10(card):
				oCVS.writeCSVRow(card,brand,'VALID')
				
			else: oCVS.writeCSVRow(card,brand,'INVALID')

		if CreditCardBrand(card) == 'diners club':
			brand ='DINERS CLUB'
			if isMod10(card):
				oCVS.writeCSVRow(card,brand,'VALID')
				
			else: oCVS.writeCSVRow(card,brand,'INVALID')
		cardsProcessed += 1

	return cardsProcessed		
	

def ProcessCard(theCard):
	if CreditCardBrand(theCard) == u'unknown':
		DisplayMessage("Unknown Card Brand")
	if CreditCardBrand(theCard) == 'visa':
		brand ='VISA'
		if isMod10(theCard):
			DisplayMessage('Card#: ' + theCard + ' Brand: ' + brand +' Valid Number')
		else:
			DisplayMessage('Card#: ' + theCard + 'Brand: ' +brand +' Invalid Number')
	elif  CreditCardBrand(theCard) == 'mastercard':
		brand ='MASTER CARD'
		if isMod10(theCard):
			DisplayMessage('Card#: ' + theCard +' Brand: ' + brand +' Valid Number')
		else:
			DisplayMessage('Card#: ' + theCard +' Brand: ' +brand +' Invalid Number')

	elif  CreditCardBrand(theCard) == 'amex':
		brand = 'AMERICAN EXPRESS'
		if isMod10(theCard):
			DisplayMessage('Card#: ' + theCard +' Brand: ' + brand +' Valid Number')
		else:
			DisplayMessage('Card#: ' + theCard +' Brand: ' +brand +' Invalid Number')

	elif  CreditCardBrand(theCard) == 'discover':
		brand ='DISCOVER'
		if isMod10(theCard):
			DisplayMessage('Card#: ' + theCard +' Brand: ' + brand +' Valid Number')
		else:
			DisplayMessage('Card#: ' + theCard +' Brand: ' +brand +' Invalid Number')	

	elif  CreditCardBrand(theCard) == 'jcb':
		brand = 'JCB'
		if isMod10(theCard):
			DisplayMessage('Card#: ' + theCard +' Brand: ' + brand +' Valid Number')
		else:
			DisplayMessage('Card#: ' + theCard +' Brand: ' +brand +' Invalid Number')

	elif  CreditCardBrand(theCard) == 'diners club':
		brand == 'DINERS CLUB'
		if isMod10(theCard):
			DisplayMessage('Card#: ' + theCard +' Brand: ' + brand +' Valid Number')
		else:
			DisplayMessage('Card#: ' + theCard +' Brand: ' +brand +' Invalid Number')



class _CSVWriter:
	def __init__(self,filename):
		try:
			self.csvFile = open(filename,'wb')
			self.writer = csv.writer(self.csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
			self.writer.writerow(('Card Number', 'Card Brand', 'Valid Number'))
		except:
			logging.error('csv File Failure')
	def writeCSVRow(self,cardnumber,brand,validnumber):
		self.writer.writerow((cardnumber,brand,validnumber))
	def writerClose(self):
		self.csvFile.close()


if __name__ == '__main__':

	CARDVERIFY_VERISION = '1.0'

	ParseCommandLine()
	logging.basicConfig(filename=gl_args.outputPath+'CARDVERIFY.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

	startTime = time.time()

	logging.info('')
	logging.info('Welcome to CARDVERIFY version 1.0 ... Verification Started')
	logging.info('')
	DisplayMessage('Welcome to CARDVERIFY ... version '+ CARDVERIFY_VERISION + '\n')


	#cardsProcessed = ProcessCards()
	if gl_args.singlecard:
		ProcessCard(gl_args.singlecard)

	elif gl_args.cardfile:
		cardsProcessed=ProcessCards(gl_cardlist)
		logging.info('Cards Processed: '+ str(cardsProcessed))
		DisplayMessage('Cards Processed '+ str(cardsProcessed))
	else:
		print 'Please provide a single card or file of cards to verify'
		sys.exit(0)


	endTime = time.time()
	duration = endTime - startTime

	#logging.info('Cards Processed: ' + str(cardsProcessed))
	logging.info('Elapsed Time: '+ str(duration) + ' seconds')
	logging.info('')
	logging.info('Program Terminated Normally')
	logging.info('')

	#DisplayMessage('Cards Processed: '+ str(cardsProcessed))
	DisplayMessage('Elapsed Time: '+ str(duration) + ' seconds')
	DisplayMessage('')
	DisplayMessage('Program End')
