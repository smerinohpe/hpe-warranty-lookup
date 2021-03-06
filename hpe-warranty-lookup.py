#!/bin/env python

import sys
import http.client
import urllib.parse
from bs4 import BeautifulSoup

def get_warranty_HTML(serial):
    params = urllib.parse.urlencode({'rows[0].item.serialNumber': serial})
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    conn = http.client.HTTPSConnection("support.hpe.com")
    conn.request("POST", "/hpsc/wc/public/find", params, headers)
    response = conn.getresponse()
    
    if response.status != 200:
        sys.exit(response.reason)

    data = response.read()
    return data

def extract_warranty_info(html):
    active_warranties = []
    soup = BeautifulSoup(html, 'html.parser')
    active = soup.find_all("td", attrs={"style": 'color: Green'}, string="Active")

    for td in active:
        warranty = {
            "service_type" : td.previous_sibling.previous_sibling.previous_sibling.get_text(strip=True),
            "start_date"   : td.previous_sibling.previous_sibling.string,
            "end_date"     : td.previous_sibling.string
        }
        active_warranties.append(warranty)

    return active_warranties


def main(argv):
    if len(argv) < 2:
        print("ERROR: A valid HPE Serial Number must be specified as an argument to this script")
        argv = [0, input('Please insert your serial: ')]

    print('\nChecking for %s ... \n' % (argv[1]))
    warranty_html = get_warranty_HTML(argv[1])
    warranty_txt = extract_warranty_info(warranty_html)
    if not warranty_txt:
        warranty_txt = "Serial not found or Expired"
    print('%s\n\nChecked!!!\n' % (warranty_txt))
    wait = input('Press ENTER to continue.')
 
if __name__ == "__main__":
    main(sys.argv)
