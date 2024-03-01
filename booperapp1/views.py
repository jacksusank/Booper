from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from .models import BoopBoard
from asgiref.sync import sync_to_async
import json
import asyncio


# Set that will contain a queue for each connected client
connected_clients = set()

"""
This is the view for the Server-Sent Events (SSE) endpoint. It sends a stream of data to the client containing
a json object of the Boop objects in the database. This is used to update the client's BoopBoard in close to real-time (~3 sec).
"""
class SSE(View):
    async def get(self, request, *args, **kwargs):
        # Asynchronous generator function to stream SSE events
        async def generate_sse_events():
            myQueue = asyncio.Queue() # This is a queue that we will use to know when to send data to the client
            myQueue.put_nowait(1) # This is to ensure that whenever a client establishes an sse connection, they get the data
            connected_clients.add(myQueue) # Add the queue to the set of connected clients
            try:
                while await myQueue.get(): # This is an asynchronous operation that waits for the queue to have a value
                    boop_board = await sync_to_async(BoopBoard.objects.get)(name="Website BoopBoard") # Our serverside BoopBoard
                    serversBoops = boop_board.boop_set.all() # This is a queryset of all the Boop objects in the BoopBoard

                    # Convert the queryset to an asynchronous operation
                    serversBoops_async = await sync_to_async(list)(serversBoops)
                    
                    # Convert Boop objects to dictionary format
                    boop_data = [{'id': boop.thisID, 'booped': boop.booped} for boop in serversBoops_async]

                    # Send SSE events for each Boop object to this client
                    for data in boop_data:
                        yield f"data: {json.dumps(data)}\n\n" 

            except GeneratorExit: # If the client disconnects...
                connected_clients.remove(myQueue) # ...then remove them from the set of connected clients...
                del myQueue # ...and delete the queue...
                pass # ...and close the generator.

        # Return the SSE response with the asynchronous generator function
        return StreamingHttpResponse(generate_sse_events(), content_type='text/event-stream')


# This is the view for the home page. It renders the buttons.html template (only called at the start of the client's session).
def home(request):
    return render(request, "buttons.html")


async def add_to_queue(queue, data):
    await queue.put(data)


# This function is called when any client sends an ajax POST request to the update_button_state endpoint.
def update_button_state_view(request):
    if request.method == "POST":
        button_id = request.POST.get("button_id")
        boop_board = BoopBoard.objects.get(name="Website BoopBoard")  # The only BoopBoard object

        if boop_board:
            serversBoops = boop_board.boop_set.all()
            button = serversBoops.get(thisID=button_id)
            button.toggle_booped() # This changes the serverside state of the button
            for client_queue in connected_clients: # For each client that is connected...
                asyncio.run(add_to_queue(client_queue, button_id)) # ... add the button_id to their queue (this value is completely arbitrary, 
                # but it will trigger the server to yield data to the client).
                
        else:
            return JsonResponse({'status': 'error', 'message': 'BoopBoard does not exist'})
        return JsonResponse({'status': 'success', 'message': 'Button state updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Request method is not a POST'})
 
