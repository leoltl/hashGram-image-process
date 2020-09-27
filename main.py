import amqp
import image
import storage
import json

def handle_delivery(channel, method, header, body):
  try:
    print(body)
    payload = json.loads(body)
    resource_key=payload["resource_key"]
    image.process(resource_key, payload["filters"])
    img_data = open(f'./{resource_key}.jpg', 'rb')
    storage.put_image(resource_key, img_data)
    img_data.close()
    channel.basic_ack(delivery_tag=method.delivery_tag)
    image.prune(resource_key)
  except Exception as e:
    print(e)

storage.init()
connection = amqp.init('upload', handle_delivery)

# start_consuming
try:
  # Loop so we can communicate with RabbitMQ
  connection.ioloop.start()
except KeyboardInterrupt:
  # Gracefully close the connection
  connection.close()
  # Loop until we're fully closed, will stop on its own
  connection.ioloop.start()