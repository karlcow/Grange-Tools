import httplib2
import BeautifulSoup as BS
import time
import os

h = httplib2.Http(".cache")
domain = "http://www.example.org/"
filesystem = "/Some/path/example.org/"
f = open("example-urls.txt", "r")
urllist = f.readlines()
f.close()

for url in urllist:
    doctype=""
    encoding=""
    title=""
    # wait 10 seconds before the next request - be nice with the validator
    time.sleep(5)
    url = url.strip()
    fres = open("lagrange-results.txt", "a")
    # Extracting doctype and encoding and title
    url2 = url.replace(domain, filesystem)
    if os.path.isfile(url2):
        html = open(url2, 'r')
        try:
            soup = BS.BeautifulSoup(html.read())
            encoding = soup.originalEncoding
            title = soup.title.string
        except Exception, e:
            pass
        html.close()
        resp= {}
        respg ={}
        urlrequest = "http://qa-dev.w3.org/wmvs/HEAD/check?uri="+url
        try:
            resp, content = h.request(urlrequest, "HEAD")
            respg, contentg = h.request(url, "HEAD")
            if resp['x-w3c-validator-status'] == "Abort":
                print url, "FAIL\n"
                fres.write(url+" FAIL\n")
            else:
                print url
                fres.write(url+"\n")
                print "validation:", resp['x-w3c-validator-status'], resp['x-w3c-validator-errors'], resp['x-w3c-validator-warnings']
                fres.write("validation: " + resp['x-w3c-validator-status'] + " " + resp['x-w3c-validator-errors'] + " " + resp['x-w3c-validator-warnings'] + "\n")
                print "encoding-server: " + respg['content-type']
                print "encoding-page: " + encoding
                fres.write("encoding-server: " + respg['content-type'] + "\n")
                fres.write("encoding-page: " + encoding + "\n")
                print "title: "+title+"\n"
                fres.write("title: "+title+"\n\n")
        except:
            pass
    else:
        print url, "DUPLICATE\n"
        fres.write(url+" DUPLICATE\n\n")
    fres.close()
