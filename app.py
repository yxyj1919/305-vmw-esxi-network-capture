from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Define common protocols
PROTOCOLS = {
    'icmp': '--proto 0x01',  # ICMP protocol number is 0x01
    'dns': '--tcpport 53',   # DNS port
    'http': '--tcpport 80',  # HTTP port
    'https': '--tcpport 443', # HTTPS port
    'ssh': '--tcpport 22',   # SSH port
    'telnet': '--tcpport 23', # Telnet port
    'ntp': '--udpport 123'   # NTP port (UDP protocol)
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_command', methods=['POST'])
def generate_command():
    # Get basic parameters
    component = request.form.get('component')
    interface = request.form.get('interface')
    switchport = request.form.get('switchport')
    
    # Get IP related parameters
    ip = request.form.get('ip')
    src_ip = request.form.get('src_ip')
    dst_ip = request.form.get('dst_ip')
    port = request.form.get('port')
    protocol = request.form.get('protocol')
    
    # Get direction parameter
    direction = request.form.get('direction', 'both')
    
    # Get MAC address parameter
    mac = request.form.get('mac')
    
    # Get VLAN parameter
    vlan = request.form.get('vlan')
    
    # Build base command
    command = "pktcap-uw "
    
    # Add interface parameters
    if component == "switchport":
        command += f"--switchport {switchport} "
    elif component == "vmnic":
        command += f"--uplink {interface} "
    elif component == "vmk":
        command += f"--vmk {interface} "
    
    # Add direction parameter
    if direction == "in":
        command += "--dir 0 "
    elif direction == "out":
        command += "--dir 1 "
    elif direction == "both":
        command += "--dir 2 "
    
    # Add MAC address filter
    if mac:
        command += f"--mac {mac} "
    
    # Add VLAN filter
    if vlan:
        command += f"--vlan {vlan} "
    
    # Add IP filter
    if ip:
        command += f"--ip {ip} "
    else:
        if src_ip:
            command += f"--srcip {src_ip} "
        if dst_ip:
            command += f"--dstip {dst_ip} "
    
    # Add protocol or port filter
    if protocol in PROTOCOLS:
        command += f"{PROTOCOLS[protocol]} "
    elif port:  # If no predefined protocol but port specified
        command += f"--tcpport {port} "
    
    # Generate commands
    file_command = command + "-o /tmp/capture.pcap"
    online_command = command + "-o - | tcpdump-uw -enr -"
    
    return jsonify({
        "file_command": file_command,
        "online_command": online_command
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 