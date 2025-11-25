// Configuration
const HSDS_ENDPOINT = 'http://localhost:5101';
const HDF_DOMAIN = '/home/test_user1/test/streamtest.h5'; // Update this to your HDF5 domain path
const DEFAULT_POLL_INTERVAL = 1000; // milliseconds

// Application state
const state = {
    sensors: new Map(), // Map of sensor_name -> {id, metadata}
    sensorData: new Map(), // Map of sensor_name -> {times: [], values: []}
    enabledSensors: new Set(), // Set of enabled sensor names
    colors: [], // Array of colors for sensors
    pollInterval: DEFAULT_POLL_INTERVAL,
    pollTimer: null,
    canvas: null,
    ctx: null,
    chartArea: { x: 80, y: 20, width: 0, height: 0 },
    authHeader: null, // HTTP Basic Auth header
    historyWindow: 10 // History window in seconds (0 = show all)
};

// Generate distinct colors for sensors
function generateColors(count) {
    const colors = [];
    for (let i = 0; i < count; i++) {
        const hue = (i * 360 / count) % 360;
        colors.push(`hsl(${hue}, 70%, 50%)`);
    }
    return colors;
}

// Create HTTP Basic Auth header
function createAuthHeader(username, password) {
    const credentials = btoa(`${username}:${password}`);
    return `Basic ${credentials}`;
}

// Get request headers with auth if available
function getRequestHeaders() {
    const headers = { 'X-Hdf-domain': HDF_DOMAIN };
    if (state.authHeader) {
        headers['Authorization'] = state.authHeader;
    }
    return headers;
}

// API Functions
async function validateDomain() {
    try {
        const url = `${HSDS_ENDPOINT}/`;
        const headers = getRequestHeaders();

        console.log('Validating domain at:', url);
        console.log('Domain:', HDF_DOMAIN);

        const response = await fetch(url, { headers, cache: 'no-cache' });
        console.log('Domain validation status:', response.status);
        console.log('Domain validation headers:', Object.fromEntries(response.headers.entries()));

        if (response.status === 200) {
            return { success: true };
        } else if (response.status === 400 || response.status === 410) {
            return { success: false, message: 'Domain not found', requiresAuth: false };
        } else if (response.status === 403) {
            return { success: false, message: 'Authentication required', requiresAuth: true };
        } else {
            return { success: false, message: `Error: status ${response.status}`, requiresAuth: false };
        }
    } catch (error) {
        console.error('Error validating domain:', error);
        return { success: false, message: `Connection error: ${error.message}`, requiresAuth: false };
    }
}

async function fetchSensors() {
    try {
        const url = `${HSDS_ENDPOINT}/groups/`;
        const headers = getRequestHeaders();
        const params = new URLSearchParams({ h5path: '/sensors', include_links: 1 });

        const fullUrl = `${url}?${params}`;
        console.log('Fetching sensors from:', fullUrl);
        console.log('Headers:', headers);

        const response = await fetch(fullUrl, { headers, cache: 'no-cache' });
        console.log('Response status:', response.status);
        console.log('Response headers:', Object.fromEntries(response.headers.entries()));

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();

        if (!data.links) return {};

        // Extract sensor names and dataset IDs
        const sensors = {};
        for (const [name, link] of Object.entries(data.links)) {
            if (link.class === 'H5L_TYPE_HARD') {
                sensors[name] = { id: link.id, name };
            }
        }

        return sensors;
    } catch (error) {
        console.error('Error fetching sensors:', error);
        return null;
    }
}

async function fetchSensorMetadata(datasetId) {
    try {
        const url = `${HSDS_ENDPOINT}/datasets/${datasetId}`;
        const headers = getRequestHeaders();
        const params = new URLSearchParams({ include_attrs: 1 });

        const response = await fetch(`${url}?${params}`, { headers });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();

        // Extract shape (number of data points)
        const shape = data.shape?.dims?.[0] || 0;

        // Extract attributes
        const attrs = {};
        if (data.attributes) {
            for (const [name, attr] of Object.entries(data.attributes)) {
                attrs[name] = attr.value;
            }
        }

        return {
            shape,
            ...attrs
        };
    } catch (error) {
        console.error(`Error fetching metadata for dataset ${datasetId}:`, error);
        return null;
    }
}

async function fetchSensorDataRange(datasetId, start, stop) {
    try {
        const url = `${HSDS_ENDPOINT}/datasets/${datasetId}/value`;
        const headers = getRequestHeaders();
        const params = new URLSearchParams({ select: `[${start}:${stop}]` });

        const response = await fetch(`${url}?${params}`, { headers });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();

        return data.value || [];
    } catch (error) {
        console.error(`Error fetching data for dataset ${datasetId}:`, error);
        return null;
    }
}

