# Data Collection Tree

# Introduction
The Project is made using the following packages:
- [Flask](https://flask.palletsprojects.com/)
- [Flask-Testing](https://pythonhosted.org/Flask-Testing/)
- [Marshmallow](https://marshmallow.readthedocs.io/)

The setup also include [gunicorn](https://gunicorn.org/) which is an WSGI server used to serve the app.

## API Docs

### 1. `/v1/insert`
This will insert a node to the tree

Payload:
```json
{
   "dim":[
      {
         "key":"country",
         "val":"US"
      }
   ],
   "metrics":[
      {
         "key":"webreq",
         "val":220
      },
      {
         "key":"timespent",
         "val":180
      }
   ]
}
```
RES: 200 OK


### 2. `/v1/query`
This is used to query an existing node in the tree

Payload:
```json
{
   "dim":[
      {
         "key":"country",
         "val":"US"
      }
   ]
}
```

Output:
```json
{
   "dim":[
      {
         "key":"country",
         "val":"US"
      }
   ],
   "metrics":[
      {
         "key":"webreq",
         "val":220
      },
      {
         "key":"timespent",
         "val":180
      }
   ]
}
```


## Running the program
The server can be started using the following command:
```
docker-compose up --build
```