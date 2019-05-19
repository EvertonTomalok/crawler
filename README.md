# crawler
This is a crawler to retrive information from http://www.adorocinema.com.br

A example is able to use in this file `todas_criticas_2019_05_19.json`


# USAGE:
  You'll need python > 3.6 installed in your machine, and pip, files manager of python.
  - First install pipenv:
    - pip install pipenv
  - Inside the folder:
    - pipenv install && pipenv shell
    
## Saving in a .json file:
  It'll generate a json file with all data collected.
   - scrapy crawl todas_criticas -o NAME_AS_YOU_WISH.json  

## Save in mongodb database:
  The information retrieved will be saved in MongoDB. To use this feature, you need to have installed in your machin, the mongoDB. See how to install here: https://docs.mongodb.com/v3.2/administration/install-community/
  To use this feature:
  - scrapy crawl todas_criticas -a save
  
  The data collected will be save in a database called `tcc`, in a collection named `filmes`
