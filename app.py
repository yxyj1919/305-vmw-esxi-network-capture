from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 定义常用协议及其对应的过滤参数
# pktcap-uw工具支持的协议过滤格式：
# - ICMP: 使用协议号0x01
# - TCP/UDP: 使用端口号
PROTOCOLS = {
    'icmp': '--proto 0x01',  # ICMP协议，使用十六进制协议号
    'dns': '--tcpport 53',   # DNS服务，同时支持TCP/UDP 53端口
    'http': '--tcpport 80',  # HTTP服务，标准80端口
    'https': '--tcpport 443', # HTTPS服务，标准443端口
    'ssh': '--tcpport 22',   # SSH服务，标准22端口
    'telnet': '--tcpport 23', # Telnet服务，标准23端口
    'ntp': '--udpport 123'   # NTP服务，使用UDP 123端口
}

@app.route('/')
def index():
    """渲染主页面"""
    return render_template('index.html')

@app.route('/generate_command', methods=['POST'])
def generate_command():
    """生成pktcap-uw命令
    
    接收前端表单数据，根据选择的参数生成对应的抓包命令。
    支持的过滤条件包括：网络组件、IP地址、MAC地址、VLAN、协议等。
    
    Returns:
        JSON对象，包含两种格式的命令：
        - file_command: 将捕获数据保存到文件
        - online_command: 实时查看捕获数据
    """
    # 获取基本参数
    component = request.form.get('component')  # 网络组件类型：switchport/vmnic/vmk
    interface = request.form.get('interface')  # 接口名称
    switchport = request.form.get('switchport')  # 交换机端口
    
    # 获取IP相关参数
    ip = request.form.get('ip')  # 单IP过滤（源或目的）
    src_ip = request.form.get('src_ip')  # 源IP过滤
    dst_ip = request.form.get('dst_ip')  # 目的IP过滤
    port = request.form.get('port')  # 自定义端口
    protocol = request.form.get('protocol')  # 预定义协议
    
    # 获取流量方向参数
    # dir 0: 入向流量
    # dir 1: 出向流量
    # dir 2: 双向流量
    direction = request.form.get('direction', 'both')
    
    # 获取MAC地址参数
    mac = request.form.get('mac')  # MAC地址过滤
    
    # 获取VLAN参数
    vlan = request.form.get('vlan')  # VLAN ID过滤
    
    # 构建基础命令
    command = "pktcap-uw "
    
    # 添加网络组件参数
    if component == "switchport":
        command += f"--switchport {switchport} "  # 虚拟交换机端口
    elif component == "vmnic":
        command += f"--uplink {interface} "  # 物理网卡
    elif component == "vmk":
        command += f"--vmk {interface} "  # VMkernel接口
    
    # 添加流量方向参数
    if direction == "in":
        command += "--dir 0 "  # 入向流量
    elif direction == "out":
        command += "--dir 1 "  # 出向流量
    elif direction == "both":
        command += "--dir 2 "  # 双向流量
    
    # 添加MAC地址过滤
    if mac:
        command += f"--mac {mac} "
    
    # 添加VLAN过滤
    if vlan:
        command += f"--vlan {vlan} "
    
    # 添加IP过滤
    # 注意：--ip参数与--srcip/--dstip互斥
    if ip:
        command += f"--ip {ip} "  # 匹配源或目的IP
    else:
        if src_ip:
            command += f"--srcip {src_ip} "  # 仅匹配源IP
        if dst_ip:
            command += f"--dstip {dst_ip} "  # 仅匹配目的IP
    
    # 添加协议或端口过滤
    if protocol in PROTOCOLS:
        command += f"{PROTOCOLS[protocol]} "  # 使用预定义协议
    elif port:  # 如果指定了自定义端口
        command += f"--tcpport {port} "  # 默认使用TCP端口
    
    # 生成两种格式的命令
    file_command = command + "-o /tmp/capture.pcap"  # 保存到文件
    online_command = command + "-o - | tcpdump-uw -enr -"  # 实时查看
    
    return jsonify({
        "file_command": file_command,
        "online_command": online_command
    })

if __name__ == '__main__':
    # 在开发环境中运行
    # 生产环境建议使用gunicorn
    app.run(host='0.0.0.0', port=5000) 