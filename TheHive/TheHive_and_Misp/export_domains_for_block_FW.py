#Example code to export IOCS of type 'domain' from Misp which have the tag 'Block_FW' set

misp_url = ' -- your_misp_url -- '
misp_key = ' -- your_Misp_api_key -- '
misp_verifycert = False
relative_path = ''
body = {
    "returnFormat": "text",
    "type": "domain",
    "tags": "1"  # you should put the ID of the 'Block_FW' tag here , in your case it might be a different nr
}

from pymisp import PyMISP
misp = PyMISP(misp_url, misp_key, misp_verifycert)
r = misp.direct_call(relative_path, body)
f = open("block_domains", "w")
f.write(r)
f.close()