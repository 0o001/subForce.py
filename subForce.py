import argparse
from googlesearch import search
from urllib.parse import urlparse
import requests
import re
import xmltodict

__author__ = 'mustafauzun0'

'''
SUBFORCE
'''

def validateSubdomain(url):
    validate = re.compile(r'^(https?://)?(?:www\.).*\..*\..*')
    return validate.match(url)

def main():
    parser = argparse.ArgumentParser(description='Subdomain Finder')

    parser.add_argument('-d', '--domain', dest='domain', help='Target Domain', required=True)
    parser.add_argument('-s', '--search', dest='search', action='store_true', help='Search Subdomains in Google')
    parser.add_argument('-w', '--wordlist', dest='wordlist', help='Subdomain Word List')
    parser.add_argument('-m', '--sitemap', dest='sitemap', help='Search in Sitemap')
    parser.add_argument('-o', '--output', dest='output', help='Output File Finding Subdomains')

    args = parser.parse_args()

    subdomains = []

    if args.search:
        for url in search('site:*.{domain}'.format(domain=args.domain)):
            if validateSubdomain(url):
                if url not in subdomains:
                    subdomains.append(url)
    
    if args.wordlist:  
        with open(args.wordlist, 'r') as file:
            wordlist = file.readlines()
            
            for word in wordlist:
                checkURL = 'http://{word}.{domain}'.format(word=word.strip(), domain=args.domain)

                try:
                    request = requests.get(checkURL, allow_redirects=False)

                    if request:
                        if url not in subdomains:
                            subdomains.append(checkURL)
                except:
                    pass
    
    if args.sitemap:
        try:
            request = requests.get(args.domain + '/' + args.sitemap, allow_redirects=False)

            if request:
                xml = xmltodict.parse(request.text)

                for item in xml['urlset']['url']:
                    if item['loc'] not in subdomains:
                        subdomains.append(item['loc'])
                
                for item in xml['sitemapindex']['sitemap']:
                    if item['loc'] not in subdomains:
                        subdomains.append(item['loc'])

        except:
            pass
    
    if args.output:
        try:
            file = open(args.output, 'w')
            file.write('\n'.join(subdomains))
            file.close()
        except IOError:
            print('[-] Unable to create file on disk')
    else:
        if subdomains:
            print(*subdomains, sep='\n')

if __name__ == '__main__':
    main()
