'use strict';

require('dotenv').config()

const request = require('request')

const AWS = require('aws-sdk');

const dynamoDb = new AWS.DynamoDB.DocumentClient(
	{
		region: process.env.DYNAMODB_REGION,
		endpoint: process.env.DYNAMODB_ENDPOINT_URL
	}
);

module.exports.scrape = (event, context, callback) => {
	var url = event.Records[0].Sns.Message

	request({
		url: url,
		json: true
	}, function(error, response, body) {

		if (!error && response.statusCode === 200) {
			var bikes = body["data"]["bikes"]

			var bulkWriteItems = []

			for(var i = 0, size = bikes.length; i < size; i++) {
			const bike = bikes[i]

			bulkWriteItems.push({
				PutRequest: {
					Item: {
						"bike_id": {
							S: bike["bike_id"]
						},
						"lat": {
							S: bike["lat"]
						},
						"lon": {
							S: bike["lon"]
						}
					}
				}
			})

			// bulkWriteItems can support up to
				// 25 put requests, so we run in a loop
			if (bulkWriteItems.length == 25) {
				const params = {
					RequestItems: {
						"rawbikes": bulkWriteItems
					}
				}

				console.log(`writing ${bulkWriteItems.length} records`)
				dynamoDb.batchWrite(params, function(err, data) {
			if (err) console.log(err, err.stack)
							else console.log(data)
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
							else console.log(data)
				})
		}
	}
})
}
