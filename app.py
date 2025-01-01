from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 定义常用协议
PROTOCOLS = {
    'icmp': '--proto 0x01',  # ICMP的协议号是0x01
    'dns': '--dstport 53 --srcport 53',  # DNS使用53端口
    'http': '--dstport 80 --srcport 80',  # HTTP使用80端口
    'https': '--dstport 443 --srcport 443',  # HTTPS使用443端口
    'ssh': '--dstport 22 --srcport 22',  # SSH使用22端口
    'telnet': '--dstport 23 --srcport 23'  # Telnet使用23端口
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
    
    # 构建基础命令
    command = "pktcap-uw "
    
    # 添加接口参数
    if component == "switchport":
        command += f"--switchport {switchport} "
    elif component == "vmnic":
        command += f"--uplink {interface} "
    elif component == "vmk":
        command += f"--vmk {interface} "
    elif component == "vnic":
        command += f"--vnic {interface} "
    
    # 添加方向参数
    if direction == "in":
        command += "--dir 0 "
    elif direction == "out":
        command += "--dir 1 "
    
    # 添加IP过滤
    if ip:  # 优先使用通用IP过滤
        command += f"--ip {ip} "
    else:  # 如果没有通用IP，则使用源IP和目标IP
        if src_ip:
            command += f"--srcip {src_ip} "
        if dst_ip:
            command += f"--dstip {dst_ip} "
    
    # 添加协议或端口过滤
    if protocol in PROTOCOLS:
        command += f"{PROTOCOLS[protocol]} "
    elif port:  # 如果没有选择预定义协议但指定了端口
        command += f"--dstport {port} --srcport {port} "
    
    # 添加捕获模式参数
    command += "--capture PortOutput "
    
    # 生成两种命令
    file_command = command + "-o /tmp/capture.pcap"
    online_command = command + "-o - | tcpdump-uw -enr -"
    
    return jsonify({
        "file_command": file_command,
        "online_command": online_command
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 