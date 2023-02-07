import pandas as pd
import argparse
import requests
import os

current_directory = os.getcwd() + '/Outputs/'
domains = []
df1 = pd.DataFrame(data=None,columns=['Alive_Domains/Subdomains','Status-Codes'])


parser = argparse.ArgumentParser()
parser.add_argument('-d', help='Enter one Domain or URl')
parser.add_argument('-f', help='Enter path to Input File')
args = parser.parse_args()
if args.f:
    file = args.f
    # Reading the domains from  the txt and adding that into a dataframe
    df = pd.read_csv(file, header=None)
    #for i in range(len(df)):
        #domains.append(df.loc[df.index[i]]
    domains = df.values.tolist()
if args.d:
    domains.append(args.d.strip())


def Is_alive(domain):

    try:
        response = requests.get(f'https://{domain}')
        if str(response.status_code) in ['200', '201', '204', '206', '300', '301', '302', '304', '307', '503', '401', '403']:
            df1.loc[len(df1)] = [domain, response.status_code]        # len(df1) means it adds the values at the end of the dataframe
        else:
            response = requests.get(f'http://{domain}')
            if str(response.status_code) in ['200', '201', '204', '206', '300', '301', '302', '304', '307', '503', '401', '403']:
                df1.loc[len(df1)] = [domain, response.status_code]
                print(f'No https but http for {domain}')
            else:
                return False

    except:
        return False


print("The status of a domain is being checked ,please hold your horses!! \nCSV file will be genrated in the Outputs dir once its completly through.... ")

for d in domains:
    domain = "".join(d)        # Since the df.values to list is giving list inside list and i couldnt pass that as an argument to the Is_alive()
    Is_alive(domain)

df1.to_csv(current_directory+"Alive_domians.csv",index=False)
print("\nThe alive domains and its status codes are:--")
print("------------------------------------------------------")
print(df1)
#print(domains)