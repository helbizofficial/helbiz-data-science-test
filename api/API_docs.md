# Washington DC Bike Hot Spots

## Usage

All responses will have the form

```json
{
    "message": "Description of what happened",
    "last_updated": "Last updated date",
    "data": "Mixed type holding the content of the response"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List all hot spots

**Definition**

`GET /api/v1/hotspots`


**Parameters**

- `"geofence":string` Name of the state (washington)
- `"date":string` Date of the data

**Basic HTTP Authentication**

- `username: admin`
- `password: PasswordForHotSpots`

**Response**

- `200 OK` on success
- `401 Unauthorized` if request is not authorized
- `404 Not Found` if there is no data in corresponding date
- `400 Bad Requeset` if parameters are in the incorrect form

```json
[
    {
        "latitude": 38.86238778760666,
        "longitude": -76.99530218265403,
        "avg_vehicle_count": 24.5
    },
    {
        "latitude": 38.93738893236049,
        "longitude": -77.0246298693365,
        "avg_vehicle_count": 12.7
    }
]
```
