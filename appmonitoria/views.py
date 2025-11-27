from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.shortcuts import redirect

from users.models import CustomUser, Profile
from events.models import Event, Team, Availability
from monitoria.models import Payment


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = Profile.objects.select_related("category").filter(user=request.user).first()
            if profile and profile.category and profile.category.title.lower() in {"m1", "m2", "m3"} and not request.user.is_staff:
                return redirect("monitoria:monitor_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_users = CustomUser.objects.count()
        total_profiles = Profile.objects.count()
        total_events = Event.objects.count()
        total_payments = Payment.objects.aggregate(total=Sum("amount")).get("total") or 0

        team_open = Team.objects.filter(status=False).count()
        availabilities_open = Availability.objects.filter(status=True).count()

        upcoming_events = (
            Event.objects.select_related("resort")
            .order_by("start_date")
            .all()[:3]
        )
        recent_payments = (
            Payment.objects.select_related("profile", "event")
            .order_by("-id")
            .all()[:5]
        )

        context.update(
            {
                "metrics": {
                    "users": total_users,
                    "profiles": total_profiles,
                    "events": total_events,
                    "payments_total": total_payments,
                    "teams_open": team_open,
                    "availabilities_open": availabilities_open,
                },
                "upcoming_events": upcoming_events,
                "recent_payments": recent_payments,
                "show_admin": self.request.user.is_staff,
            }
        )
        return context
