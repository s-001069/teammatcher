import csv
import io

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import pandas as pd 

from teacher_side.matcher.genetic_matcher import match
from teacher_side.matcher.random_matcher import random_match
from teacher_side.matcher.utils import *
from .forms import UploadFileForm
from .models import CSVGeneration


def index(request):
    teams = []

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            team_size = form.cleaned_data['team_size']
            team_template = form.cleaned_data.get('team_template')

            df = pd.read_csv(request.FILES['file'])
            weights = get_weights(form)
            df_result, target_col, best_fitness = match(df, team_template, weights)
            print("Best fitness:", best_fitness)

            # csv generation
            csv_content = df_result.to_csv(index=False)
            CSVGeneration.objects.create_generation(
                    csv_data=csv_content,
                    team_size=team_size,
                    template_used=team_template,
                    student_count=df.shape[0]
            )


            grouped = df_result.groupby(target_col)
            for name, group in grouped:
                teams.append({
                    'name': name,
                    'members': group.to_dict('records') # convert group rows to list of dicts
                })
            
            teams.sort(key=lambda x: int(x['name'].split()[-1]) if x['name'].split()[-1].isdigit() else 999)
        else:
            print(form.errors)
    else:
        form = UploadFileForm()
        if 'results' in request.session:
            del request.session['results']

    historical_generations = CSVGeneration.objects.order_by('-id')[:5] # ordered to get the most recent

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
            'Content-Disposition': 
                f'attachment; filename="teams_{generation.generated_at.strftime("%Y%m%d_%H%M%S")}.csv"'
        },
    )
    response.write(generation.csv_data)
    return response