// Initialize sensors
async function initializeSensors() {
    const sensorsData = await fetchSensors();
    if (!sensorsData) {
        setTimeout(initializeSensors, 5000); // Retry after 5 seconds
        return;
    }

    // Update sensors map
    const newSensorNames = new Set();

    for (const [name, sensorInfo] of Object.entries(sensorsData)) {
        newSensorNames.add(name);

        if (!state.sensors.has(name)) {
            // New sensor - fetch metadata
            const metadata = await fetchSensorMetadata(sensorInfo.id);

            if (metadata) {
                state.sensors.set(name, {
                    ...sensorInfo,
                    ...metadata
                });
                state.enabledSensors.add(name);
                state.sensorData.set(name, {
                    times: [],
                    values: [],
                    lastShape: 0
                });
            }
        } else {
            // Existing sensor - update ID in case it changed
            const existingSensor = state.sensors.get(name);
            existingSensor.id = sensorInfo.id;
        }
    }

    // Remove sensors that no longer exist
    for (const sensorName of state.sensors.keys()) {
        if (!newSensorNames.has(sensorName)) {
            state.sensors.delete(sensorName);
            state.sensorData.delete(sensorName);
            state.enabledSensors.delete(sensorName);
        }
    }

    // Generate colors for all sensors
    state.colors = generateColors(state.sensors.size);

    // Update UI
    renderSensorList();
}

// Fetch data for all sensors
async function updateSensorData() {
    const promises = Array.from(state.sensors.entries()).map(async ([name, sensor]) => {
        const currentData = state.sensorData.get(name);

        // Fetch updated metadata to get current shape
        const metadata = await fetchSensorMetadata(sensor.id);
        if (!metadata) return;

        const newShape = metadata.shape;

        // Update sensor metadata
        sensor.shape = newShape;

        // Check if there's new data
        if (newShape > currentData.lastShape) {
            // Fetch new data points
            const newValues = await fetchSensorDataRange(sensor.id, currentData.lastShape, newShape);

            if (newValues && newValues.length > 0) {
                // Calculate time values based on start_time and frequency
                const startTime = sensor.start_time || 0;
                const frequency = sensor.frequency || 1;
                const interval = 1.0 / frequency;

                // Generate time values for new data points
                for (let i = 0; i < newValues.length; i++) {
                    const index = currentData.lastShape + i;
                    const time = startTime + (index * interval);
                    currentData.times.push(time);
                    currentData.values.push(newValues[i]);
                }

                currentData.lastShape = newShape;
            }
        }
    });

    await Promise.all(promises);
    renderChart();
}

// Calculate min and max values for sensor based on scale_factor
function getSensorRange(sensor) {
    const scaleFactor = sensor.scale_factor || 1;
    return {
        min: 0,
        max: scaleFactor,
        units: ''
    };
}

// Display error message in sensor list
function displayError(message) {
    const sensorList = document.getElementById('sensorList');
    sensorList.innerHTML = `<p class="loading" style="color: #d32f2f;">${message}</p>`;
}

// Render sensor list in side panel
function renderSensorList() {
    const sensorList = document.getElementById('sensorList');
    sensorList.innerHTML = '';

    if (state.sensors.size === 0) {
        sensorList.innerHTML = '<p class="loading">No sensors available</p>';
        return;
    }

    const sensorArray = Array.from(state.sensors.entries());
    sensorArray.forEach(([name, sensor], index) => {
        const sensorItem = document.createElement('div');
        sensorItem.className = 'sensor-item';

        const color = state.colors[index];
        const isEnabled = state.enabledSensors.has(name);
        const range = getSensorRange(sensor);
        const dataCount = state.sensorData.get(name)?.values.length || 0;

        sensorItem.innerHTML = `
            <div class="sensor-header">
                <input type="checkbox"
                       class="sensor-checkbox"
                       id="sensor-${name}"
                       ${isEnabled ? 'checked' : ''}
                       data-sensor-name="${name}">
                <label class="sensor-name" for="sensor-${name}">${sensor.description || name}</label>
                <div class="sensor-color" style="background-color: ${color};"></div>
            </div>
            <div class="sensor-details">
                <div><strong>Name:</strong> ${name}</div>
                <div><strong>Range:</strong> ${range.min} - ${range.max} ${range.units}</div>
                <div><strong>Frequency:</strong> ${sensor.frequency || 'N/A'} Hz</div>
                <div><strong>Start:</strong> ${formatDateTime(sensor.start_time)}</div>
                <div><strong>Data Points:</strong> ${dataCount} / ${sensor.shape || 0}</div>
            </div>
        `;

        sensorList.appendChild(sensorItem);

        // Add event listener
        const checkbox = sensorItem.querySelector('.sensor-checkbox');
        checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
                state.enabledSensors.add(name);
            } else {
                state.enabledSensors.delete(name);
            }
            renderChart();
        });
    });
}

