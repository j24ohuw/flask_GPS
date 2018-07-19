# Flask Location REST API
- API tools and documentation


## REST URLs

#### GET /products/  
- Description: returns JSON response containing all products currently in the database
- Response: 
    ```JSON
    {
    "result": {
        "data": [
            {
                "description": "iphone4",
                "id": 85,
                "locations": [
                    {
                        "datetime": "Wed, 12 Oct 2016 13:00:00 GMT",
                        "elevation": 100,
                        "id": 71,
                        "latitude": 47.9,
                        "longitude": 43.2
                    }
                ]
            },
            {
                "description": "iphone2",
                "id": 84,
                "locations": [
                    {
                        "datetime": "Fri, 14 Oct 2016 13:00:00 GMT",
                        "elevation": 500,
                        "id": 66,
                        "latitude": -130,
                        "longitude": 140
                    },
                    {
                        "datetime": "Fri, 14 Oct 2016 13:00:00 GMT",
                        "elevation": 500,
                        "id": 67,
                        "latitude": -130,
                        "longitude": 140
                    },
    ```
    
#### POST /products/ 
- Description: view for adding a product. You need to pass all relevant information e.i) description, longitude, latitude, time(in ISO8601 format)
- Response: 
    ```JSON

    {
        "message": "",
        "result": {
            "data": {
                "datetime": "2016-10-12T13:00:00+00:00",
                "elevation": 100,
                "id": 72,
                "latitude": 47.9,
                "longitude": 43.2,
                "product": {
                    "description": "iphone4",
                    "product_id": 86
                }
            },
            "errors": {}
        }
    }
    ```

#### GET,PUT /products/<int:pk>
- Description: view for retrieving or editing a product description.
- Response: 
    ```JSON
    {
        "result": {
            "data": {
                "description": "iphone2",
                "id": 84,
                "locations": [
                    {
                        "datetime": "Fri, 14 Oct 2016 13:00:00 GMT",
                        "elevation": 500,
                        "id": 66,
                        "latitude": -130,
                        "longitude": 140
                    },    
    ```   
#### POST /products/<int:pk>
- Description: view for adding a new location to an existing product. You need to pass in elevation, latitude, longitude, and datetime.
- Response: 
    ```JSON

    {
    "message": "new location added to a product",
    "result": {
        "data": {
            "datetime": "2016-10-12T13:00:00+00:00",
            "elevation": -500,
            "id": 74,
            "latitude": -33,
            "longitude": 49,
            "product": {
                "description": "iphone4",
                "product_id": 86
                }
            },
            "errors": {}
        }
    }
    ```    
#### PUT, DELETE /locations/<int:pk>
- Description: view for editing/deleting a location from its parent product. 
- Response: 
    ```JSON
    {
    "message": "location edited",
    "result": {
        "data": {
            "datetime": "2016-10-19T12:00:00+00:00",
            "elevation": 504.5,
            "id": 74,
            "latitude": 140,
            "longitude": -180,
            "product": {
                "description": "iphone4",
                "product_id": 86
            }
        },
        "errors": {}
        }
    }
    
    ```   
