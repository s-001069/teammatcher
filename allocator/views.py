import csv
import io
import json
import os
import random
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import UploadFileForm

def index(request):
    teams = []
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            team_size = form.cleaned_data['team_size']
            csv_file = request.FILES['file']
            
            # Read CSV file
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            # Store all rows
            all_students = list(reader)
            
            # Shuffle
            random.shuffle(all_students)
            
            # Load team names if available
            team_names = []
            config_path = os.path.join(settings.BASE_DIR, 'team_names.json')
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        team_names = json.load(f)
                except Exception:
                    pass # Fallback to default if error
            
            # Split and assign team numbers/names
            results_for_session = []
            
            for i in range(0, len(all_students), team_size):
                chunk = all_students[i:i + team_size]
                team_index = i // team_size
                
                if team_index < len(team_names):
                    team_name = team_names[team_index]
                else:
                    team_name = f'Team {team_index + 1}'
                
                # Add team info to each student and add to results
                for student in chunk:
                    student_with_team = student.copy()
                    student_with_team['team'] = team_name
                    results_for_session.append(student_with_team)
                
                # Pass tuple of (name, members) to template
                teams.append({'name': team_name, 'members': chunk})
            
            # Store in session for download
            request.session['results'] = results_for_session
            
    else:
        form = UploadFileForm()
        # Clear session if visiting fresh
        if 'results' in request.session:
            del request.session['results']

    return render(request, 'allocator/index.html', {'form': form, 'teams': teams})

def download_csv(request):
    results = request.session.get('results', [])
    
    if not results:
        return HttpResponse("No results found to download.", content_type='text/plain')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="teams.csv"'},
    )

    if results:
        # Get fieldnames from the first result
        fieldnames = list(results[0].keys())
        
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    return response
