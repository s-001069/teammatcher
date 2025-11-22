import csv
import io
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import TeamNameTemplate, CSVGeneration
import random


def index(request):
    teams = []
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            team_size = form.cleaned_data['team_size']
            team_template = form.cleaned_data.get('team_template')
            csv_file = request.FILES['file']
            
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            all_students = list(reader)
            
            random.shuffle(all_students)
            
            team_names = []
            if team_template:
                team_names = team_template.team_names
            
            results_for_csv = []
            
            for i in range(0, len(all_students), team_size):
                chunk = all_students[i:i + team_size]
                team_index = i // team_size
                
                if team_index < len(team_names):
                    team_name = team_names[team_index]
                else:
                    team_name = f'Team {team_index + 1}'
                
                for student in chunk:
                    student_with_team = student.copy()
                    student_with_team['team'] = team_name
                    results_for_csv.append(student_with_team)
                
                teams.append({'name': team_name, 'members': chunk})
            
            if results_for_csv:
                output = io.StringIO()
                fieldnames = list(results_for_csv[0].keys())
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results_for_csv)
                csv_data = output.getvalue()
                
                CSVGeneration.objects.create_generation(
                    csv_data=csv_data,
                    team_size=team_size,
                    template_used=team_template,
                    student_count=len(all_students)
                )
            
            request.session['results'] = results_for_csv
            
    else:
        form = UploadFileForm()
        if 'results' in request.session:
            del request.session['results']

    historical_generations = CSVGeneration.objects.all()[:5]

    return render(request, 'allocator/index.html', {
        'form': form,
        'teams': teams,
        'historical_generations': historical_generations
    })


def download_csv(request):
    results = request.session.get('results', [])
    
    if not results:
        latest_generation = CSVGeneration.objects.first()
        if latest_generation:
            response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': 'attachment; filename="teams_latest.csv"'},
            )
            response.write(latest_generation.csv_data)
            return response
        else:
            return HttpResponse("No results found to download.", content_type='text/plain')

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="teams.csv"'},
    )

    if results:
        fieldnames = list(results[0].keys())
        
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    return response


def download_historical_csv(request, generation_id):
    generation = get_object_or_404(CSVGeneration, id=generation_id)
    
    response = HttpResponse(
        content_type='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename="teams_{generation.generated_at.strftime("%Y%m%d_%H%M%S")}.csv"'
        },
    )
    response.write(generation.csv_data)
    return response
