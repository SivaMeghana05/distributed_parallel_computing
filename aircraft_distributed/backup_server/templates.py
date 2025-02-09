BACKUP_MONITOR_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Backup Server Monitor</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 20px;
            background-color: #f5f5f5;
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-active { background-color: #28a745; }
        .status-inactive { background-color: #dc3545; }
        .sync-info {
            margin-top: 10px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th { background-color: #f8f9fa; }
        .actions {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            background-color: #007bff;
            color: white;
            transition: background-color 0.3s;
        }
        button:hover { background-color: #0056b3; }
        .error { color: #dc3545; }
        .success { color: #28a745; }
        .metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <h1>Backup Server Monitor</h1>
    
    <div class="dashboard">
        <div class="card">
            <h2>System Status</h2>
            <div class="sync-info">
                <p>
                    <span class="status-indicator" id="primaryStatus"></span>
                    Primary Server Status: <span id="primaryServerStatus">Checking...</span>
                </p>
                <p>Last Sync: <span id="lastSyncTime">Never</span></p>
            </div>
            <div class="metrics">
                <div class="metric-card">
                    <div>Total Aircraft</div>
                    <div class="metric-value" id="totalAircraft">0</div>
                </div>
                <div class="metric-card">
                    <div>Sync Success Rate</div>
                    <div class="metric-value" id="syncRate">0%</div>
                </div>
                <div class="metric-card">
                    <div>Active Aircraft</div>
                    <div class="metric-value" id="activeAircraft">0</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Aircraft Data</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Model</th>
                        <th>Status</th>
                        <th>Last Update</th>
                    </tr>
                </thead>
                <tbody id="aircraftList">
                    <!-- Aircraft data will be populated here -->
                </tbody>
            </table>
        </div>
    </div>

    <div class="actions">
        <button onclick="forceSyncData()">Force Sync</button>
        <button onclick="refreshData()">Refresh Data</button>
    </div>

    <script>
        function updateStatus() {
            fetch('/backup/status/')
                .then(response => response.json())
                .then(data => {
                    const primaryStatus = document.getElementById('primaryStatus');
                    const statusText = document.getElementById('primaryServerStatus');
                    
                    primaryStatus.className = 'status-indicator ' + 
                        (data.primary_available ? 'status-active' : 'status-inactive');
                    statusText.textContent = data.primary_available ? 'Online' : 'Offline';
                    
                    if(data.last_sync_time) {
                        document.getElementById('lastSyncTime').textContent = 
                            new Date(data.last_sync_time).toLocaleString();
                    }
                    
                    document.getElementById('totalAircraft').textContent = data.total_aircraft;
                    document.getElementById('activeAircraft').textContent = data.active_aircraft;
                    document.getElementById('syncRate').textContent = data.sync_success_rate + '%';
                })
                .catch(error => console.error('Error:', error));
        }

        function refreshData() {
            fetch('/backup/aircraft/')
                .then(response => response.json())
                .then(data => {
                    const aircraftList = document.getElementById('aircraftList');
                    aircraftList.innerHTML = '';
                    
                    data.forEach(aircraft => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${aircraft.aircraft_id}</td>
                            <td>${aircraft.model}</td>
                            <td>
                                <span class="status-indicator ${aircraft.is_active ? 'status-active' : 'status-inactive'}"></span>
                                ${aircraft.is_active ? 'Active' : 'Inactive'}
                            </td>
                            <td>${new Date(aircraft.last_updated).toLocaleString()}</td>
                        `;
                        aircraftList.appendChild(row);
                    });
                })
                .catch(error => console.error('Error:', error));
        }

        function forceSyncData() {
            fetch('/backup/sync/', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    refreshData();
                    updateStatus();
                })
                .catch(error => alert('Sync failed: ' + error));
        }

        // Initial load
        updateStatus();
        refreshData();

        // Set up automatic refresh
        setInterval(updateStatus, 5000);  // Every 5 seconds
        setInterval(refreshData, 10000);  // Every 10 seconds
    </script>
</body>
</html>""" 