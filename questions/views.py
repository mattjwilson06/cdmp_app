from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django import forms
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic import DetailView

from .models import QuestionPool, Question, QuestionVersion, QuestionPoolAssociation
from .forms import QuestionPoolForm, QuestionForm, AnswerFormSet

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .models import QuestionPool, Question, QuestionVersion, QuestionPoolAssociation
from .forms import QuestionForm, QuestionPoolSelectionForm, AnswerFormSet


class QuestionPoolCreateView(LoginRequiredMixin, CreateView):
    model = QuestionPool
    form_class = QuestionPoolForm
    template_name = 'questions/pool_form.html'
    success_url = reverse_lazy('pool_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class QuestionPoolDetailView(LoginRequiredMixin, DetailView):
    model = QuestionPool
    template_name = 'questions/pool_detail.html'
    context_object_name = 'pool'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.question_set.all()
        return context


class QuestionPoolSelectionForm(forms.Form):
    pools = forms.ModelMultipleChoiceField(
        queryset=QuestionPool.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class QuestionPoolListView(LoginRequiredMixin, View):
    def get(self, request):
        pools = QuestionPool.objects.all()
        return render(request, 'questions/pool_list.html', {'pools': pools})

class QuestionCreateView(LoginRequiredMixin, View):
    def get(self, request, pool_id=None):
        form = QuestionForm()
        pool_form = QuestionPoolSelectionForm()
        formset = AnswerFormSet()
        
        if pool_id:
            pool = get_object_or_404(QuestionPool, id=pool_id)
            pool_form = QuestionPoolSelectionForm(initial={'pools': [pool]})
        
        return render(request, 'questions/question_form.html', {
            'form': form,
            'pool_form': pool_form,
            'formset': formset,
            'pool_id': pool_id
        })

    def post(self, request, pool_id=None):
        form = QuestionForm(request.POST)
        pool_form = QuestionPoolSelectionForm(request.POST)
        formset = AnswerFormSet(request.POST)
        
        if form.is_valid() and pool_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                question = form.save(commit=False)
                question.created_by = request.user
                question.save()

                question_version = QuestionVersion.objects.create(
                    question=question,
                    text=form.cleaned_data['text'],
                    created_by=request.user,
                    version_number=1
                )
                question.current_version = question_version
                question.save()

                # Save formset
                for answer_form in formset:
                    if answer_form.is_valid() and answer_form.has_changed():
                        answer = answer_form.save(commit=False)
                        answer.question = question
                        answer.question_version = question_version
                        answer.save()

                selected_pools = pool_form.cleaned_data['pools']
                
                # If pool_id is provided, ensure this pool is included
                if pool_id:
                    specific_pool = get_object_or_404(QuestionPool, id=pool_id)
                    if specific_pool not in selected_pools:
                        selected_pools.append(specific_pool)

                for pool in selected_pools:
                    QuestionPoolAssociation.objects.create(
                        question=question,
                        pool=pool,
                        added_by=request.user
                    )

            # Redirect to the detail view of the pool where the question was added
            redirect_pool = specific_pool if pool_id else selected_pools[0]
            return redirect('pool_detail', pk=redirect_pool.id)
        
        return render(request, 'questions/question_form.html', {
            'form': form,
            'pool_form': pool_form,
            'formset': formset,
            'pool_id': pool_id
        })