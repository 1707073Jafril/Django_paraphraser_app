# paraphrase/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .some_paraphrase_library import paraphrase_function
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def paraphrase_view(request):
    if request.method == "POST":
        input_text = request.POST.get('input_paragraph', '')

        # Call your paraphrasing function
        paraphrased_sentences = paraphrase_function(input_text)

        # Calculate similarity scores between input and each paraphrase
        similarity_scores = calculate_similarity(input_text, paraphrased_sentences)

        # Combine paraphrased sentences with their similarity scores
        paraphrased_results = [
            {'paraphrase': sentence, 'similarity': round(similarity, 2)}
            for sentence, similarity in zip(paraphrased_sentences, similarity_scores)
        ]

        return render(request, 'paraphrase/index.html', {
            'input_text': input_text,
            'paraphrased_results': paraphrased_results
        })

    return render(request, 'paraphrase/index.html')


def download_txt(request):
    if request.method == "POST":
        input_text = request.POST.get('input_text', '')
        paraphrased_results_json = request.POST.get('paraphrased_results', '[]')

        try:
            paraphrased_results = json.loads(paraphrased_results_json)
        except json.JSONDecodeError:
            paraphrased_results = []

        # Create a string for the content to be downloaded
        content = f"Input Text:\n{input_text}\n\n"
        content += "Paraphrased Sentence\t\t| Similarity Score\n"
        content += "=" * 80 + "\n"
        for result in paraphrased_results:
            paraphrase = result['paraphrase']
            similarity = result['similarity']
            content += f"{paraphrase}\t| {similarity}\n"

        # Create the HTTP response with the content
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=paraphrased_results.txt'

        return response

    # If not a POST request, redirect back to the paraphrase view or return a proper response



def calculate_similarity(original, paraphrased_list):
    # Use TF-IDF to represent the texts
    vectorizer = TfidfVectorizer().fit_transform([original] + paraphrased_list)
    vectors = vectorizer.toarray()

    # Calculate cosine similarity between the original and each paraphrase
    cosine_similarities = cosine_similarity([vectors[0]], vectors[1:])[0]
    
    return cosine_similarities
