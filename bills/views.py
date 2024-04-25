from django.db.models import Count, Q, Sum
from django.views.generic import TemplateView
from bills.models import Bill, Legislator, Vote, VoteResult


class BillsView(TemplateView):
    """
    Template view for displaying bills and legislator voting data.

    Renders charts or tables based on the requested tab.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab"] = self.request.GET.get("tab", "")

        if context["tab"] in ("charts", "tables"):
            context["data"] = self.get_data()

        self.template_name = self.get_template(context["tab"])
        return context

    def get_data(self):
        """
        Fetches and aggregates bills and legislators voting data.

        Returns a dictionary containing:
            - legislators: QuerySet of legislators with annotations for
            total votes, yeas, and nays.
            - total_bills: Total number of bills voted on.
            - bills: QuerySet of bills with annotations for total votes, yeas,
            and nays.
            - votes_cast: Total number of votes cast across all bills.
        """

        legislators = self.get_legislators_data()
        bills = self.get_bills_data()

        return {**legislators, **bills}

    def get_bills_data(self):
        """
        Fetches and aggregates bills voting data.

        Returns a dictionary containing:
            - bills: QuerySet of bills with annotations for total votes, yeas,
            and nays.
            - votes_cast: Total number of votes cast across all bills.
        """

        yea = {'votes__results__vote_type': VoteResult.VoteType.YEA}
        nay = {'votes__results__vote_type': VoteResult.VoteType.NAY}

        annotations = {
            "total_yeas": Count("votes__results", filter=Q(**yea)),
            "total_nays": Count("votes__results", filter=Q(**nay)),
            "total_votes": Count("votes__results"),
        }

        bills = (
            Bill.objects.values("title", "sponsor__name")
            .annotate(**annotations)
            .order_by("title")
        )
        votes_cast = bills.aggregate(summ=Sum("total_votes", default=0))

        return {"bills": bills, "votes_cast": votes_cast["summ"]}

    def get_legislators_data(self):
        """
        Fetches and aggregates legislator voting data.

        Returns a dictionary containing:
            - legislators: QuerySet of legislators with annotations for
            total votes, yeas, and nays.
            - total_bills: Total number of bills voted on.
        """

        yea = {'voting_results__vote_type': VoteResult.VoteType.YEA}
        nay = {'voting_results__vote_type': VoteResult.VoteType.NAY}

        annotations = {
            "total_yeas": Count("voting_results", filter=Q(**yea)),
            "total_nays": Count("voting_results", filter=Q(**nay)),
        }

        legislators = (
            Legislator.objects.values("name").annotate(**annotations).order_by("name")
        )
        total_bills = Vote.objects.values("bill").distinct().count()

        return {"legislators": legislators, "total_bills": total_bills}

    def get_template(self, tab):
        """
        Returns the appropriate template name based on the requested tab.
        """
        templates = {
            "charts": "bills/charts.html",
            "tables": "bills/tables.html",
        }
        return templates.get(tab, "base.html")
