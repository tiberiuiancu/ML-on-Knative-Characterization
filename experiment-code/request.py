import logging
import time
import os
import base64
import random
import requests
import json
import numpy as np
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import boto3
from botocore.client import Config

# maximum time to wait between requests
MAX_WAIT_SEC = 3 * 60

# minimum time in-between requests to consider them part of different bursts
MIN_WAIT_SEC = 60

# run each experiment twice
N_RUNS = 3

# setup logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

# service names that we will make inference calls to
services = []

# get a random permutation of services, and run them N_RUNS times
services = N_RUNS * services
random.shuffle(services)

# load images to send for inference
to64 = lambda x: base64.b64encode(open(x, "rb").read()).decode()
imgs = [to64(os.path.join("images", img)) for img in os.listdir("images")]

# create s3 client
client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    config=Config(signature_version='s3v4'),
    region_name='nl-ams',
    verify=False
)


def s3_upload(buf: str, service: str, run: int):
    client.put_object(Bucket="test", Key=f"thesis/experiments/latency/{service}_{str(run)}.csv", Body=buf)
    logging.info("flushed dataframe")


def make_request(service):
    # get random image to send for inference
    img = random.choice(imgs)

    # create endpoint url from service name
    endpoint = f"http://{service}:80/predict"

    # record start time
    start = time.time()

    # send request and check if status code is 200
    if requests.post(endpoint, data=json.dumps(img)).status_code != 200:
        return None, service
    else:
        # append record to dataframe
        req_duration = time.time() - start
        return req_duration, service


def parse_dates(fn):
    # parse list of dates
    dates = pd.read_csv(fn, header=0).timestamp
    dates = pd.to_datetime(dates, format="mixed", utc=False)

    # some magic to shift dates to start now
    deltas = dates.diff()
    max_wait = np.timedelta64(MAX_WAIT_SEC, "s")
    min_wait = np.timedelta64(MIN_WAIT_SEC, "s")

    # if deltas > max_wait, make them max_weight
    series_max_wait = pd.Series([max_wait] * len(dates))
    deltas = (deltas < max_wait) * deltas + (deltas >= max_wait) * series_max_wait

    # if deltas < min_wait, make it 0
    # in other words, if deltas > min_wait, leave it as is
    deltas = deltas * (deltas > min_wait)

    deltas = deltas.cumsum()
    dates = (deltas + pd.Timestamp.now()).iloc[1:]

    return list(dates.sort_values())


if __name__ == "__main__":

    # create thread pool to execute requests
    pool = ThreadPoolExecutor(max_workers=20)

    # get experiment length
    times = parse_dates("dates.csv")
    end_time = pd.Timestamp.now() + pd.Timedelta(
        seconds=len(services) * ((times[-1] - times[0]).total_seconds() + MAX_WAIT_SEC)
    )
    logging.info(f"All experiments will finish around {end_time}")

    for i, service in enumerate(services):
        logging.info(f"--------------------- EXPERIMENT {i+1}/{len(services)} ({service}) ---------------------")
        logging.info(f"sleeping for {MAX_WAIT_SEC//60} minutes")
        time.sleep(MAX_WAIT_SEC)

        # parse times to send requests
        times = parse_dates("dates.csv")

        buff = ""
        futures = []
        for t in times:
            # get the current time
            now = pd.Timestamp.now()

            # calculate the number of seconds until the next closest time
            delta_t = t - now

            # convert pandas timestamp to seconds
            delta_t = delta_t.total_seconds()

            # sleep until the next request only if the wait time is supposed ot be greater than 1 min
            if delta_t > 60:
                logging.info(f"next request will be sent at {t}")
                time.sleep(delta_t)

            logging.info(f"sending request to {service}")
            futures.append(pool.submit(make_request, service))

        # collect whatever is left of the requests
        run_number = services[:i].count(service)
        for f in futures:
            try:
                duration, service = f.result(timeout=300)
                if duration is not None:
                    buff += f"{int(time.time())},{run_number},{duration},{service}\n"
            except:
                pass

        # flush df
        s3_upload(buff, service, run_number)

        logging.info("---------------- EXPERIMENT FINISHED ----------------")

    exit(0)
