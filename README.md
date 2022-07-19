# Candlestick Image Generator

This is simple AWS lambda made to generate and upload candlestick 
graph images to s3 bucket. Feel free to use, copy, and improve this code. 
The intention is to use this as part of a bigger project: Telegram-Stock-Bot 
which is currently under development. 



## Deployment

To deploy this project on your AWS environment make sure that you created s3 bucket,
AWS lambda, and assigned correct IAM roles to them.

Lambda requirements:
* environment varables: `BUCKET_NAME`
* Runtime: `Python3.9`
* Architecture: `x86_64`
* Memory: `256Mb`

Also, the project needs to be uploaded via s3 bucket due to size of the 
final zip exceeds 50Mb.

### Building project

```bash
python3 -m pip install --only-binary :all: --platform manylinux1_x86_64  --target ./my-package -r requirements.txt
cd my-package  
zip -r ../my-deployment-package.zip .
cd ..
zip -g my-deployment-package.zip lambda_function.py
```

After you builb project once and you don't change any libraries you can simply update
zip with he following command.

```bash
zip -g my-deployment-package.zip lambda_function.py
```