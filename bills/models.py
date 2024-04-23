from django.db import models


class Legislator(models.Model):
    """
    Model representing a Person, an individual elected to government.
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"


class Bill(models.Model):
    """
    Model representing a piece of legislation introduced in the Congress.
    """
    title = models.CharField(max_length=255)
    sponsor = models.ForeignKey(Legislator, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.title}"


class Vote(models.Model):
    """
    Model representing a vote on a particular Bill.
    """
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)


class VoteResult(models.Model):
    """
    Model representing a vote cast by a legislator for or against a piece of
    legislation.
    """

    class VoteType(models.IntegerChoices):
        """
        Represents the available types of Votes.
        """
        YAE = 1
        NAY = 2

    legislator = models.ForeignKey(Legislator, on_delete=models.PROTECT)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    vote_type = models.IntegerField(choices=VoteType.choices)
