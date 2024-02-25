from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import BoopBoard
from django.views.generic import View
from django.core.serializers import serialize
import json
from django.http import StreamingHttpResponse
from asgiref.sync import sync_to_async
import asyncio

import time






"""
This is the view for the Server-Sent Events (SSE) endpoint. It sends a stream of data to the client containing
a json object of the Boop objects in the database. This is used to update the client's BoopBoard in close to real-time (~3 sec).
"""
class SSE(View):
    async def get(self, request, *args, **kwargs):
        # Asynchronous generator function to stream SSE events
        async def generate_sse_events():
            try:
                while True:
                    # Retrieve data from the BoopBoard model
                    boop_board = await sync_to_async(BoopBoard.objects.get)(name="Website BoopBoard")
                    serversBoops = boop_board.boop_set.all()

                    # Convert the queryset to an asynchronous operation
                    serversBoops_async = await sync_to_async(list)(serversBoops)

                    
                    # Convert Boop objects to dictionary format
                    boop_data = [{'id': boop.thisID, 'booped': boop.booped} for boop in serversBoops_async]

                    # Send SSE events for each Boop object
                    for data in boop_data:
                        yield f"id: {data['id']}\n"
                        yield f"data: {json.dumps(data)}\n\n"
                    
                    # Sleep for some time before sending the next event
                    await asyncio.sleep(0.5)  # Adjust the delay as needed
            except GeneratorExit:
                pass # Close the generator

        # Return the SSE response with the asynchronous generator function
        return StreamingHttpResponse(generate_sse_events(), content_type='text/event-stream')
    


    # # This function is called when the client sends a GET request to the SSE endpoint (about every 3 seconds).
    # def get(self, request, *args, **kwargs):
    #     print("SSE view______GET")
    #     response = HttpResponse(content_type='text/event-stream')
    #     response['Cache-Control'] = 'no-cache'
    #     response['Retry'] = 'none'
    #     # response['Connection'] = 'keep-alive'

    #     # Retrieve data from the Boop model
    #     # justBoops = Boop.objects.all()

    #     # Retrieve data from the BoopBoard model
    #     boop_board = BoopBoard.objects.get(name="Website BoopBoard")  # The name of our BoopBoard object
    #     if boop_board:
    #         print("BoopBoard exists")
    #         serversBoops = boop_board.boop_set.all()

    #     # Convert Boop objects to dictionary format
    #     boop_data = [{'id': boop.thisID, 'booped': boop.booped} for boop in serversBoops]

    #     for data in boop_data:
    #         response.write(f"id: {data['id']}\n") # Send the Boop ID
    #         response.write(f"data: {json.dumps(data)}\n\n")  # Serialize data to JSON
    #         response.flush()
    #         print("SSE response sent")
    #     # time.sleep(5)
    #     return response
    

        


# This is the view for the home page. It renders the buttons.html template (only called at the start of the client's session).
def home(request):
    return render(request, "buttons.html")


# This function sends the Server-Sent Events (SSE) to the client
def send_sse(data):
    # Construct the SSE message data
    # message_data = {
    #     'id': 123,
    #     'type': 'update',
    #     'data': 'Some data to send to the client'
    # }

    # # Format the SSE message as a string
    # sse_message = f"id: {message_data['id']}\n"
    # sse_message += f"event: {message_data['type']}\n"
    # sse_message += f"data: {json.dumps(message_data['data'])}\n\n"

    # # Create the HTTP response with SSE message
    # response = HttpResponse(sse_message, content_type='text/event-stream')
    # response['Cache-Control'] = 'no-cache'
    # response['Last-Event-ID'] = str(message_data['id'])








    # Construct SSE message
    # event_data = {
    #     'data': data  # SSE event data
    # }

    # Format SSE message
    # sse_message = f"data: {json.dumps(event_data)}\n\n"
    # response.write(f"id: {data['id']}\n") # Send the Boop ID


    # Create HTTP response with SSE message
    response = HttpResponse(content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response.write(f"id: {data['id']}\n") # Send the Boop ID


    # boop_data = [{'id': boop.thisID, 'booped': boop.booped}

    return response








    # event = f"data: {data}\n\n"
    # print("send_sse")

    # response = HttpResponse(event, content_type='text/event-stream')
    # response['Cache-Control'] = 'no-cache'

    # response.write(f"id: {data['id']}\n") # Send the Boop ID
    # response.write(f"data: {json.dumps(data)}\n\n")  # Serialize data to JSON
    # response.flush()

    # return response
    
    # return HttpResponse(event, content_type='text/event-stream')


# This function is called when the client sends an ajax POST request to the update_button_state endpoint.
def update_button_state_view(request):
    if request.method == "POST":
        print("update_button_state_view")
        button_id = request.POST.get("button_id")
        boop_board = BoopBoard.objects.get(name="Website BoopBoard")  # The first (and only) BoopBoard object
        if boop_board:
            serversBoops = boop_board.boop_set.all()
            button = serversBoops.get(thisID=button_id)
            button.toggle_booped()
        else:
            print("BoopBoard does not exist")
            return JsonResponse({'status': 'error', 'message': 'BoopBoard does not exist'})

        # Send SSE to all clients
        # button_data = serialize('json', [button])
        # send_sse(button_data)

        return JsonResponse({'status': 'success', 'message': 'Button state updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Request method is not a POST'})
 
