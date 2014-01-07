#!/usr/bin/python
import re
import sys
import time
import json
import urllib2
import gdata.spreadsheet.service

from config import *
from spreadsheet import *

##### Main


def main():
    # Create the client to the spreadsheet
    #spr_client = get_spreadsheet_client()
    skip = 0

    curr_iter = 0
    for (row_id, row) in get_rows_from_spreadsheet():
        curr_iter = curr_iter + 1
        if curr_iter <= skip:
            print "Skipping %d" % curr_iter
            continue

        try:
            isbn = row.custom['isbn'].text
            title = row.custom['title'].text

            if not title:
                print "\t%s Missing from spreadsheet!" % isbn
                continue
            print "Processing %s" % title

            ebook_filename = 'ebooks/%s.pdf' % title
            
            print "\tGetting eBook Site Response..."
            ebook_url = ebook_site % isbn
            response = urllib2.urlopen(ebook_url)
            raw_html = response.read()

            try:
                print "\tGetting PDF Link..."
                pdf_link = re.search("(libgen.org/get?.*)' title", raw_html).groups(1)[0]
            except Exception, e:
                print "\tNo link found!"
                update_row(row_id, columns['ebook'], 'N')
                continue

            # print "\tGetting & Saving PDF File (%s) ..." % ebook_filename
            # pdf_response = urllib2.urlopen('http://' + pdf_link)
            # pdf_length = float(pdf_response.headers['content-length'])
            # pdf_written = 0.
            # CHUNK = 128 * 1024
            # with open(ebook_filename, 'wb') as fp:
            #     for chunk in iter(lambda: pdf_response.read(CHUNK), ''):
            #         if not chunk: break
            #         fp.write(chunk)
            #         pdf_written += len(chunk)
            #         print "\tPercentage Done: %f     \r" % (100.0 * pdf_written / pdf_length),
            #         sys.stdout.flush()
            # print "\tPDF File Saved!"
            # fp.close()

            update_row(row_id, columns['ebook'], 'Y')
            update_row(row_id, columns['ebook link'], 'http://' + pdf_link)
            
        except Exception, e:
            print "ISBN: %s" % isbn
            print e


if __name__ == "__main__":
    main()