Event Service
Overview
The Event Service is a robust and scalable service designed to facilitate communication between various microservices, particularly for integrating with AWS Lambda functions and other services. It uses RabbitMQ as a message broker to handle events and route them to the appropriate services based on the type of event.

This service listens to specific queues, processes incoming messages, and performs necessary operations by invoking the appropriate callback functions.

Features
Event Handling: Listens to multiple queues and processes messages based on their type.
Scalability: Designed to handle a large volume of messages with configurable prefetch counts.
Reliability: Includes error handling and automatic reconnection to ensure continuous operation.
Installation
Prerequisites
Python 3.6 or higher
RabbitMQ server
Dependencies
Ensure you have the required Python libraries installed. You can install them using pip:

bash
Copy code
pip install pika
Configuration
RabbitMQ Host: Set the RabbitMQ server host in the variables.py file.

python
Copy code
HOST = 'localhost'  # Replace with your RabbitMQ server host
Callback Functions: Implement the callback functions for your services. Create files email.py and inventory.py with appropriate email_service_callback and inventory_service_callback functions, respectively.

python
Copy code
# email.py
def email_service_callback(ch, method, properties, body):
    # Process the message for the email service
    print('call the email service for operation')

# inventory.py
def inventory_service_callback(ch, method, properties, body):
    # Process the message for the inventory service
    print('call the inventory service for operation')
Usage
To start the event service, run the following command:

bash
Copy code
python event_service.py
This will:

Connect to RabbitMQ using the host specified in variables.py.
Declare queues for different services (email_events and inventory_events).
Start consuming messages from these queues and invoke the appropriate callback functions.
Error Handling
The service includes error handling and automatic reconnection to RabbitMQ in case of network issues or server restarts. If an error occurs, the service will log the error, close the connection, and retry after 5 seconds.

Contributing
Contributions to improve the event service are welcome! Please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any questions or issues, please contact:

Email: mr.sudarshanuprety@gmail.com
