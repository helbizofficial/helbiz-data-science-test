'use strict';

require('dotenv').config()

const AWS = require('aws-sdk');

const dynamoDb = new AWS.DynamoDB.DocumentClient(
	{
		region: process.env.DYNAMODB_REGION,
		endpoint: process.env.DYNAMODB_ENDPOINT_URL
	}
);

const request = require('request')

// Scrape takes the given URL and grabs the
// JSON object, parsing the individual
// records, and comitting them to DynamoDB
// for further processing
module.exports.scrape = (event, context, callback) => {
	// The clock function will notify us
	// which URL we should be scraping
	var url = event.Records[0].Sns.Message

	request({
		url: url,
		json: true
	}, function(error, response, body) {

		if (!error && response.statusCode === 200) {
			var bikes = body["data"]["bikes"]

			// We're going to prepare a bulk-write
			// to make better use of each call
			var bulkWriteItems = []

			// prepare each record. Once we reach 25 records
			// we commit those to the database, flush our
			// queue, and continue until we've read every
			// result.
			for(var i = 0, size = bikes.length; i < size; i++) {
			const bike = bikes[i]

			bulkWriteItems.push({
				PutRequest: {
					Item: {
						bike_id: bike["bike_id"],
						lat: bike["lat"],
						lon: bike["lon"]
					}
				}
			})

			// bulkWriteItems can support up to
				// 25 put requests, so we run in a loop
			if (bulkWriteItems.length == 25) {
				// as described by
				// https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/DynamoDB.html#batchWriteItem-property
				const params = {
					RequestItems: {
						"rawbikes": bulkWriteItems
					}
				}

				console.log(`writing ${bulkWriteItems.length} records`)
				dynamoDb.batchWrite(params, function(err, data) {
			if (err) console.log(err, err.stack)
				})

				bulkWriteItems = []
			}
	}

			// If there's anything left in the
			// queue, send it back to the database
			if (bulkWriteItems.length > 0) {
				const params = {
					RequestItems: {
						"rawbikes": bulkWriteItems
					}
				}

				console.log(`writing ${bulkWriteItems.length} records`)
				dynamoDb.batchWrite(params, function(err, data) {
					if (err) console.log(err, err.stack)
				})
		}
	}
})

	// lastly, update the timestamp on our config
	// so that we don't re-read the same API results
	// before their TTL has elapsed
	const current_timestamp = Date.now()
	const params = {
		TableName: "gbfs_config",
		Key: {
			"url": url,
		},
		UpdateExpression: "set last_seen = :x",
		ExpressionAttributeValues: {
			":x": current_timestamp
		}
	}

	console.log(url)
	console.log(`last seen: ${current_timestamp}`)
	dynamoDb.update(params, function(err, data) {
		if (err) console.log(err)
	})
}
