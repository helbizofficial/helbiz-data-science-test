# Hotbiz
#### A Serverless Pipeline for GBFS Data

## Overview
Hotbiz leans extensively on the 
[Serverless Framework](https://www.serverless.com/) for
developing and running a suite of event-driven lambdas.

This framework provides the abstractions and tooling
needed to rapidly design and deploy this project as a
suite of highly-independent and scalable tasks.

It's native development environment, and a rich suite
of plugins make it easy to configure and deploy new
code locally, and in the cloud.

## Lambdas
### Clock - Python Runtime
Clock is scheduled to run once every minute. The 
offline-schedule plugin needed to be coaxed into 
accepting `rate` as an array (you can see that the
package.json file references a forked repo with the
fix in-place).

Clock reads configuration records from our DynamoDB:
basically the URLs for every endpoint we need to read,
and the last time we accessed the URL.

If the current system time is more recent (minus the
configured TTY), then we issue an SNS notification to
trigger another Lambda task (Scraper), which downloads
and processes the raw JSON.

### Scraper - Node.js
Scraper is a generic JSON-parsing Lambda, triggered by 
an SNS notification. Rather than create separate
Lambdas for each endpoint (or a single monolith
responsible for every provider), this Lambda will
accept the URL as a message parameter. Meaning, we can
invoke arbitrarily many Lambdas for as many endpoints
as we need to configure. Much more scalable.

In the course of running Offline-SNS, I couldn't
trigger any Python runtimes using local SNS. For some
reason, Node.js runtimes work without any issue.

It would have been awesome to use Python here, and
leverage the amazing data science libraries (Pandas,
SciKitlearn, etc), but for the sake of running local
SNS, Node was selected out of necessity.

### Transform - Node.js
Transform would be a great candidate for DynamoDB
Stream events. For now, it's triggered once a day.
It aggregates the raw data points gathered throughout
the day, grouping them by hex-id, and committing them
back to DynamoDB

### Hotspot - Python
Our only http-event Lambda. `GET /hotspot` will return
the 10 most trafficked zones in our data set for the
given day

## DynamoDB
DynamoDB provided the flexibility needed to rapidly
develop and iterate on a design. By virtue of being
document based, schema changes were quick to implement.

Being an AWS product, integrating with the Serverless
Framework, and the Offline plugin, took minimal
configuration. A working, in-memory database took
minutes to set-up and run.

![AWS Infrastructure](https://i.imgur.com/3QGcLNB.png)

## Deploying to AWS
The Serverless Framework borrows heavily from
CloudFormation, reducing friction during deployments
to an AWS-based production environment. A live version
of this project would continue to lean on SNS event
triggers, allowing more granular fan-out (more Lambdas
with focused functions, and specific triggers). A
production setup could consider DynamoDB Streams as
event triggers. In place of periodic functions fired
by cron events, specialized functions could be designed
to fire when new records are added or updated to our
database.


## Install Serverless Framework
This project depends heavily on the Serverless
Framework, and related plugins, to provision resources
and process events

(see Plugins section of serverless.yml for complete
list of dependencies - eg: serverless-offline)
```
$ npm install -g serverless
```

## Serverless Offline
The Serverless Offline plugin allows us to simulate
the API gateway, and SNS services, allowing us to 
invoke additional lambdas programatically, instead of
manually. This makes it easier to see how our
Lambdas can fan-out, creating and responding to events
automatically

![serverless-offline](https://i.imgur.com/OFd9J3Q.png)

## Install DynamoDB
This dependency may be improved by further-leveraging
containers. It should be possible to manage a local
instance of DynamoDB through a Docker Image. For now,
we rely on the basic installation, which requires JRE
```
$ sls dynamodb install
```

## Hotspots
We make several assumptions to calculate our hotspots:
Given consistent sampling across our APIs, we do not
need to scale resutls coming from any single provider.
For example, if UBER updated their data twice as 
often as Bird, we would need to account for additional
samples coming from UBER, and avoid skewing our results
simply based on the volume of data from any given 
provider.

Based on this assumption, we tally the number of
vehicles in any zone throughout the day. The ten most
trafficked zones are flagged as our hotspots.
