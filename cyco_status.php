<?php

// Array of device IP addresses
$devices = array(
    '192.168.1.101',
    '192.168.1.102',
    '192.168.1.103',
    '192.168.1.104',
    '192.168.1.105'
);

// SSH authentication credentials
$username = 'your_username';
$password = 'your_password';

// Function to check device status and retrieve load average and uptime
function checkDeviceStatus($ip, $username, $password) {
    $command = "ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=yes -o PubkeyAuthentication=no -l $username $ip 'uptime'";
    exec($command, $output, $returnCode);

    // If the return code is 0, the device is reachable
    if ($returnCode === 0) {
        $uptimeInfo = explode(' up ', $output[0]);
        $uptime = trim($uptimeInfo[1]);
        
        $loadAverage = explode(',', $uptimeInfo[2]);
        $loadAverage = array_map('trim', $loadAverage);
    } else {
        $uptime = 'N/A';
        $loadAverage = array('N/A', 'N/A', 'N/A');
    }

    return array(
        'reachable' => $returnCode === 0,
        'uptime' => $uptime,
        'loadAverage' => $loadAverage
    );
}

// Monitor device status and retrieve load average and uptime
$statuses = array();
foreach ($devices as $device) {
    $statuses[$device] = checkDeviceStatus($device, $username, $password);
}

// Display device status, load average, and uptime on the web page
?>

<!DOCTYPE html>
<html>
<head>
    <title>Device Monitoring</title>
</head>
<body>
    <h1>Device Monitoring</h1>
    <table>
        <tr>
            <th>Device</th>
            <th>Status</th>
            <th>Load Average</th>
            <th>Uptime</th>
        </tr>
        <?php foreach ($statuses as $device => $status): ?>
        <tr>
            <td><?php echo $device; ?></td>
            <td><?php echo $status['reachable'] ? 'Online' : 'Offline'; ?></td>
            <td><?php echo implode(', ', $status['loadAverage']); ?></td>
            <td><?php echo $status['uptime']; ?></td>
        </tr>
        <?php endforeach; ?>
    </table>
</body>
</html>
