from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 定义常用协议
PROTOCOLS = {
    'icmp': '--proto 0x01',  # ICMP的协议号是0x01
    'dns': '--tcpport 53',   # DNS使用53端口
    'http': '--tcpport 80',  # HTTP使用80端口
    'https': '--tcpport 443', # HTTPS使用443端口
    'ssh': '--tcpport 22',   # SSH使用22端口
    'telnet': '--tcpport 23', # Telnet使用23端口
    'ntp': '--udpport 123'   # NTP使用123端口 UDP协议
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_command', methods=['POST'])
def generate_command():
    # 获取基本参数
    component = request.form.get('component')
    interface = request.form.get('interface')
    switchport = request.form.get('switchport')
    
    # 获取IP相关参数
    ip = request.form.get('ip')
    src_ip = request.form.get('src_ip')
    dst_ip = request.form.get('dst_ip')
    port = request.form.get('port')
    protocol = request.form.get('protocol')
    
    # 获取方向参数
    direction = request.form.get('direction', 'both')
    
    # 添加MAC地址参数获取
    mac = request.form.get('mac')
    
    # 添加VLAN参数获取
    vlan = request.form.get('vlan')
    
    # 构建基础命令
    command = "pktcap-uw "
    
    # 添加接口参数
    if component == "switchport":
        command += f"--switchport {switchport} "
    elif component == "vmnic":
        command += f"--uplink {interface} "
    elif component == "vmk":
        command += f"--vmk {interface} "
    
    # 添加方向参数
    if direction == "in":
        command += "--dir 0 "
    elif direction == "out":
        command += "--dir 1 "
    elif direction == "both":
        command += "--dir 2 "
    
    # 添加MAC地址过滤
    if mac:
        command += f"--mac {mac} "
    
    # 添加VLAN过滤
    if vlan:
        command += f"--vlan {vlan} "
    
    # 添加IP过滤
    if ip:
        command += f"--ip {ip} "
    else:
        if src_ip:
            command += f"--srcip {src_ip} "
        if dst_ip:
            command += f"--dstip {dst_ip} "
    
    # 修改协议或端口过滤
    if protocol in PROTOCOLS:
        command += f"{PROTOCOLS[protocol]} "
    elif port:  # 如果没有选择预定义协议但指定了端口
        command += f"--tcpport {port} "  # 使用 --tcpport 替代原来的 --dstport 和 --srcport
    
    # 生成两种命令
    file_command = command + "-o /tmp/capture.pcap"
    online_command = command + "-o - | tcpdump-uw -enr -"
    
    return jsonify({
        "file_command": file_command,
        "online_command": online_command
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 