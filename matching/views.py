from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import MatchingForm
from .models import MatchingResult
from django.contrib.auth.decorators import login_required
#import requests
#import matplotlib.pyplot as plt
#import io
#import base64
#import pandas as pd
from django.http import FileResponse
#from .utils import generate_dashboard_pdf

from .forms import MatchingForm


#import requests
from django.shortcuts import render
from .forms import MatchingForm
from .utils import extract_text_and_images_from_file  # Assure-toi d'importer ta fonction
from django.contrib import messages


API_URL = "http://localhost:8001/predict"  # <-- à adapter selon ton déploiement




@login_required
# matching/views.py
def matching_view(request):
    result = None
    confidence = None

    if request.method == 'POST':
        form = MatchingForm(request.POST, request.FILES)
        if form.is_valid():
            titre = form.cleaned_data['titre']
            fichier = form.cleaned_data['fichier']

            try:
                # 🔍 Extraction du texte enrichi (texte brut + OCR)
                texte, images = extract_text_and_images_from_file(fichier)

                # 📡 Appel à l'API IA
                response = requests.post(API_URL, json={"text": texte})

                if response.status_code == 200:
                    json_response = response.json()
                    result = json_response.get("prediction")
                    confidence = json_response.get("confidence")
                    MatchingResult.objects.create(
    utilisateur=request.user,
    titre=titre,
    texte_nettoye=texte,
    niveau_pred=result,
    success_rate=confidence
)


                else:
                    messages.error(request, "Erreur lors de l'appel à l'API. Code: " + str(response.status_code))

            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {str(e)}")

    else:
        form = MatchingForm()

    return render(request, 'matchs/matching.html', {
        'form': form,
        'result': result,
        'confidence': confidence
    })





from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractYear
from .models import MatchingResult
#import json


@login_required
def dashboard_view(request):
    # Données filtrées par utilisateur
    results = MatchingResult.objects.filter(utilisateur=request.user).order_by('-date_analyse')

    # 📊 Diagramme en secteurs : répartition par niveau
    niveau_counts = results.values('niveau_pred').annotate(total=Count('id'))
    pie_data = {
        'labels': [n['niveau_pred'] for n in niveau_counts],
        'values': [n['total'] for n in niveau_counts]
    }

    # 📈 Histogramme annuel : nombre de matchings par année
    year_counts = results.annotate(year=ExtractYear('date_analyse')) \
                         .values('year').annotate(total=Count('id')).order_by('year')
    bar_data = {
        'labels': [str(y['year']) for y in year_counts],
        'values': [y['total'] for y in year_counts]
    }

    # 🔁 Envoi des données au template
    context = {
        'results': results,
        'pie_data': json.dumps(pie_data),
        'bar_data': json.dumps(bar_data)
    }

    return render(request, 'matchs/dashboard.html', context)




#from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse
import io
@login_required
def download_pdf(request):
    results = MatchingResult.objects.filter(utilisateur=request.user)
    html = render_to_string("pdf/historique_pdf.html", {'results': results, 'user': request.user})
    result = io.BytesIO()
    pisa.CreatePDF(io.StringIO(html), dest=result)
    result.seek(0)
    return HttpResponse(result.read(), content_type='application/pdf')
@login_required
def home(request):
    return render(request, 'matchs/accueil.html')

@login_required
def accueil(request):
    return render(request, 'matchs/accueil.html')
@login_required
def aligner(request):
    return render(request, 'matchs/matching.html')
@login_required
def result(request):
    return render(request, 'matchs/result.html')
@login_required
def base1(request):
    return render(request, 'base1.html')
# from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# from io import BytesIO
# from .models import MatchingResult

# def export_dashboard_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=\"dashboard_skilmapp.pdf\"'
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
    
#     # Texte
#     p.setFont("Helvetica-Bold", 16)
#     p.drawString(50, 800, "Rapport Skilmapp - Historique des Matchings")

#     # Données (exemples)
#     results = MatchingResult.objects.all()
#     labels = ['Succès', 'Échec']
#     success = results.filter(score__gte=50).count()
#     fail = results.count() - success

#     # Graphique circulaire
#     fig = Figure(figsize=(4, 4))
#     ax = fig.add_subplot(111)
#     ax.pie([success, fail], labels=labels, autopct='%1.1f%%', colors=["#2ecc71", "#e74c3c"])
#     ax.set_title("Taux de succès des matchings")

#     # Intégration graphique dans PDF
#     pie_buffer = BytesIO()
#     FigureCanvas(fig).print_png(pie_buffer)
#     p.drawImage(ImageReader(pie_buffer), 50, 500, width=300, height=300)

#     # Fin
#     p.showPage()
#     p.save()
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#     return response
