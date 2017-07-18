# stash-bitbucket-mirror-all
Mirror all available repos from a stash/bitbucket server to another git server

## To run:
```
docker run -it --rm --name stash-bitbucket-mirror-all -e STASH_URL=http://www.example.com -e STASH_USER=myusername -e STASH_PWD=mypwd -e STASH_URL_PART_TO_CHANGE=www.example.com -e STASH_URL_PART_TO_REPLACE_WITH  ddumenil/stash-bitbucket-mirror-all
```

## To build:
```
docker build -t stash-bitbucket-mirror-all .
```

Hat tip to the original script creator Jason LeMonier who chipped in on this Stack Overflow question:

https://stackoverflow.com/questions/36090075/how-to-extract-the-list-of-all-repositories-in-stash-or-bitbucket

