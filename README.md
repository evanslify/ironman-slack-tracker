docker run -it -v ~/Projects/ironman-slack-spam:/home/dev/code -v ~/.aws:/home/dev/.aws -v ~/.gitconfig:/home/dev/.gitconfig simple.lambdadocker build -t simple.lambda .
docker build -t simple.lambda .
aws lambda update-function-code --function-name ironman-tracker --zip-file fileb://deployment-package.zip
aws lambda invoke --function-name ironman-tracker --payload '{"post_slack": true}' -
