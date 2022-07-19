import os
import boto3
import matplotlib.pyplot as plt
import pandas as pd
import json

from botocore.exceptions import NoCredentialsError

def lambda_handler(event, context):
    
    imageName = generate_graph(event)

    upload_to_aws('/tmp/' + imageName, imageName)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Upload successful')
    }


def upload_to_aws(local_file, s3_file):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(Filename=local_file, Bucket=os.environ['BUCKET_NAME'], Key=s3_file)
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None

def generate_graph(data):
    open = []
    close = []
    high = []
    low = []
    timeIndex = []

    for dataFrame in data['results']:
        open.append(dataFrame['o'])
        close.append(dataFrame['c'])
        high.append(dataFrame['h'])
        low.append(dataFrame['l'])
        timeIndex.append(
            int(dataFrame['t'])/1000)

    prices = pd.DataFrame({'open': open,
                        'close': close,
                        'high': high,
                        'low': low},
                        index=timeIndex)

    # create figure
    fig, ax = plt.subplots()
    plt.grid(color='#434547')
    titleObj = plt.title(data['ticker'])
    plt.setp(titleObj, color='#b4bec4')
    ax.spines['right'].set_color('#b4bec4')
    ax.spines['left'].set_color('#b4bec4')
    ax.spines['bottom'].set_color('#b4bec4')
    ax.spines['top'].set_color('#b4bec4')
    ax.tick_params(colors='#b4bec4')
    ax.set_facecolor('#2f3133')
    fig.patch.set_facecolor('#2f3133')
    fig.set_size_inches(9, 4)


    # define width of candlestick elements
    width = 1000
    width2 = 100

    # define up and down prices
    up = prices[prices.close >= prices.open]
    down = prices[prices.close < prices.open]

    # define colors to use
    greenBarColor = "#62cea5"
    redBarColor = "#fa7671"

    # plot up prices
    plt.bar(up.index, up.close-up.open, width, bottom=up.open, color=greenBarColor)
    plt.bar(up.index, up.high-up.close, width2,
            bottom=up.close, color=greenBarColor)
    plt.bar(up.index, up.low-up.open, width2, bottom=up.open, color=greenBarColor)

    # plot down prices
    plt.bar(down.index, down.close-down.open, width,
            bottom=down.open, color=redBarColor)
    plt.bar(down.index, down.high-down.open, width2,
            bottom=down.open, color=redBarColor)
    plt.bar(down.index, down.low-down.close, width2,
            bottom=down.close, color=redBarColor)

    imageName = data['ticker']+'.png'

    fig.savefig('/tmp/' + imageName, dpi=150)

    return imageName