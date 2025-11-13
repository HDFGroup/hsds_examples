# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a pure client-side web application that displays live streaming sensor data from an HDF5 REST API (HSDS) service. There is no build process, bundler, or backend server - just open `index.html` in a browser.

## Running the Application

1. Update configuration in `app.js` lines 2-3:
   ```javascript
   const HSDS_ENDPOINT = 'http://localhost:5101';
   const HDF_DOMAIN = '/home/john/streamtest.h5';
   ```

2. Open `index.html` directly in a web browser

## Architecture

### Data Flow
1. **Initialization**: `fetchSensors()` queries `/groups/?h5path=/sensors` to discover all sensor datasets
2. **Metadata Loading**: For each sensor, `fetchSensorMetadata()` retrieves shape (data point count) and attributes (description, start_time, frequency, scale_factor)
3. **Incremental Data Fetching**: `updateSensorData()` polls each sensor's shape and only fetches new data points using `fetchSensorDataRange(id, start, stop)`
4. **Time Calculation**: Since HSDS doesn't provide time values, they're calculated as: `time[i] = start_time + (i / frequency)`

### State Management
All application state lives in the `state` object (app.js:7-17):
- `sensors`: Map of sensor_name -> sensor object (includes id, metadata, current shape)
- `sensorData`: Map of sensor_name -> {times: [], values: [], lastShape: 0}
- `enabledSensors`: Set of sensor names that are currently visible on the chart
- `pollTimer`: Interval timer for automatic updates

### HSDS API Integration
All API calls require the `X-Hdf-domain` header. The application expects:
- `/sensors` group containing datasets
- Dataset attributes: `description`, `start_time`, `frequency`, `scale_factor`, `update_interval`
- 1D float arrays for sensor values

### Rendering
Canvas-based plotting (no charting library):
- `renderChart()` handles all canvas drawing
- X-axis: time range from earliest sensor start_time to latest data point
- Y-axis: auto-scales based on all enabled sensor values
- Each sensor gets a unique HSL color based on its index

## Key Implementation Details

### Incremental Data Loading
The app tracks `lastShape` for each sensor and only fetches data from `[lastShape:newShape]` when the dataset grows. This avoids re-fetching the entire dataset on each poll.

### Dynamic Sensor Detection
`initializeSensors()` runs on each poll cycle to detect new sensors being added or removed from the `/sensors` group.

### Pause Functionality
The pause checkbox (index.html:19-22) stops/resumes the polling timer but manual refresh still works.

## Configuration Points
- `HSDS_ENDPOINT`: Server URL (app.js:2)
- `HDF_DOMAIN`: HDF5 domain path (app.js:3)
- `DEFAULT_POLL_INTERVAL`: Milliseconds between updates (app.js:4)
- `chartArea`: Canvas margins for axes (app.js:16)

## Example Usage
See `sensor_query.ipynb` for Python examples of querying the HSDS API and understanding the expected data structure.
