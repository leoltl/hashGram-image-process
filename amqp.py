import pika
from decouple import config

# Create a global channel variable to hold our channel object in
channel = None
connection = None


def init(queue, handle_delivery):
  # Step #2
  def on_connected(connection):
      """Called when we are fully connected to RabbitMQ"""
      # Open a channel
      connection.channel(on_open_callback=on_channel_open)

  # Step #3
  def on_channel_open(new_channel):
      """Called when our channel has opened"""
      global channel
      channel = new_channel
      channel.queue_declare(queue=queue, durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

  # Step #4
  def on_queue_declared(frame):
      """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
      channel.basic_consume(queue, handle_delivery)

  # Step #1: Connect to RabbitMQ using the default parameters
  parameters = pika.URLParameters(config('CloudAMQP_URI'))
  global connection
  connection = pika.SelectConnection(parameters, on_open_callback=on_connected)
  return connection
