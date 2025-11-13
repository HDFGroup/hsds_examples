# Live Sensor Data Viewer

A web application that displays live streaming data from an HDF5 REST API (HSDS) service providing sensor data.

## Features

- **Real-time Data Visualization**: Displays live streaming sensor data on a canvas
- **Dynamic Sensor Management**: Automatically detects when sensors are added or removed
- **Interactive Controls**: Toggle individual sensors on/off using checkboxes
- **Time-based X-axis**: Displays datetime labels converted from epoch seconds
- **Responsive Design**: Adapts to different screen sizes
- **Configurable Polling**: Adjust how frequently the app checks for new data
- **Incremental Data Loading**: Only fetches new data points, not the entire dataset

## Application Structure

```
.
├── index.html     # Main HTML structure
├── styles.css     # Styling and layout
└── app.js         # Application logic
```

## HSDS API Structure

The application expects an HDF5 REST API (HSDS) service with the following structure:

### Domain Structure
- HDF5 domain contains a `/sensors` group
- Each sensor is a dataset under `/sensors` (e.g., `/sensors/xyz`, `/sensors/abc`)
- Sensor datasets contain 1D array of float values

### API Endpoints Used

#### 1. Get Sensors List
```
GET /groups/?h5path=/sensors&include_links=1
Headers: X-Hdf-domain: /path/to/domain.h5
```

Returns links to all sensor datasets.

#### 2. Get Sensor Metadata
```
GET /datasets/{dataset_id}?include_attrs=1
Headers: X-Hdf-domain: /path/to/domain.h5
```

Returns dataset shape and attributes:
- `shape.dims[0]`: Number of data points in the dataset
- `attributes`:
  - `description`: Sensor description (string)
  - `start_time`: Start time in epoch seconds (float)
  - `frequency`: Sampling frequency in Hz (int)
  - `scale_factor`: Value scale factor (int)
  - `update_interval`: How often data is added (int)

#### 3. Get Sensor Data
```
GET /datasets/{dataset_id}/value?select=[start:stop]
Headers: X-Hdf-domain: /path/to/domain.h5
```

Returns data values in the specified range.

## Setup and Usage

1. **Update Configuration**: Edit `app.js` lines 2-3 and change the configuration constants:
   ```javascript
   const HSDS_ENDPOINT = 'http://localhost:5101';
   const HDF_DOMAIN = '/home/john/streamtest.h5';
   ```

2. **Open in Browser**: Simply open `index.html` in a web browser. No build process required!

3. **Configure Polling**: Use the "Poll Interval" input to adjust how often the app checks for new data (in milliseconds).

## How It Works

1. **Initial Load**:
   - Fetches all sensor names from `/sensors` group
   - For each sensor, fetches metadata including attributes and current shape

2. **Sensor Display**:
   - Each sensor appears in the side panel with its metadata
   - Shows current data point count and total shape

3. **Data Polling**:
   - Periodically checks each sensor's shape to detect new data
   - Only fetches new data points (from lastShape to newShape)
   - Calculates time values based on start_time and frequency

4. **Visualization**:
   - X-axis starts at the earliest sensor start_time
   - Each enabled sensor gets a unique color
   - Grid lines and labels make the chart easy to read
   - Time labels show HH:MM:SS.ms format

5. **Interaction**:
   - Uncheck a sensor's checkbox to hide its plot line
   - Click "Refresh Now" to manually update data

## Time Calculation

Since the HSDS API doesn't provide explicit time values, the app calculates them:
```
time[i] = start_time + (i / frequency)
```

Where:
- `start_time` is from the sensor's attribute
- `i` is the data point index
- `frequency` is the sampling rate in Hz

## Browser Compatibility

Works in all modern browsers that support:
- Canvas API
- Fetch API
- ES6+ JavaScript

## CORS Considerations

If your HSDS service is on a different domain, ensure it has appropriate CORS headers:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET
Access-Control-Allow-Headers: X-Hdf-domain
```

## Example Python Notebook

See `sensor_query.ipynb` for examples of how to query the HSDS API using Python.
