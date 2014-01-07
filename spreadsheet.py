import types
import gdata.spreadsheet.service

from config import *

def get_spreadsheet_client():
    ''' Prepares and returns the spreadsheet client.'''
    spr_client = gdata.spreadsheet.service.SpreadsheetsService()
    spr_client.ClientLogin(email, password)
    return spr_client

def get_feed_from_spreadsheet(spr_client):
    return spr_client.GetListFeed(spreadsheet_key, worksheet_id)

# def get_row_from_spreadsheet(isbn):
#     if type(isbn) == types.IntType:
#         isbn = str(isbn)

#     for idx in range(len(feed.entry)):
#         row = feed.entry[idx]
#         if row.custom['isbn'].text == isbn:
#             # Note: the plus  two is for standard off-by-one indexing plus header row
#             return (idx + 2, row)

def get_rows_from_spreadsheet():
    for idx in range(len(feed.entry)):
        yield (idx + 2, feed.entry[idx])

def update_row(row_id, column_id, value):
    return spr_client.UpdateCell(row_id, column_id, value, spreadsheet_key, worksheet_id)

spr_client = get_spreadsheet_client()
feed = get_feed_from_spreadsheet(spr_client)