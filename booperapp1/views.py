from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
#import the boop and boop board classes from models.py on next line from 
from . import models
from .models import Boop, BoopBoard

from django.views.generic import View
import time
import json
from .models import Boop, BoopBoard


# For the SSE view
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize




# Create your views here.
class SSE(View):
    def get(self, request, *args, **kwargs):
        print("SSE view______GET")
        response = HttpResponse(content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        # response['Connection'] = 'keep-alive'

        # Retrieve data from the Boop model
        justBoops = Boop.objects.all()


        # Retrieve data from the BoopBoard model
        boop_board = BoopBoard.objects.first()  # Assuming there's only one BoopBoard object
        if boop_board:
            print("BoopBoard exists")
            serversBoops = boop_board.boop_set.all()




        # Convert Boop objects to dictionary format
        boop_data = [{'id': boop.thisID, 'booped': boop.booped} for boop in serversBoops]



        for data in boop_data:
            print("This is Data")
            response.write(f"id: {data['id']}\n")
            response.write(f"data: {json.dumps(data)}\n\n")  # Serialize data to JSON
            # time.sleep(0.2)  # Simulate periodic updates
            response.flush()
            print("SSE response sent")
        
        return response

def home(request):
    return render(request, "buttons.html")


def send_sse(data):
    event = f"data: {data}\n\n"
    print("send_sse")
    return HttpResponse(event, content_type='text/event-stream')

def update_button_state_view(request):
    print("update_button_state_view")
    if request.method == "POST":
        print("update_button_state_view: request.method == POST")
        button_id = request.POST.get("button_id")
        print("Button id: " + button_id)
        # print(serversBoops)
        # button = serversBoops[int(button_id)-1]
        boop_board = BoopBoard.objects.first()  # Assuming there's only one BoopBoard object
        if boop_board:
            print("BoopBoard exists")
            serversBoops = boop_board.boop_set.all()
            button = serversBoops.get(thisID=button_id)
            button.toggle_booped()

        # Send SSE to all clients
        button_data = serialize('json', [button])
        send_sse(button_data)

        return JsonResponse({'status': 'success', 'message': 'Button state updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Request method is not a POST'})
