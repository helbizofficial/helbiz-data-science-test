'use strict';

require('dotenv').config()

const AWS = require('aws-sdk');
const h3 = require('h3-js');

const dynamoDb = new AWS.DynamoDB.DocumentClient(
	{
		region: process.env.DYNAMODB_REGION,
		endpoint: process.env.DYNAMODB_ENDPOINT_URL
	}
);

const request = require('request')

// Transform takes the data points gathered in
// `rawbikes` and applies a simple aggregation.
// The raw lat / long values are mapped to
// hex-index values. The tallies are gathered for
// each
//
// Each index with a corresponding tally for the
// day is committed to `hotspots`
module.exports.transform = (event, context, callback) => {
	var params = {
		TableName: "rawbikes"
	}

	var bulkWriteItems = []

	// grab every rawbike entry with the explicit
	// latitude and longitude values - map it to
	// a hexidecimal value and accumulate to see
	// our hotspots
	dynamoDb.scan(params, function(err, data) {
		data.Items.forEach(function(bike) {
			const lat = bike["lat"]
			const lon = bike["lon"]

			// tally every bike that falls within the
			// given hex index
			index = h3.geoToH3(lat, lon, 75)
			bulkWriteItems[index] = bulkWriteItems[index] + 1 || 1
		})

	})

	writeParams = []

	// with our raw points grouped by hexagon, we
	// can commit the rollup values to our database
	// when we want to rank them, simply order by
	// tally
	bulkWriteItems.forEach(function(entry) {
		const [key, value] = entry;

		// [lat, lon]
		const center = h3.h3ToGeo(key)
		writeParams.push({
			PutRequest: {
				Item: {
					id: key,
					lat: center[0],
					lon: center[1],
					tally: value,
					created_at: Date.now()
				}
			}
		})

		if (writeParams.length == 25) {
			// as described by
			// https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/DynamoDB.html#batchWriteItem-property
			const params = {
				RequestItems: {
					"hotspots": bulkWriteItems
				}
			}

			console.log(`writing ${writeParams.length} records`)
			dynamoDb.batchWrite(params, function(err, data) {
		if (err) console.log(err, err.stack)
			})

			writeParams = []
		}
	})

	// clean up any remaining records in write params
	const params = {
		RequestItems: {
			"hotspots": bulkWriteItems
		}
	}

	dynamoDb.batchWrite(params, function(err, data) {
			if (err) console.log(err, err.stack)
	})

	// clear all records from raw table - we've already
	// processed them
	bulkWriteItems.forEach(item => {
		var params = {
			TableName: "rawbikes",
			Key: {
				bike_id: item["bike_id"]
			}
		}

		dynamoDb.delete(params, function(err, data) {
			if(err) {
				console.log(err)
			}
		}
	})
}
