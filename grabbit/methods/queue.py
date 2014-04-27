
from grabbit.frames import Method


CLASS_ID = 50

class QueueMethod(Method):
	method_class = CLASS_ID


class DeclareOk(QueueMethod):
	"""Confirm queue was declared successfully.
	name: Name of declared queue. Important for generated names.
	messages: Count of messages held in queue (ready to be delivered)
	consumers: Count of consumers of this queue
	"""
	method_id = 11
	fields = [
		('name', ShortString),
		('messages', Long),
		('consumers', Long),
	]

class Declare(QueueMethod):
	"""Create a new queue if it doesn't already exist.
	Args:
		name: Queue name, limited to characters: a-z A-Z 0-9 _ . : -
		      If blank, a unique name is generated by the server.
		passive: Do not create the queue if it doesn't eixst (raise a NotFound instead)
		durable: Whether queue needs to persist across a broker restart. Note that persistent messages
		         are only useful when held in a durable queue.
		exclusive: Only this connection may interact with this queue, and it is deleted on disconnect
		autodelete: Automatically delete queue when the last consumer stops consuming from it.
	Some special error cases:
		PreconditionFailed: Name contained illegal characters
		ResourceLocked: Queue already exists and is exclusive to another connection
	"""
	method_id = 10
	response = DeclareOk
	fields = [
		(None, Short),
		('name', ShortString),
		(None, Bits('passive', 'durable', 'exclusive', 'autodelete', 'nowait')),
		('arguments', FieldTable),
	]

class BindOk(QueueMethod):
	"""Confirm queue bind was successful"""
	method_id = 21
	fields = []

class Bind(QueueMethod):
	"""Bind queue to exchange with given routing_key.
	This will cause messages on that exchange to be conditionally routed to the queue
	based on the exchange type and routing key.
	Note that binds between durable queues and durable exchanges are automatically durable.
	"""
	method_id = 20
	response = BindOk
	fields = [
		(None, Short),
		('queue', ShortString),
		('exchange', ShortString),
		('routing_key', ShortString),
		(None, Bits('nowait')),
		('arguments', FieldTable),
	]

class UnbindOk(QueueMethod):
	"""Confirm queue unbind was successful"""
	method_id = 51
	fields = []

class Unbind(QueueMethod):
	"""Cancel a binding between given queue and exchange with given routing_key.
	Raises NotFound if that exact combination of (queue, exchange, routing_key) cannot be found.
	"""
	method_id = 50
	response = UnbindOk
	has_nowait = False
	fields = [
		(None, Short),
		('queue', ShortString),
		('exchange', ShortString),
	]

class PurgeOk(QueueMethod):
	"""Confirm a queue has been purged.
	messages: Count of messages that were purged
	"""
	method_id = 31
	fields = [('messages', Long)]

class Purge(QueueMethod):
	"""Purge given queue, removing all messages that were ready to deliver."""
	method_id = 30
	response = PurgeOk
	fields = [
		(None, Short),
		('name', ShortString),
		(None, Bits('nowait')),
	]

class DeleteOk(QueueMethod):
	"""Confirm deletion of queue.
	messages: Count of messages that were ready to deliver at the time of deletion
	"""
	method_id = 41
	fields = [('messages', Long)]

class Delete(QueueMethod):
	"""Delete a queue, cancelling all consumers.
	if_unused: Only delete the queue if it has no consumers, else raise PreconditionFailed
	if_empty: Only delete the queue if it has no pending messages, else raise PreconditionFailed
	"""
	method_id = 40
	response = DeleteOk
	fields = [
		(None, Short),
		('name', ShortString),
		(None, Bits('if_unused', 'if_empty', 'nowait')),
	]
