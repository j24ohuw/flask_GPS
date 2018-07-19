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
- Description: you need to pass all relevant information

    ```

