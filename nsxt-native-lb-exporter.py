import requests
import csv

#Author: Khalid Moussa 

# NSX-T Manager details (ensure it starts with https://)
nsxt_manager = "NSX-FQDN"  # Correct URL with HTTPS scheme
username = "admin" # admin user or an EA privilages user better, you may try with a VS Admin but I didn't check the RBAC 
password = "Password" # Your username password

# Disable SSL warnings for self-signed certificates
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# API headers
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Function to get virtual servers
def get_virtual_servers():
    url = f"{nsxt_manager}/api/v1/loadbalancer/virtual-servers"
    response = requests.get(url, auth=(username, password), headers=headers, verify=False)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Failed to get virtual servers, Status Code: {response.status_code}")
        return []

# Function to get pool members for a given pool ID
def get_pool_members(pool_id):
    url = f"{nsxt_manager}/api/v1/loadbalancer/pools/{pool_id}"
    response = requests.get(url, auth=(username, password), headers=headers, verify=False)
    if response.status_code == 200:
        pool_data = response.json()
        return pool_data.get('members', [])
    else:
        print(f"Failed to get pool details for Pool ID: {pool_id}, Status Code: {response.status_code}")
        return []

# Function to export virtual server, VIP, and pool member details to a CSV file
def export_lb_config_to_csv():
    # Get the virtual servers
    virtual_servers = get_virtual_servers()

    # Open the CSV file using raw string to avoid backslash issues
    with open(r'D:\Users\khalid\automation\Scripts\prodcbsddc.csv', mode='w', newline='') as file: # Update this path accordingly 
        writer = csv.writer(file)
        writer.writerow(["Virtual Server Name", "VIP IP Address", "Pool Members (IP addresses)"])

        # Process each virtual server
        for vs in virtual_servers:
            vs_name = vs.get('display_name')
            vip_ip = vs.get('ip_address')  # Extract VIP IP address
            pool_id = vs.get('pool_id')  # Pool associated with the virtual server

            if pool_id:
                # Get pool members (IP addresses)
                pool_members = get_pool_members(pool_id)
                member_ips = [member.get('ip_address') for member in pool_members]

                # Write to the CSV: virtual server name, VIP, and pool member IPs
                writer.writerow([vs_name, vip_ip, ', '.join(member_ips)])
            else:
                # If no pool associated, write just the virtual server name and VIP
                writer.writerow([vs_name, vip_ip, "No pool associated"])

    print("Export completed successfully.")

if __name__ == "__main__":
    export_lb_config_to_csv()
