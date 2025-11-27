from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from decimal import Decimal, InvalidOperation
from django.db.models import Sum

from monitoria.models import Payment
from users.models import Profile
from weasyprint import HTML

from events.models import Availability, Cancellation, Event, Product, Resort, Team
from events.serializers import (
    AvailabilitySerializer,
    CancellationSerializer,
    EventSerializer,
    ProductSerializer,
    ResortSerializer,
    TeamSerializer,
)


from formtools.wizard.views import SessionWizardView
from .forms import EventForm, TeamForm, AvailabilityForm

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class CancellationViewSet(viewsets.ModelViewSet):
    queryset = Cancellation.objects.all()
    serializer_class = CancellationSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ResortViewSet(viewsets.ModelViewSet):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer


class EventListView(ListView):
    template_name = "events/event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        return (
            Event.objects.select_related("resort")
            .prefetch_related("team__availabilities__profile")
            .order_by("start_date", "name")
        )


class EventDetailView(DetailView):
    template_name = "events/event_detail.html"
    context_object_name = "event"
    model = Event

    def get_queryset(self):
        return Event.objects.select_related("resort").prefetch_related(
            "team__availabilities__profile__user"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = getattr(self.object, "team", None)
        context["team"] = team
        if team:
            context["availabilities"] = team.availabilities.select_related(
                "profile", "profile__user"
            )
        else:
            context["availabilities"] = []
        return context


class EventCreateView(View):
    template_name = "events/event_form.html"

    def get(self, request):
        event_form = EventForm()
        team_form = TeamForm(prefix="team")
        return render(
            request,
            self.template_name,
            {"event_form": event_form, "team_form": team_form},
        )

    def post(self, request):
        event_form = EventForm(request.POST)
        team_form = TeamForm(request.POST, prefix="team")

        team_has_data = team_form.has_changed()

        if not event_form.is_valid() or (team_has_data and not team_form.is_valid()):
            return render(
                request,
                self.template_name,
                {"event_form": event_form, "team_form": team_form},
            )

        event = event_form.save()

        if team_has_data:
            team = team_form.save(commit=False)
            team.event = event
            team.save()

        return redirect("events:event_detail", pk=event.pk)


class TeamListView(ListView):
    template_name = "events/team_list.html"
    context_object_name = "teams"

    def get_queryset(self):
        return Team.objects.select_related("event").prefetch_related("availabilities__profile").order_by(
            "event__start_date", "name"
        )


class TeamDetailView(DetailView):
    template_name = "events/team_detail.html"
    context_object_name = "team"
    model = Team

    def get_queryset(self):
        return Team.objects.select_related("event").prefetch_related(
            "availabilities__profile", "availabilities__profile__user"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["availabilities"] = self.object.availabilities.select_related(
            "profile", "profile__user"
        )
        from .forms import AvailabilityCreateForm
        context["availability_form"] = AvailabilityCreateForm()
        return context


class TeamStatusUpdateView(View):
    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        action = request.POST.get("action")
        if action == "close":
            team.status = True
        elif action == "open":
            team.status = False
        team.save()
        return redirect("events:team_detail", pk=pk)


class AvailabilityStatusUpdateView(View):
    def post(self, request, pk):
        availability = get_object_or_404(Availability, pk=pk)
        if "status" in request.POST:
            availability.status = request.POST.get("status") == "true"
        if "summoned" in request.POST:
            availability.summoned = request.POST.get("summoned") == "true"
        reason = request.POST.get("cancel_reason")
        clear_cancel = request.POST.get("clear_cancel")
        if clear_cancel:
            availability.cancellation = None
        if reason:
            cancellation = Cancellation.objects.create(reason=reason, availability=availability)
            availability.cancellation = cancellation
            availability.status = False
        availability.save()
        return redirect("events:team_detail", pk=availability.team_id)


class TeamAvailabilityCreateView(View):
    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        from .forms import AvailabilityCreateForm

        form = AvailabilityCreateForm(request.POST)
        if form.is_valid():
            form.save_with_team(team)
        return redirect("events:team_detail", pk=pk)


class SelfAvailabilityView(View):
    """Monitor marca disponibilidade para o evento/time vinculado ao evento."""

    def post(self, request, event_pk):
        if not request.user.is_authenticated:
            return redirect("events:event_detail", pk=event_pk)

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect("events:event_detail", pk=event_pk)

        event = get_object_or_404(Event, pk=event_pk)
        team = getattr(event, "team", None)
        if not team or team.status:
            return redirect("events:event_detail", pk=event_pk)

        availability, created = Availability.objects.get_or_create(
            team=team, profile=profile, defaults={"status": True}
        )
        if not created:
            availability.status = True
        availability.save()

        return redirect("events:event_detail", pk=event_pk)


# Product pages
class ProductListView(ListView):
    template_name = "events/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.prefetch_related("events").all().order_by("name")


class ProductDetailView(DetailView):
    template_name = "events/product_detail.html"
    context_object_name = "product"
    model = Product

    def get_queryset(self):
        return Product.objects.prefetch_related("events")


class ProductCreateView(View):
    template_name = "events/product_form.html"

    def get(self, request):
        from .forms import ProductForm

        form = ProductForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        from .forms import ProductForm

        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect("events:product_detail", pk=product.pk)
        return render(request, self.template_name, {"form": form})


class ProductUpdateView(View):
    template_name = "events/product_form.html"

    def get(self, request, pk):
        from .forms import ProductForm

        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, self.template_name, {"form": form, "product": product})

    def post(self, request, pk):
        from .forms import ProductForm

        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("events:product_detail", pk=product.pk)
        return render(request, self.template_name, {"form": form, "product": product})


class ResortListView(ListView):
    template_name = "events/resort_list.html"
    context_object_name = "resorts"

    def get_queryset(self):
        return Resort.objects.prefetch_related("events").all().order_by("name")


class ResortDetailView(DetailView):
    template_name = "events/resort_detail.html"
    context_object_name = "resort"
    model = Resort

    def get_queryset(self):
        return Resort.objects.prefetch_related("events")


class ResortCreateView(View):
    template_name = "events/resort_form.html"

    def get(self, request):
        from .forms import ResortForm

        form = ResortForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        from .forms import ResortForm

        form = ResortForm(request.POST)
        if form.is_valid():
            resort = form.save()
            return redirect("events:resort_detail", pk=resort.pk)
        return render(request, self.template_name, {"form": form})


class ResortUpdateView(View):
    template_name = "events/resort_form.html"

    def get(self, request, pk):
        from .forms import ResortForm

        resort = get_object_or_404(Resort, pk=pk)
        form = ResortForm(instance=resort)
        return render(request, self.template_name, {"form": form, "resort": resort})

    def post(self, request, pk):
        from .forms import ResortForm

        resort = get_object_or_404(Resort, pk=pk)
        form = ResortForm(request.POST, instance=resort)
        if form.is_valid():
            form.save()
            return redirect("events:resort_detail", pk=resort.pk)
        return render(request, self.template_name, {"form": form, "resort": resort})


class EventPaymentReportView(View):
    template_name = "events/event_payments_report.html"

    def get_filters(self, request):
        status = request.GET.get("status") or ""
        min_amount = request.GET.get("min_amount") or ""
        max_amount = request.GET.get("max_amount") or ""
        filters = {}
        if status:
            filters["status"] = status
        # Safe decimal parsing
        def parse_decimal(value):
            try:
                return Decimal(value)
            except (InvalidOperation, TypeError):
                return None
        min_val = parse_decimal(min_amount)
        max_val = parse_decimal(max_amount)
        return filters, min_val, max_val

    def get_queryset(self, event, filters, min_val, max_val):
        qs = Payment.objects.filter(event=event).select_related("profile", "profile__user")
        if "status" in filters:
            qs = qs.filter(status=filters["status"])
        if min_val is not None:
            qs = qs.filter(amount__gte=min_val)
        if max_val is not None:
            qs = qs.filter(amount__lte=max_val)
        return qs

    def build_context(self, event, payments, filters, min_val, max_val):
        agg = payments.aggregate(total=Sum("amount"))
        total_amount = agg.get("total") or Decimal("0")
        status_counts = {
            "PAID": payments.filter(status="PAID").count(),
            "PENDING": payments.filter(status="PENDING").count(),
            "CANCELED": payments.filter(status="CANCELED").count(),
        }
        return {
            "event": event,
            "payments": payments,
            "filters": {
                "status": filters.get("status", ""),
                "min_amount": min_val if min_val is not None else "",
                "max_amount": max_val if max_val is not None else "",
            },
            "summary": {
                "total_amount": total_amount,
                "count": payments.count(),
                "status_counts": status_counts,
            },
        }

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        filters, min_val, max_val = self.get_filters(request)
        payments = self.get_queryset(event, filters, min_val, max_val)
        context = self.build_context(event, payments, filters, min_val, max_val)

        if request.GET.get("format") == "pdf":
            html_string = render_to_string(self.template_name, {**context, "export": True})
            pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = f"relatorio_pagamentos_evento_{event.pk}.pdf"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        return render(request, self.template_name, context)


class EventWizard(SessionWizardView):
    template_name = "events/event_wizard.html"
    form_list = [EventForm, TeamForm, AvailabilityForm]

    def done(self, form_list, **kwargs):
        event_form = form_list[0]
        team_form = form_list[1]
        availability_form = form_list[2]

        event = event_form.save()
        team = team_form.save(commit=False)
        team.event = event
        team.save()

        availability = availability_form.save(commit=False)
        availability.team = team
        availability.save()

        return render(self.request, 'events/done.html', {
            'event': event,
            'team': team,
            'availability': availability
        })
