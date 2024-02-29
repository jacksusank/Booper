from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from .models import BoopBoard
from asgiref.sync import sync_to_async
import json
import asyncio


# Maintain a set of connected client IDs
connected_clients = set()
masterQueue = asyncio.Queue()


"""
This is the view for the Server-Sent Events (SSE) endpoint. It sends a stream of data to the client containing
a json object of the Boop objects in the database. This is used to update the client's BoopBoard in close to real-time (~3 sec).
"""
class SSE(View):
    async def get(self, request, *args, **kwargs):
        # Asynchronous generator function to stream SSE events
        async def generate_sse_events():
            masterQueue.put_nowait(1) # This is to ensure that whenever a client establishes an sse connection, they get the data
            connected_clients.add(id(request))
            try:
                while True:
                    if not masterQueue.empty(): # If there is data in the queue then that means that there are changes that need to be sent to the clients
                        # Retrieve data from the BoopBoard model
                        masterQueue.get_nowait() # This returns and removes the first item in the queue
                        boop_board = await sync_to_async(BoopBoard.objects.get)(name="Website BoopBoard") # The our serverside BoopBoard
                        serversBoops = boop_board.boop_set.all() # This is a queryset of all the Boop objects in the BoopBoard

                        # Convert the queryset to an asynchronous operation
                        serversBoops_async = await sync_to_async(list)(serversBoops)

                        
                        # Convert Boop objects to dictionary format
                        boop_data = [{'id': boop.thisID, 'booped': boop.booped} for boop in serversBoops_async]

                        # Send SSE events for each Boop object to this client
                        for data in boop_data:
                            yield f"data: {json.dumps(data)}\n\n"
                        
                    else:
                        await asyncio.sleep(0.1)

            except GeneratorExit: # If the client disconnects...
                connected_clients.remove(id(request)) # ...then remove them from the set of connected clients...
                pass # ...and close the generator.

        # Return the SSE response with the asynchronous generator function
        return StreamingHttpResponse(generate_sse_events(), content_type='text/event-stream')


# This is the view for the home page. It renders the buttons.html template (only called at the start of the client's session).
def home(request):
    return render(request, "buttons.html")


# This function is called when any client sends an ajax POST request to the update_button_state endpoint.
def update_button_state_view(request):
    if request.method == "POST":
        button_id = request.POST.get("button_id")
        boop_board = BoopBoard.objects.get(name="Website BoopBoard")  # The only BoopBoard object

        if boop_board:
            serversBoops = boop_board.boop_set.all()
            button = serversBoops.get(thisID=button_id)
            button.toggle_booped() # This changes the serverside state of the button
            for i in range(connected_clients.__len__()):
                masterQueue.put_nowait(button_id) 
                # We add this arbitrary value to the queue this many times because we are going to send an sse to 
                # each of the clients and for each one, we are going to take one item off of the queue

        else:
            return JsonResponse({'status': 'error', 'message': 'BoopBoard does not exist'})
        return JsonResponse({'status': 'success', 'message': 'Button state updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Request method is not a POST'})
 
