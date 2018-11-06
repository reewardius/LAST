import json
from pprint import pprint

out = {}
filterWords = ["failed", "TIMEOUT", "Couldn't find", "", "FourOhFourRequest"]

def readInitialNmap():
    with open('examples/onehost/nmap-output.json') as f:
        data = json.load(f)
        hostinfo = data["nmaprun"]["host"]
        
        for host in hostinfo:
            ipadres = hostinfo["address"]["@addr"]
            out[ipadres] = {}

            out[ipadres]['OS'] = hostinfo["os"]["osmatch"]["@name"]
            out[ipadres]['Ports'] = {}
            for value in hostinfo["ports"]["port"]:
                currentport = value["@portid"]
                out[ipadres]['Ports'][currentport] = {}
                out[ipadres]['Ports'][currentport]['protocol'] = value["@protocol"]
                out[ipadres]['Ports'][currentport]['service'] = value["service"]["@name"]

def addVulnFindingsToKey(arg, ip):
    currentBlock = out[ip]
    currentBlock['Vulnerabilities'] = {}
    portsOfIP = arg['ports']
    
    for port in portsOfIP['port']:
        currentBlock['Vulnerabilities'][port['@portid']] = {}
        if 'script' in port:
            for vultest in port['script']:
                currentBlock['Vulnerabilities'][port['@portid']]["Nmap-Vuln"] = {}
                if not any(word in vultest["@output"] for word in filterWords):
                    currentBlock['Vulnerabilities'][port['@portid']]["Nmap-Vuln"][vultest['@id']] = str(vultest['@output'])

def addVulscanFindingsToKey(arg, ip):
    currentBlock = out[ip]
    currentVulBlock = currentBlock['Vulnerabilities']
    portsOfIP = arg['ports']
    for port in portsOfIP['port']:
        currentVulBlock[port["@portid"]]["Nmap-Vulscan"] = {}
        if type(port['script'])==list:
            for vulscantest in port['script']:
                if not any(word in vulscantest["@output"] for word in filterWords):
                    print("")
                else:
                    print("")
        else:
            if not any(word in port['script']["@output"] for word in filterWords):
                print("")
            else:
                print("")

def readVulnerabilitiesNmap(pathToFile, vuln):
    with open(pathToFile) as f:
        data = json.load(f)
        hostinfo = data["nmaprun"]["host"]
        ip = hostinfo["address"]["@addr"]
        if ip in out:
            if vuln:
                addVulnFindingsToKey(hostinfo, ip)
            else:
                addVulscanFindingsToKey(hostinfo, ip)
        else:
            print('creating new key')

def run():
    readInitialNmap()
    readVulnerabilitiesNmap('examples/onehost/nmapvuln.json', True)   # Vuln
    readVulnerabilitiesNmap('examples/onehost/nmapvuln2.json', False) # Vulscan

def main():
    run()
    print(out)
    
if __name__ == "__main__":
    main()