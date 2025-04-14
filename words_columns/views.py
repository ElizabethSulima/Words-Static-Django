import math
import re
from collections import Counter

from django.shortcuts import render

from .forms import UploadForm


total_documents = 10000000
document_frequencies = Counter()


def get_form(request):
    return render(request, "app/index.html")


def handle_uploaded_file(f):
    text = list(f.chunks())[0].decode("utf-8")
    words = re.findall(
        r"([а-яА-ЯёЁa-zA-Z]+)\b",
        text,
    )
    words_list = [word.lower() for word in words]
    all_count_words = len(words_list)
    word_counts = Counter(words_list)

    tf = {word: count / all_count_words for word, count in word_counts.items()}

    for word in set(words_list):
        document_frequencies[word] += 1

    idf = {
        word: math.log(total_documents / document_frequencies[word])
        for word in tf.keys()
    }
    tf_idf_list = [
        (word, tf_val, idf_val)
        for word, tf_val in tf.items()
        for idf_val in [idf[word]]
    ]
    sorted_tf_idf_list = sorted(tf_idf_list, key=lambda x: x[2], reverse=True)[
        :50
    ]

    return sorted_tf_idf_list


def output_words(request):
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        list_data = handle_uploaded_file(request.FILES["my_file"])
        return render(request, "app/result.html", {"data": list_data})

    return render(request, "app/index.html", context={})
