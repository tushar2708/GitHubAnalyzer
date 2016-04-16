from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from GitIssues.models import Query
from GitIssues.models import Result
from GitIssues.forms import QueryForm

# Create your views here.
@login_required
def query_list(request):
    try:
        queries = sorted(Query.objects.exclude(GitHubPublicRepo=""), reverse= True)
    except Query.DoesNotExist:
        raise Http404('No Valid Query exists in history')
    return render(request, 'GitIssues/query_list.html', {
        'queries': queries,
        })

'''
    View to accept new query on home pag
'''
@login_required
def query_new(request):
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.userName = request.user
            query.query_date = timezone.now()
            query.CreateQuery("openIssues")
            query.save()
            return redirect('result_detail', id=query.id)
    else:
        form = QueryForm()
        return render(request, 'GitIssues/query_new.html', {'form': form})

'''
    View to show resulting counts on result's page
'''
@login_required
def result_detail(request, id):
    query = Query.objects.get(id=id)
    result = Result.objects.create(QueryStr = query.restQry);
    result.createResult();
    result.save()
    return render(request, 'GitIssues/result_detail.html', {
        'result': result,
    })


