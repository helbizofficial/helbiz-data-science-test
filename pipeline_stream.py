import logging
import argparse
import apache_beam as beam
from os import getenv
from apache_beam.options.pipeline_options import PipelineOptions


PROJECT = getenv('PROJECT_ID')
schema = 'latitude:FLOAT, longitude:FLOAT, cnt_vehicles:FLOAT, date:STRING'
TOPIC_NAME = getenv('TOPIC')
TOPIC = f"projects/{PROJECT}/topics/{TOPIC_NAME}"


def clean_data(data):
    dct = eval(data)
    # vals --> [latitude, longitude, count of vehicles, date]
    vals = dct.values()
    # res --> "latitude,longitude,count of vehicles,date"
    res = ','.join(vals)
    return res


class Split(beam.DoFn):
    def process(self, element):
        element = element.split(",")

        return [{
            'latitude': float(element[0]),
            'longitude': float(element[1]),
            'cnt_vehicles': float(element[2]),
            'date': element[3]
        }]


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_topic")
    parser.add_argument("--output")
    # Parse known arguments into an object.
    known_args = parser.parse_known_args(argv)

    p = beam.Pipeline(options=PipelineOptions())

    (p
     | 'ReadData' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes)
     | "Decode" >> beam.Map(lambda x: x.decode('utf-8'))
     | "Clean Data" >> beam.Map(clean_data)
     | 'ParseCSV' >> beam.ParDo(Split())
     | 'WriteToBigQuery' >> beam.io.WriteToBigQuery('{0}:gbfs_feeds.hotspots'.format(PROJECT), schema=schema,
                                                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
     )
    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logger = logging.getLogger().setLevel(logging.INFO)
    main()
