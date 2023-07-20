from django.shortcuts import render, get_object_or_404, redirect
from ..models import Meeting
from datetime import datetime
from django.utils import timezone
import random
import string
from .forms import ParticipantForm

def join_meeting(request, meeting_id):
    # Get the meeting object or return a 404 error if not found
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Convert the current time to the timezone of the meeting start time
    current_time = timezone.localtime(timezone.now())

    # Convert the meeting start time to the same timezone format as current_time
    meeting_start_time = timezone.localtime(meeting.start_time)

    # Check if the meeting has already started or ended
    has_started = meeting_start_time <= current_time
    has_ended = meeting.end_time <= current_time

    if not has_started:
        # Meeting has not started yet
        return render(request, 'not_started.html', {'meeting': meeting})
    
    if has_ended:
        # Meeting has already ended
        return render(request, 'ended.html', {'meeting': meeting})
    
    if request.method == 'POST':
        # Process the form submission
        form = ParticipantForm(request.POST)
        
        if form.is_valid():
            # The form data is valid, process the participant's details here
            participant_name = form.cleaned_data['participant_name']
            
            # Save the participant's details to the database or handle as needed
            
            # Redirect to the meeting room or any other desired page
            return redirect('virtual_app:meeting_room', meeting_id=meeting_id)
    else:
        # If it's a GET request, display the form for the user to enter their details
        form = ParticipantForm()

    return render(request, 'join_meeting.html', {
        'meeting': meeting,
        'form': form,
    })

def meeting_room(request, meeting_id):
    # Get the meeting object or return a 404 error if not found
    meeting = get_object_or_404(Meeting, id=meeting_id)
    
    # Retrieve the participant_token from the request (assumed to be passed in the URL query params)
    participant_token = request.GET.get('participant_token', '')
    
    return render(request, 'meeting_room.html', {
        'meeting': meeting,
        'participant_token': participant_token,
    })