// Format datetime from epoch seconds
function formatDateTime(epochSeconds) {
    if (!epochSeconds) return 'N/A';
    const date = new Date(epochSeconds * 1000);
    return date.toLocaleString();
}

// Format time for axis labels
function formatTimeLabel(epochSeconds) {
    const date = new Date(epochSeconds * 1000);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    const ms = String(Math.floor(date.getMilliseconds())).padStart(3, '0');
    return `${hours}:${minutes}:${seconds}.${ms}`;
}

// Initialize canvas
function initializeCanvas() {
    state.canvas = document.getElementById('dataCanvas');
    state.ctx = state.canvas.getContext('2d');

    // Set canvas size to match display size
    function resizeCanvas() {
        const rect = state.canvas.getBoundingClientRect();
        state.canvas.width = rect.width;
        state.canvas.height = rect.height;

        // Update chart area
        state.chartArea.width = state.canvas.width - state.chartArea.x - 20;
        state.chartArea.height = state.canvas.height - state.chartArea.y - 50;

        renderChart();
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
}

// Render chart
function renderChart() {
    if (!state.ctx) return;

    const ctx = state.ctx;
    const canvas = state.canvas;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Get enabled sensors with data
    const enabledSensorsWithData = Array.from(state.enabledSensors)
        .filter(name => {
            const data = state.sensorData.get(name);
            return data && data.values.length > 0;
        });

    if (enabledSensorsWithData.length === 0) {
        // Draw empty state
        ctx.fillStyle = '#999';
        ctx.font = '16px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('No data to display', canvas.width / 2, canvas.height / 2);
        return;
    }

    // Calculate data ranges
    let minTime = Infinity;
    let maxTime = -Infinity;
    let minValue = Infinity;
    let maxValue = -Infinity;

    // First pass: find the maximum time across all enabled sensors
    enabledSensorsWithData.forEach(name => {
        const data = state.sensorData.get(name);
        if (data.times.length > 0) {
            const dataMaxTime = Math.max(...data.times);
            if (dataMaxTime > maxTime) maxTime = dataMaxTime;
        }
    });

    // Calculate time cutoff based on history window
    const timeCutoff = state.historyWindow > 0 ? maxTime - state.historyWindow : -Infinity;

    // Second pass: calculate time range for data within the history window
    enabledSensorsWithData.forEach(name => {
        const data = state.sensorData.get(name);

        if (data.times.length > 0) {
            // Filter data within the history window to find min time
            for (let i = 0; i < data.times.length; i++) {
                const time = data.times[i];
                if (time >= timeCutoff) {
                    if (time < minTime) minTime = time;
                }
            }
        }
    });

    // Calculate vertical scale from sensor attributes (min_value and max_value)
    if (enabledSensorsWithData.length > 0) {
        enabledSensorsWithData.forEach(name => {
            const sensor = state.sensors.get(name);
            if (sensor) {
                const sensorMinValue = sensor.min_value !== undefined ? sensor.min_value : 0;
                const sensorMaxValue = sensor.max_value !== undefined ? sensor.max_value : (sensor.scale_factor || 1);

                if (sensorMinValue < minValue) minValue = sensorMinValue;
                if (sensorMaxValue > maxValue) maxValue = sensorMaxValue;
            }
        });
    } else {
        // No enabled sensors, use default range
        minValue = -1;
        maxValue = 1;
    }

    // Add padding to value range
    const valueRange = maxValue - minValue;
    const valuePadding = valueRange * 0.1 || 1;
    minValue -= valuePadding;
    maxValue += valuePadding;

    // Draw axes
    const chartArea = state.chartArea;
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(chartArea.x, chartArea.y);
    ctx.lineTo(chartArea.x, chartArea.y + chartArea.height);
    ctx.lineTo(chartArea.x + chartArea.width, chartArea.y + chartArea.height);
    ctx.stroke();

    // Draw y-axis labels
    ctx.fillStyle = '#333';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';

    const ySteps = 5;
    for (let i = 0; i <= ySteps; i++) {
        const value = minValue + (maxValue - minValue) * (i / ySteps);
        const y = chartArea.y + chartArea.height - (i / ySteps) * chartArea.height;
        ctx.fillText(value.toFixed(3), chartArea.x - 5, y);

        // Draw grid line
        ctx.strokeStyle = '#e0e0e0';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(chartArea.x, y);
        ctx.lineTo(chartArea.x + chartArea.width, y);
        ctx.stroke();
    }

    // Draw x-axis labels
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';

    const xSteps = 6;
    const timeRange = maxTime - minTime;
    for (let i = 0; i <= xSteps; i++) {
        const time = minTime + (timeRange * i / xSteps);
        const x = chartArea.x + (i / xSteps) * chartArea.width;
        ctx.fillText(formatTimeLabel(time), x, chartArea.y + chartArea.height + 5);

        // Draw grid line
        ctx.strokeStyle = '#e0e0e0';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x, chartArea.y);
        ctx.lineTo(x, chartArea.y + chartArea.height);
        ctx.stroke();
    }

    // Draw data lines
    enabledSensorsWithData.forEach((name, index) => {
        const data = state.sensorData.get(name);
        const sensorIndex = Array.from(state.sensors.keys()).indexOf(name);
        const color = state.colors[sensorIndex];

        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.beginPath();

        let firstPoint = true;
        for (let i = 0; i < data.times.length; i++) {
            const time = data.times[i];
            const value = data.values[i];

            // Skip data points outside the history window
            if (time < timeCutoff) continue;

            const x = chartArea.x + ((time - minTime) / (maxTime - minTime)) * chartArea.width;
            const y = chartArea.y + chartArea.height - ((value - minValue) / (maxValue - minValue)) * chartArea.height;

            if (firstPoint) {
                ctx.moveTo(x, y);
                firstPoint = false;
            } else {
                ctx.lineTo(x, y);
            }
        }

        ctx.stroke();
    });
}

