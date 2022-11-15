### Notes

**Technical challenges in implementing streaming vs batch data**
- Batch data needs enough compute and memory to handle the volume or transformations (e.g. complex joins), which might involve adding a cluster if the data is too large for one machine.  Streaming data can look at short windows or single records, but may also require a cluster if the velocity of the streaming records is too much for one machine.  
- Some things are also more complicated to resolve for streaming data than for batch data, like handling sessions, performing joins, ensuring processing order in parallel streams, and handling events that arrive late or out of order.

**Cloud-native services considered**
- For batch data, I would consider using AWS EMR/Glue/Lambda for both ingestion and ETL.  For ingesting streaming data, I would look into a stream processor like Kinesis or MKS(managed Kafka) for more configurability.  For streaming receiving data from the processor and ETL, I would try Glue (managed Spark) or Step/Lambda functions for smaller jobs.  
- DynamoDB (managed NoSQL) is good for storage in lower-frequency, event-driven data patterns, Redshift for very large-scale data, and S3 for aggregating from many sources.  For more advanced queries in downstream analysis, I would consider RDS (managed SQL) and Redshift.  

**Next steps: for a use case involving millions of sensors in the ocean and collecting billions of records per day**
- I would explore using a time series database like TimeScaleDB or InfluxDB, which is very well-suited for IoT/sensor data patterns.  TimeScaleDB is built on top of PostgreSQL and benefits from its fault-tolerance and widely-used query language (which would help a data science team a lot).  I like the compiled environment of Golang for insert performance in InfluxDB, but have read that higher cardinality dimensions can cause a large drop-off.  
- To deploy either of these, I would look into deploying it on a Docker image on AWS EC2, or on ECS (managed containers), or EKS (managed K8s).  AWS also has a managed time-series DB called Timestream, but as a NoSQL DB, its SQL queries are likely more limited than the native sorts of queries you can perform on TimeScaleDB/Postgres (complex joins, window functions, etc.).

**Next steps: integrating a neural network-based model that forecasts the duration of a big wave session into this architecture**
- I'd expose a new endpoint called `/forecast` that takes a POST http method in `api.py`.  I would include the trained and pickled model in the waimea directory and load it in the new `/forecast` endpoint in order to pass the POST request body data containing the input features to the model and return the prediction for wave duration.  Then I would add the new PyTorch/TensorFlow dependencies to `requires.txt`.  This way, a POST request to the `/forecast` endpoint could be made from anywhere (e.g. triggered by alerts) with the feature inputs.
