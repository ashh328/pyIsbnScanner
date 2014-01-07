#!/usr/bin/python
import sys
import time
import json
import urllib2
import gdata.spreadsheet.service

from config import *
from spreadsheet import *

#### Exceptions


class BookScannerException(Exception): pass
class BookScannerMoreThanOneResultException(BookScannerException): pass


#### Functions


def book_metadata(isbn):
    ''' Given an ISBN string, will return the Google Book's JSON object for that ISBN. '''
    response = urllib2.urlopen(google_api_url % isbn)
    book_json_raw = response.read()
    return json.loads(book_json_raw)


def format_spreadsheet_row(isbn, book_json_data, box_number):
    ''' Given a book's JSON data, return a dcitionary that represents a row in the spreadsheet. '''
    data = {}
    data['date'] = time.strftime('%m/%d/%Y')
    data['time'] = time.strftime('%H:%M:%S')
    
    data['isbn'] = pull_isbn_from_json(book_json_data)
    if not data['isbn']:
        data['isbn'] = isbn

    data['json'] = book_json_data.get('selfLink', null_value)
    data['title'] = book_json_data['volumeInfo'].get('title', null_value)
    data['authors'] = ','.join(book_json_data['volumeInfo'].get('authors', []))
    
    data['description'] = book_json_data['volumeInfo'].get('description', null_value)
    data['description'] = data['description'][0:max_description] + " ... "

    data['categories'] = ','.join(book_json_data['volumeInfo'].get('categories', []))
    
    data['box'] = box_number

    if book_json_data['saleInfo'].has_key('retailPrice'):
        data['price'] = str(book_json_data['saleInfo']['retailPrice']['amount'])
    else:
        data['price'] = null_value
    
    if book_json_data['volumeInfo'].has_key('imageLinks'):
        data['image'] = book_json_data['volumeInfo']['imageLinks']['thumbnail']
    else:
        data['image'] = null_value

    return data

def pull_isbn_from_json(book_json_data):
    ''' Given a book's JSON data, find the ISBN13 number. '''
    isbn10 = None
    isbn13 = None

    for isbn in book_json_data['volumeInfo']['industryIdentifiers']:
        if isbn['type'] == 'ISBN_13':
            isbn13 = isbn['identifier']
        elif isbn['type'] == 'ISBN_10':
            isbn10 = isbn['identifier']

    if isbn13: 
        return isbn13
    elif isbn10:
        return isbn10
    else:
        return None

def save_isbn_to_spreadsheet(isbn, box_number, spr_client):
    ''' Given an ISBN string and the spreadsheet client, save the metadata to the Google Spreadsheet. '''
    # Ask google for data on this book
    book_json = book_metadata(isbn)

    # Make sure we have only one result, otherwise an issue
    if book_json['totalItems'] == 1:

        # Get the JSON object for the book itself
        book_json_data = book_json['items'][0]

        # Prepare the dictionary to write
        row = format_spreadsheet_row(isbn, book_json_data, box_number)

        # Update the Spreadsheet
        entry = spr_client.InsertRow(row, spreadsheet_key, worksheet_id)
        if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
            print "Insert row succeeded."
        else:
            print "Insert row failed."
    else:
        raise BookScannerMoreThanOneResultException


##### Main


def main():
    # Create the client to the spreadsheet
    spr_client = get_spreadsheet_client()

    # Get box number from command line
    box_number = sys.argv[1]

    f = open(filename % box_number)
    isbns = f.readlines()
    f.close()

    for isbn in isbns:
        try:
            # Save book's metadata to the spreadsheet
            isbn = isbn.strip()
            print isbn
            save_isbn_to_spreadsheet(isbn, box_number, spr_client)
        except BookScannerMoreThanOneResultException, e:
            print "We got more than one results for ISBN %s" % isbn
        except Exception, e:
            print "ISBN: %s" % isbn
            print e


if __name__ == "__main__":
    main()
