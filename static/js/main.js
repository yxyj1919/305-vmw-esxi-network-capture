document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('captureForm');
    const protocolSelect = document.getElementById('protocol');
    const portInput = document.getElementById('port');
    const portGroup = portInput.closest('.form-group');

    // 当选择协议时禁用/启用端口输入
    protocolSelect.addEventListener('change', function() {
        if (this.value !== '') {
            portInput.disabled = true;
            portInput.value = '';
            portGroup.style.opacity = '0.5';
        } else {
            portInput.disabled = false;
            portGroup.style.opacity = '1';
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 生成中...';
        
        const formData = new FormData(this);
        
        fetch('/generate_command', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('file-command').textContent = data.file_command || '使用在线分析模式时无需此命令';
            document.getElementById('online-command').textContent = data.online_command;
            
            // 滚动到结果区域
            document.querySelector('.result').scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('生成命令时发生错误！', 'error');
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.innerHTML = '<i class="fas fa-magic"></i> 生成命令';
        });
    });

    // 为所有复制按钮添加事件监听
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const command = document.getElementById(targetId).textContent;
            
            if (command && command !== '使用在线分析模式时无需此命令') {
                navigator.clipboard.writeText(command)
                    .then(() => {
                        const originalText = this.innerHTML;
                        this.innerHTML = '<i class="fas fa-check"></i> 已复制';
                        this.classList.add('copied');
                        
                        setTimeout(() => {
                            this.innerHTML = originalText;
                            this.classList.remove('copied');
                        }, 2000);
                        
                        showNotification('命令已复制到剪贴板！', 'success');
                    })
                    .catch(() => {
                        showNotification('复制失败，请手动复制', 'error');
                    });
            }
        });
    });

    // IP地址输入框联动
    const ipInput = document.getElementById('ip');
    const srcIpInput = document.getElementById('src_ip');
    const dstIpInput = document.getElementById('dst_ip');
    const ipSpecificGroups = document.querySelectorAll('.ip-specific');

    ipInput.addEventListener('input', function() {
        const hasValue = this.value.length > 0;
        ipSpecificGroups.forEach(group => {
            const input = group.querySelector('input');
            input.disabled = hasValue;
            group.style.opacity = hasValue ? '0.5' : '1';
            if (hasValue) {
                input.value = '';
            }
        });
    });

    [srcIpInput, dstIpInput].forEach(input => {
        input.addEventListener('input', function() {
            const hasValue = srcIpInput.value.length > 0 || dstIpInput.value.length > 0;
            ipInput.disabled = hasValue;
            ipInput.closest('.form-group').style.opacity = hasValue ? '0.5' : '1';
            if (hasValue) {
                ipInput.value = '';
            }
        });
    });

    // 组件类型切换处理
    const componentSelect = document.getElementById('component');
    const interfaceGroup = document.getElementById('interfaceGroup');
    const switchportGroup = document.getElementById('switchportGroup');
    const interfaceInput = document.getElementById('interface');
    const switchportInput = document.getElementById('switchport');

    componentSelect.addEventListener('change', function() {
        if (this.value === 'switchport') {
            interfaceGroup.style.display = 'none';
            switchportGroup.style.display = 'block';
            interfaceInput.required = false;
            switchportInput.required = true;
            // 显示帮助模态框
            showModal();
        } else {
            interfaceGroup.style.display = 'block';
            switchportGroup.style.display = 'none';
            interfaceInput.required = true;
            switchportInput.required = false;
        }
    });

    // 表单提交前的验证
    form.addEventListener('submit', function(e) {
        const component = componentSelect.value;
        if (component === 'switchport' && !switchportInput.value) {
            e.preventDefault();
            showNotification('请输入端口号', 'error');
            return;
        }
        if (component !== 'switchport' && !interfaceInput.value) {
            e.preventDefault();
            showNotification('请输入接口名称', 'error');
            return;
        }
        // ... 现有的提交处理代码 ...
    });

    // 添加模态框控制函数
    function showModal() {
        const modal = document.getElementById('helpModal');
        modal.classList.add('show');
    }

    // 关闭模态框的点击事件
    document.querySelector('.close-modal').addEventListener('click', function() {
        const modal = document.getElementById('helpModal');
        modal.classList.remove('show');
    });

    // 点击模态框外部关闭
    document.getElementById('helpModal').addEventListener('click', function(e) {
        if (e.target === this) {
            this.classList.remove('show');
        }
    });

    // 按ESC键关闭模态框
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('helpModal');
            modal.classList.remove('show');
        }
    });
});

// 添加通知功能
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        ${message}
    `;
    
    document.body.appendChild(notification);
    
    // 触发动画
    setTimeout(() => notification.classList.add('show'), 10);
    
    // 自动移除通知
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// 添加通知样式
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        transform: translateX(120%);
        transition: transform 0.3s ease;
        z-index: 1000;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification.success {
        border-left: 4px solid #4CAF50;
    }
    
    .notification.error {
        border-left: 4px solid #f44336;
    }
    
    .notification i {
        margin-right: 10px;
    }
    
    .notification.success i {
        color: #4CAF50;
    }
    
    .notification.error i {
        color: #f44336;
    }
    
    .copy-btn.copied {
        background-color: #4CAF50;
    }
`;
document.head.appendChild(style); 