// Start polling
function startPolling() {
    stopPolling();
    state.pollTimer = setInterval(async () => {
        await initializeSensors(); // Check for new sensors
        await updateSensorData();
    }, state.pollInterval);
}

// Stop polling
function stopPolling() {
    if (state.pollTimer) {
        clearInterval(state.pollTimer);
        state.pollTimer = null;
    }
}

// Show login dialog
function showLoginDialog() {
    return new Promise((resolve, reject) => {
        const dialog = document.getElementById('loginDialog');
        const form = document.getElementById('loginForm');
        const cancelBtn = document.getElementById('cancelLogin');
        const errorDiv = document.getElementById('loginError');
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');

        // Clear previous values
        form.reset();
        errorDiv.style.display = 'none';

        // Show dialog
        dialog.style.display = 'flex';
        usernameInput.focus();

        // Handle form submission
        const handleSubmit = async (e) => {
            e.preventDefault();
            const username = usernameInput.value.trim();
            const password = passwordInput.value;

            if (!username || !password) {
                errorDiv.textContent = 'Please enter both username and password';
                errorDiv.style.display = 'block';
                return;
            }

            // Create auth header
            state.authHeader = createAuthHeader(username, password);

            // Try validating again
            const validationResult = await validateDomain();

            if (validationResult.success) {
                // Success - hide dialog and resolve
                dialog.style.display = 'none';
                cleanup();
                resolve(true);
            } else {
                // Failed - show error
                if (validationResult.requiresAuth) {
                    errorDiv.textContent = 'Invalid username or password';
                } else {
                    errorDiv.textContent = validationResult.message;
                }
                errorDiv.style.display = 'block';
                state.authHeader = null; // Clear invalid auth
            }
        };

        // Handle cancel
        const handleCancel = () => {
            dialog.style.display = 'none';
            cleanup();
            reject(new Error('Login cancelled'));
        };

        // Cleanup function
        const cleanup = () => {
            form.removeEventListener('submit', handleSubmit);
            cancelBtn.removeEventListener('click', handleCancel);
        };

        form.addEventListener('submit', handleSubmit);
        cancelBtn.addEventListener('click', handleCancel);
    });
}

// Initialize application
async function init() {
    initializeCanvas();

    // Validate domain before proceeding
    let validationResult = await validateDomain();
    if (!validationResult.success) {
        if (validationResult.requiresAuth) {
            // Show login dialog
            try {
                await showLoginDialog();
                // Login successful, continue with initialization
            } catch (error) {
                // Login cancelled
                displayError('Login cancelled');
                return;
            }
        } else {
            // Other error
            displayError(validationResult.message);
            return;
        }
    }

    // Set up controls
    const pollIntervalInput = document.getElementById('pollInterval');
    pollIntervalInput.addEventListener('change', (e) => {
        state.pollInterval = parseInt(e.target.value) || DEFAULT_POLL_INTERVAL;
        startPolling();
    });

    const refreshBtn = document.getElementById('refreshBtn');
    refreshBtn.addEventListener('click', async () => {
        await initializeSensors();
        await updateSensorData();
    });

    const pauseCheckbox = document.getElementById('pauseCheckbox');
    pauseCheckbox.addEventListener('change', (e) => {
        if (e.target.checked) {
            stopPolling();
        } else {
            startPolling();
        }
    });

    const historyWindowInput = document.getElementById('historyWindow');
    historyWindowInput.addEventListener('change', (e) => {
        state.historyWindow = parseInt(e.target.value) || 0;
        renderChart();
    });

    // Initial load
    await initializeSensors();
    await updateSensorData();

    // Start polling
    startPolling();
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
